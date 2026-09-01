// Faits du site. Une seule source, jamais recopiée dans une page.
module.exports = {
  name: "SOS-EcoVadis",
  // URL_PRODUCTION est injectée par Netlify (voir netlify.toml) ; en local on retombe
  // sur l'URL de déploiement, puis sur le domaine cible.
  url:
    process.env.URL_CANONIQUE ||
    process.env.URL ||
    "https://sos-ecovadis.com",
  langDefault: "fr",
  langs: ["fr", "nl", "en"],
  publisher: {
    legalName: "IMAGINATION@WORK SRL",
    brand: "ESG INTERIM MANAGEMENT (ESGIM)",
    vatID: "BE0774.373.269",
    companyNumber: "0774.373.269",
    street: "Boulevard du Souverain 24",
    postalCode: "1170",
    city: "Watermael-Boitsfort",
    country: "BE",
    legalUrl: "https://esgim.eu/legal",
  },
  author: {
    name: "François Dequenne",
    email: "fd@esgim.eu",
    org: "ESGIM",
    aboutUrl: "https://esgim.eu",
  },
  booking: {
    url: "https://calendly.com/francois-dequenne/30min",
    label: "Réserver mon appel de 30 min — 125 € HTVA",
  },
  hubspot: {
    portalId: "9391878",
    // Le script HubSpot et le bandeau de consentement arrivent à l'étape 2.
    enabled: false,
  },
};
