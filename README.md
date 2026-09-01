# sos-ecovadis

Site statique de **SOS-EcoVadis** : landing de campagne (FR d'abord, puis NL et EN)
et, à terme, publication HTML du Knowledge Catalogue EcoVadis.

Éditeur : **IMAGINATION@WORK SRL** — BCE 0774.373.269, TVA BE0774.373.269,
Boulevard du Souverain 24, 1170 Watermael-Boitsfort.
**ESG INTERIM MANAGEMENT (ESGIM)** est une marque de cette société.
Auteur : François Dequenne — fd@esgim.eu.

Vision et décisions : `SOS-ECOVADIS_project_vision_v1.1.md` (projet Claude).
Nous sommes à l'**étape 1 — preuve de pipeline**.

## Ce que fait ce dépôt

| Brique | Choix |
|---|---|
| Générateur | Eleventy 3 (Nunjucks + Markdown), Node 20 |
| Hébergeur | Netlify — build `npm run build`, publication `_site` |
| Domaine cible | sos-ecovadis.com (apex canonique, www redirigé) |
| Suivi | HubSpot Starter, portail 9391878 — branché à l'étape 2 |
| Réservation | Calendly, 30 min, 125 € HTVA, prépayé |

## Démarrer

```bash
npm install
npm run serve     # http://localhost:8080/fr/
npm run build     # génère _site/
```

## Arborescence

```
eleventy.config.js        configuration du générateur
netlify.toml              build, en-têtes de sécurité, CSP, redirections
src/_data/site.js         faits du site (éditeur, auteur, réservation)
src/_data/urlplan.js      plan d'URL par langue — jamais recopié dans une page
src/_includes/layouts/    gabarits
src/_includes/partials/   <head>, blocs réutilisables
src/assets/css/main.css   jetons de base (l'identité ESGIM arrive à l'étape 2)
src/fr/index.njk          page de preuve de pipeline
src/404.njk               page introuvable
```

## Règles qui ne se négocient pas

- Le préfixe de langue (`/fr/`, `/nl/`, `/en/`) et les mots
  `savoir` / `kennis` / `knowledge` sont figés : ils coûtent cher à changer une
  fois indexés.
- Un slug publié ne change jamais — on redirige.
- Aucune page n'écrit son `canonical` à la main : il est dérivé du plan d'URL.
- Rien n'est indexable tant que la page n'est pas relue (`robots: noindex` par
  défaut sur les pages de chantier).
- Aucun changement sur esgim.eu, aucune demande à l'agence qui l'exploite.

## Étapes suivantes

2. Coquille de la landing `/fr/`, pages légales, script HubSpot + bandeau de
   consentement, identité ESGIM.
3. Pages de situation S1/S2/S3, CTA HubSpot, propagation des UTM jusqu'à Calendly.
4. Publication des fiches : gabarit, JSON-LD, `sitemap.xml`, `llms.txt`, RSS.
5. Mise en ligne : domaine, HTTPS, Search Console, test e-mail bout en bout.
