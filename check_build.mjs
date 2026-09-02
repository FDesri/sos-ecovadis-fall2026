// Contrôle de sortie : toute URL annoncée au sitemap doit exister dans _site,
// aucune fiche non publiée ne doit y être, et chaque page doit porter son
// canonique, son titre et sa description. Sert en local et sur Netlify.
import fs from "node:fs";
import path from "node:path";

const OUT = "_site";
const fail = [];
const note = (m) => fail.push(m);

// 1. URL du sitemap -> fichier présent
const sm = fs.readFileSync("public/sitemap.xml", "utf8");
const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
for (const loc of locs) {
  const p = path.join(OUT, new URL(loc).pathname, "index.html");
  if (!fs.existsSync(p)) note(`sitemap : ${loc} n'a pas de page (${p})`);
}

// 2. Aucune fiche non publiée rendue
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const pages = walk(OUT).filter((f) => f.endsWith(".html"));

const catalog = JSON.parse(fs.readFileSync("index/catalog.json", "utf8"));
const notPublished = catalog.objects.filter((o) => o.status !== "published");
for (const o of notPublished) {
  for (const [, v] of Object.entries(o.languages || {})) {
    for (const p of pages) {
      if (p.includes(`/${v.slug}/`)) note(`fiche non publiée rendue : ${o.id} ${v.slug}`);
    }
  }
}

// 3. Balises obligatoires sur chaque page
for (const p of pages) {
  const html = fs.readFileSync(p, "utf8");
  const url = "/" + path.relative(OUT, p).replace(/index\.html$/, "").replace(/\\/g, "/");
  if (!/<link rel="canonical" href="https:\/\/[^"]+">/.test(html)) note(`canonical absent : ${url}`);
  if (!/<title>.+<\/title>/.test(html)) note(`title absent : ${url}`);
  if (!/<meta name="description" content=".{20,}">/.test(html)) note(`description absente ou courte : ${url}`);
  if ((html.match(/<h1[ >]/g) || []).length !== 1) note(`H1 non unique : ${url}`);
  if (!/<html lang="(fr|nl|en)">/.test(html)) note(`attribut lang absent : ${url}`);
}

// 4. Tout lien interne doit aboutir à une page produite
const known = new Set(pages.map((p) => "/" + path.relative(OUT, p).replace(/index\.html$/, "").replace(/\\/g, "/")));
for (const f of ["/robots.txt", "/sitemap.xml", "/llms.txt", "/catalog.json", "/feed.xml", "/assets/css/main.css"]) known.add(f);
for (const p of pages) {
  const html = fs.readFileSync(p, "utf8");
  const from = "/" + path.relative(OUT, p).replace(/index\.html$/, "").replace(/\\/g, "/");
  for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
    if (!known.has(m[1])) note(`lien interne mort : ${from} -> ${m[1]}`);
  }
}

// 5. Fichiers machine à la racine
for (const f of ["robots.txt", "sitemap.xml", "llms.txt", "catalog.json", "404.html"]) {
  if (!fs.existsSync(path.join(OUT, f))) note(`fichier machine absent : /${f}`);
}

console.log(`pages HTML : ${pages.length} · URL au sitemap : ${locs.length}`);
if (fail.length) {
  console.error(`\n${fail.length} problème(s) :`);
  for (const f of fail.slice(0, 40)) console.error("  - " + f);
  process.exit(1);
}
console.log("Contrôle de sortie : tout est vert.");
