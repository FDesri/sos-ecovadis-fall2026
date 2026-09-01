// SOS-EcoVadis — configuration Eleventy 3
// Source de vérité du plan d'URL : src/_data/urlplan.js (miroir de taxonomy/url-plan.yaml
// côté catalogue). Aucun canonical n'est écrit à la main dans une page.

module.exports = function (eleventyConfig) {
  // Actifs recopiés tels quels
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Filtres utilitaires
  eleventyConfig.addFilter("dateISO", (d) =>
    new Date(d).toISOString().slice(0, 10)
  );
  eleventyConfig.addFilter("dateFR", (d) =>
    new Intl.DateTimeFormat("fr-BE", {
      day: "numeric",
      month: "long",
      year: "numeric",
      timeZone: "Europe/Brussels",
    }).format(new Date(d))
  );
  // URL absolue à partir de site.url — sert aux canonical, hreflang, OG, sitemap
  eleventyConfig.addFilter("absolute", function (path) {
    const base = (this.ctx?.site?.url || "").replace(/\/$/, "");
    return base + path;
  });

  eleventyConfig.setQuietMode(true);

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["njk", "md", "html"],
    pathPrefix: "/",
  };
};
