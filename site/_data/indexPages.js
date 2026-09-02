// Pages d'index (accueil de langue, index des sujets) : URL et alternatives
// précalculées, comme pour les hubs. Aucune logique d'URL dans les gabarits.
import { urlplan } from "../lib/urls.js";

const ORDER = ["fr", "nl", "en"];

// Étape 2 : /fr/ est passé à la landing. L'accueil du catalogue français
// bascule tel quel vers /fr/sujets/, qui listait déjà les mêmes sujets.
// /nl/ et /en/ gardent leur accueil de catalogue tant qu'il n'y a pas de
// landing traduite (spec de l'étape 2, hors périmètre).
const HOME_LANGS = ["nl", "en"];

// L'équivalent français d'un accueil de catalogue est désormais /fr/sujets/ :
// c'est vers là que pointent l'alternative hreflang et le sélecteur de langue,
// pas vers la landing, qui n'a pas de version traduite.
const topicAlt = Object.fromEntries(ORDER.map((x) => [x, `/${x}/${urlplan.branches.hub[x]}/`]));
const homeAlt = Object.fromEntries(
  ORDER.map((x) => [x, x === "fr" ? topicAlt.fr : `/${x}/`]),
);

export default {
  home: HOME_LANGS.map((l) => ({ lang: l, url: `/${l}/`, alt: homeAlt })),
  topics: ORDER.map((l) => ({ lang: l, url: `/${l}/${urlplan.branches.hub[l]}/`, alt: topicAlt })),
};
