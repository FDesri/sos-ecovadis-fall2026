/* Suivi HubSpot et bandeau de consentement — ÉCRITS, INERTES.
 *
 * Rien ne s'allume tant que ACTIF vaut false. C'est voulu : sur
 * sos-ecovadis.netlify.app, le suivi ne compterait rien, et le domaine
 * sos-ecovadis.com n'est pas encore branché. Bascule à l'étape 5, quand
 * le domaine est en place et que HubSpot connaît ce domaine.
 *
 * Pour allumer, à l'étape 5 :
 *   1. passer ACTIF à true ;
 *   2. dans HubSpot, Réglages → Confidentialité → Cookies, activer
 *      l'opt-in européen et ajouter sos-ecovadis.com aux domaines suivis.
 * La CSP de netlify.toml autorise déjà js.hs-scripts.com et js.hs-banner.com :
 * il n'y a rien à y toucher.
 */
(function () {
  "use strict";

  var ACTIF = false;
  var PORTAIL = "9391878";
  var CLE = "sos-ecovadis-consentement";

  var bandeau = document.getElementById("consentement");
  if (!ACTIF || !bandeau) return;

  function chargerHubSpot() {
    if (document.getElementById("hs-script-loader")) return;
    var s = document.createElement("script");
    s.id = "hs-script-loader";
    s.async = true;
    s.defer = true;
    s.type = "text/javascript";
    s.src = "https://js.hs-scripts.com/" + PORTAIL + ".js";
    document.head.appendChild(s);
  }

  function memoriser(valeur) {
    try { localStorage.setItem(CLE, valeur); } catch (e) { /* navigation privée */ }
  }

  var deja = null;
  try { deja = localStorage.getItem(CLE); } catch (e) { /* idem */ }

  if (deja === "oui") { chargerHubSpot(); return; }
  if (deja === "non") return;

  bandeau.hidden = false;
  bandeau.querySelector("[data-consent='oui']").addEventListener("click", function () {
    memoriser("oui");
    bandeau.hidden = true;
    chargerHubSpot();
  });
  bandeau.querySelector("[data-consent='non']").addEventListener("click", function () {
    memoriser("non");
    bandeau.hidden = true;
  });
})();
