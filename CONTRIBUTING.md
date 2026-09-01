# Contribuer au Knowledge Catalog SOS-EcoVadis

Ce dépôt est la source de vérité d'un catalogue de connaissances publié sous le
nom d'un praticien. Une fiche fausse coûte plus cher qu'une fiche absente.

La gouvernance complète — propriétaires, cadence de révision, archivage,
nommage, versionnement, règles de contenu — est dans **[GOVERNANCE.md](GOVERNANCE.md)**.
Ce fichier ne dit que l'essentiel pour contribuer.

## Qui valide

François Dequenne (fd@esgim.eu) est propriétaire du catalogue et valide toute
fiche. Aucune fiche ne passe en `status: published` sans sa relecture.

## Le cycle d'une fiche

```
Note Evernote (capture)
   ↓  export .enex
Fiche normalisée, trois langues        status: draft   reliability: expert-drafted
   ↓  relecture François — « approved »
Fiche validée                          status: published   reliability: expert-validated
   ↓  commit sur main
```

`status: review` est l'état d'attente : le contenu vient d'une note experte, la
mise en fiche et les traductions attendent la relecture.

## Sources acceptables

Voir `taxonomy/sources-registry.yaml`, qui fait autorité.

- **Autorisé** : référentiels (EcoVadis, GRI, GHG Protocol, ISO), régulateurs
  (Commission européenne, EUR-Lex), normalisateurs (EFRAG), institutions
  publiques (SPF Emploi, Unia), et le portefeuille de missions ESGIM.
- **Interdit** : cabinets de conseil concurrents, plateformes de notation
  concurrentes, agrégateurs et comparateurs commerciaux.

Toute affirmation chiffrée, datée ou réglementaire porte une référence, placée
immédiatement après l'affirmation. Une donnée issue du portefeuille ESGIM est
attribuée à ESGIM, jamais présentée comme un chiffre publié par EcoVadis.

## Ce qu'une fiche doit respecter

- **Front matter complet** — validé par `schemas/knowledge-object.schema.json`.
  `description` fait entre 70 et 155 caractères et résume la réponse.
- **Un H1 unique**, formulé comme la question qu'un humain pose.
- **Un bloc de résumé en tête** (« En bref »), lisible seul.
- **Au moins 30 % d'intertitres interrogatifs** sur un article.
- **Parité linguistique** — un objet existe en EN, FR et NL, sous le même `id`.
- **Néerlandais = flamand.** En cas d'écart avec l'usage des Pays-Bas, le
  flamand l'emporte : kmo, VTE, rapportering, vouvoiement « u », FOD, Unia. Le
  glossaire (`catalog/glossary/`) prime sur toute autre source terminologique.
  Le NL se traduit depuis l'anglais ou depuis le concept, jamais depuis le
  français.
- **Slugs stables.** Un slug publié ne change jamais : on redirige.

## Avant de proposer une modification

```bash
python3 scripts/build_index.py --check-only   # valide sans rien écrire
python3 scripts/build_index.py                # régénère index et public/
```

Le build refuse : champ obligatoire manquant, `description` hors fenêtre, id ou
slug dupliqué, slug `related` non résolu, source inconnue du registre, parité
de langues rompue, objet sans hub, fiche publiée dont la révision est due.

La même validation tourne en GitHub Actions sur chaque push et chaque pull
request. Un build rouge bloque la fusion.

## Ce qu'il ne faut pas faire

- Éditer à la main `index/catalog.json`, `index/jsonld.json` ou quoi que ce
  soit dans `public/` : ce sont des fichiers générés.
- Écrire un `canonical_url` dans une fiche : il est dérivé de
  `taxonomy/url-plan.yaml`.
- Réutiliser le slug d'une fiche archivée.
- Modifier une fiche `pricing` ou `service` sans instruction explicite de
  François.
