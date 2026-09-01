// Plan d'URL (v1.1) — branches par langue. Étendu aux autres types d'objets
// le jour où les fiches sont publiées ; les branches ci-dessous ne changent plus.
module.exports = {
  root: { fr: "/fr/", nl: "/nl/", en: "/en/" },
  situations: {
    S1: { fr: "/fr/monter/", nl: "/nl/opwaarderen/", en: "/en/upgrade/" },
    S2: { fr: "/fr/retrograde/", nl: "/nl/terugval/", en: "/en/downgrade/" },
    S3: {
      fr: "/fr/premiere-evaluation/",
      nl: "/nl/eerste-evaluatie/",
      en: "/en/first-assessment/",
    },
  },
  knowledge: { fr: "/fr/savoir/", nl: "/nl/kennis/", en: "/en/knowledge/" },
  legal: {
    fr: {
      mentions: "/fr/mentions-legales/",
      privacy: "/fr/confidentialite/",
      cookies: "/fr/cookies/",
    },
  },
};
