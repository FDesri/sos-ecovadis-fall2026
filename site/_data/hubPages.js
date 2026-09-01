// Une page par hub et par langue (16 × 3 = 48), plus l'index des sujets.
import kb from "./kb.js";

export default kb.hubs.flatMap((h) =>
  kb.langs.map((l) => ({
    lang: l,
    id: h.id,
    url: h.path[l],
    title: h.title[l],
    members: h.members[l],
    alt: Object.fromEntries(kb.langs.map((x) => [x, h.path[x]])),
  })),
).filter((p) => p.members.length > 0);
