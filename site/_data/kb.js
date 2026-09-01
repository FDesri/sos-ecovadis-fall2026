// Vue du catalogue pour les gabarits : hubs résolus, index slug -> objet,
// URL alternatives par langue. Source unique : index/catalog.json + url-plan.
import fs from "node:fs";
import { urlplan, LANGS, pathFor, hubPath } from "../lib/urls.js";

const catalog = JSON.parse(fs.readFileSync("index/catalog.json", "utf8"));

const published = catalog.objects.filter((o) => o.status === "published");

// slug (par langue) -> fiche, pour résoudre `related`
const bySlug = {};
for (const lang of LANGS) bySlug[lang] = {};
for (const o of published) {
  for (const lang of LANGS) {
    const v = o.languages[lang];
    if (!v) continue;
    bySlug[lang][v.slug] = {
      id: o.id, type: o.type, title: v.title, description: v.description,
      url: pathFor(lang, o.type, v.slug),
    };
  }
}

// id -> URL par langue, pour hreflang
const alternates = {};
for (const o of published) {
  alternates[o.id] = {};
  for (const lang of LANGS) {
    const v = o.languages[lang];
    if (v) alternates[o.id][lang] = pathFor(lang, o.type, v.slug);
  }
}

// hubs, membres publiés résolus par langue
const hubs = catalog.hubs.map((h) => ({
  id: h.id,
  slug: h.slug,
  title: h.title,
  path: Object.fromEntries(LANGS.map((l) => [l, hubPath(l, h.slug[l])])),
  members: Object.fromEntries(LANGS.map((l) => [l,
    h.members
      .map((id) => published.find((o) => o.id === id))
      .filter(Boolean)
      .map((o) => ({
        id: o.id, type: o.type,
        title: o.languages[l]?.title,
        description: o.languages[l]?.description,
        url: o.languages[l] ? pathFor(l, o.type, o.languages[l].slug) : null,
      }))
      .filter((m) => m.url)
      .sort((a, b) => a.title.localeCompare(b.title, l)),
  ])),
}));

export default {
  branches: urlplan.branches,
  singletons: urlplan.singletons,
  langs: LANGS,
  count: published.length,
  hubs,
  bySlug,
  alternates,
  jsonld: JSON.parse(fs.readFileSync("index/jsonld.json", "utf8")),
};
