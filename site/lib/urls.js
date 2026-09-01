// Construction des URL du catalogue. Reprend à l'identique la règle de
// scripts/build_index.py : taxonomy/url-plan.yaml est la seule source.
// Ce fichier n'est PAS un fichier de données Eleventy — il n'a pas de place
// dans site/_data, où un export nommé masquerait l'objet exporté par défaut.
import fs from "node:fs";
import yaml from "js-yaml";

export const urlplan = yaml.load(fs.readFileSync("taxonomy/url-plan.yaml", "utf8"));
export const LANGS = ["en", "fr", "nl"];

export function pathFor(lang, type, slug) {
  const s = urlplan.singletons;
  if (type === "glossary") return s.glossary.canonical;
  if (type === "organization") return s.organization[lang];
  return `/${lang}/${urlplan.branches[type][lang]}/${slug}/`;
}

export function hubPath(lang, slug) {
  return `/${lang}/${urlplan.branches.hub[lang]}/${slug}/`;
}
