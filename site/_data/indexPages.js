// Pages d'index (accueil de langue, index des sujets) : URL et alternatives
// précalculées, comme pour les hubs. Aucune logique d'URL dans les gabarits.
import { urlplan } from "../lib/urls.js";

const ORDER = ["fr", "nl", "en"];
const homeAlt = Object.fromEntries(ORDER.map((x) => [x, `/${x}/`]));
const topicAlt = Object.fromEntries(ORDER.map((x) => [x, `/${x}/${urlplan.branches.hub[x]}/`]));

export default {
  home: ORDER.map((l) => ({ lang: l, url: `/${l}/`, alt: homeAlt })),
  topics: ORDER.map((l) => ({ lang: l, url: `/${l}/${urlplan.branches.hub[l]}/`, alt: topicAlt })),
};
