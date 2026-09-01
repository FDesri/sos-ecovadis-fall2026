// Métadonnées du site. Le domaine canonique vient de taxonomy/url-plan.yaml :
// il n'est JAMAIS écrit en dur ailleurs.
import fs from "node:fs";
import yaml from "js-yaml";

const urlplan = yaml.load(fs.readFileSync("taxonomy/url-plan.yaml", "utf8"));
const base = `${urlplan.site.scheme}://${urlplan.site.canonical_host}`;

export default {
  url: process.env.URL_CANONIQUE || base,
  name: "SOS-EcoVadis",
  tagline: {
    fr: "Base de connaissances EcoVadis pour les TPE et PME",
    nl: "EcoVadis-kennisbank voor kmo's",
    en: "EcoVadis knowledge base for small companies",
  },
  publisher: "ESG Interim Management",
  publisherUrl: "https://esgim.eu/",
  aboutUrl: "https://esgim.eu/about",   // GOVERNANCE §7 décision 8
  author: "François Dequenne",
  license: { name: "CC BY-NC 4.0", url: "https://creativecommons.org/licenses/by-nc/4.0/" },
  langs: ["fr", "nl", "en"],
};
