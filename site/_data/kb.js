// Vue du catalogue pour les gabarits : hubs résolus, index slug -> objet,
// URL alternatives par langue. Source unique : index/catalog.json + url-plan.
import fs from "node:fs";
import { urlplan, LANGS, pathFor, hubPath } from "../lib/urls.js";

const catalog = JSON.parse(fs.readFileSync("index/catalog.json", "utf8"));

// Une fiche retirée pour révision dépassée (D32) reste dans catalog.json mais
// ne se rend plus : `indexable` est la seule autorité côté rendu.
const published = catalog.objects.filter(
  (o) => o.status === "published" && o.indexable !== false,
);
const excluded = new Set(
  catalog.objects
    .filter((o) => o.status === "published" && o.indexable === false)
    .map((o) => o.id),
);

// Fiche -> carte affichable dans une liste, pour une langue donnée.
const card = (o, l) => ({
  id: o.id, type: o.type,
  title: o.languages[l]?.title,
  description: o.languages[l]?.description,
  url: o.languages[l] ? pathFor(l, o.type, o.languages[l].slug) : null,
});

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
      .map((o) => card(o, l))
      .filter((m) => m.url)
      .sort((a, b) => a.title.localeCompare(b.title, l)),
  ])),
}));

// Fiches publiées qu'aucun hub ne porte (D31). Elles ne sont pas orphelines :
// l'index des sujets les liste sous « Autres fiches ».
const unhubbed = Object.fromEntries(
  LANGS.map((l) => [l,
    (catalog.unhubbed || [])
      .map((id) => published.find((o) => o.id === id))
      .filter(Boolean)
      .map((o) => card(o, l))
      .filter((m) => m.url)
      .sort((a, b) => a.title.localeCompare(b.title, l)),
  ]),
);

export default {
  branches: urlplan.branches,
  singletons: urlplan.singletons,
  langs: LANGS,
  count: published.length,
  hubs,
  unhubbed,
  excluded: [...excluded],
  bySlug,
  alternates,
  jsonld: JSON.parse(fs.readFileSync("index/jsonld.json", "utf8")),
};
