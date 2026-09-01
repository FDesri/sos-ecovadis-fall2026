// Flux Atom : les 30 fiches françaises publiées les plus récentes.
import fs from "node:fs";
import { pathFor } from "../lib/urls.js";

const catalog = JSON.parse(fs.readFileSync("index/catalog.json", "utf8"));

const items = catalog.objects
  .filter((o) => o.status === "published" && o.languages.fr)
  .map((o) => ({
    title: o.languages.fr.title,
    description: o.languages.fr.description,
    url: pathFor("fr", o.type, o.languages.fr.slug),
    updated: `${o.date_updated}T00:00:00Z`,
  }))
  .sort((a, b) => b.updated.localeCompare(a.updated))
  .slice(0, 30);

export default { items, updated: items[0]?.updated || new Date().toISOString() };
