# Gouvernance du Knowledge Catalog SOS-EcoVadis

Version 1.0 — 27 août 2026. Propriétaire du document : François Dequenne (ESGIM).

Sans gouvernance, un catalogue devient obsolète. Ce document fixe qui possède quoi, quand on révise, comment on valide, comment on archive, comment on nomme et comment on versionne.

## 1. Rôles et propriétaires

| Rôle | Titulaire | Responsabilité |
|---|---|---|
| Propriétaire du catalogue | François Dequenne (fd@esgim.eu) | Décisions finales, validation de toute fiche, tarifs |
| Propriétaire par domaine | François Dequenne (par défaut) ; un expert ESGIM peut être désigné par thème via `expert_reviewer` | Exactitude méthodologique du domaine |
| Rédaction et maintenance | Claude (sessions du projet « Create and promote ESG consultancy services ») | Conversion ENEX → fiches, traductions, index, cohérence |
| Source de vérité | Ce dépôt GitHub (`FDesri/sos-ecovadis-fall2026`) | Evernote = capture uniquement ; Drive = bureau de relecture |

## 2. Workflow de validation

```
Note Evernote (capture)
   ↓  export .enex → Drive 01_inbox_enex ou dépôt dans la conversation Claude
Fiche normalisée (Claude)          status: draft   reliability: expert-drafted
   ↓  relecture François — « approved » / « approved with changes »
Fiche validée                      status: published   reliability: expert-validated
   ↓  commit sur main → exploitation (site, RAG, agents IA)
```

Règle : rien ne passe en `status: published` sans relecture humaine. Les fiches créées en masse le 27/08/2026 sont en `status: review` : le contenu vient des notes expertes, la mise en fiche et les traductions attendent la relecture de François.

## 3. Fréquence de révision

| Objet | Cadence | Déclencheur additionnel |
|---|---|---|
| Fiches méthodologie / médailles / seuils | Trimestrielle | Toute évolution méthodologique EcoVadis, conférence Sustain annuelle |
| Scores indicatifs des médailles (Bronze ≈ 64, Argent ≈ 73…) | À chaque mise à jour du portefeuille ESGIM | Rising Bar : les seuils montent en continu |
| Pricing (kb-0001) et services (kb-0003, kb-0004) | À chaque révision tarifaire ESGIM | Jamais modifiés sans instruction explicite de François |
| Glossaire (kb-0005) | Annuelle | Ouverture d'un Help Center NL EcoVadis ; renommage de modules |
| FAQ | Semestrielle | Nouvelles questions récurrentes des prospects |
| Expert (kb-0002) | Annuelle | — |

Chaque révision incrémente `version`, met à jour `date_updated`, et se trace dans l'historique git.

## 4. Politique d'archivage

Une fiche remplacée n'est jamais supprimée : `status: archived`, déplacement vers `catalog/_archive/`, et la fiche qui la remplace la référence dans `source_note`. Les slugs publiés ne sont jamais réutilisés. Les notes sources (.enex) restent archivées dans Drive `sos_ecovadis_fall2026` ; le registre `SOURCES.md` fait le lien fiche ↔ note ↔ fichier Drive.

## 5. Règles de nommage

- Fichiers : `catalog/<lang>/<type-pluriel>/<slug>.md` ; slug en kebab-case, minuscules, sans date, stable après publication.
- IDs : `kb-XXXX`, permanents, partagés par les trois langues d'un même objet. Plages par type dans `taxonomy/taxonomy.yaml`.
- Slugs localisés par langue ; le lien entre langues passe par l'`id` (et `translation_of`).
- Terminologie : le glossaire (kb-0005) prime. FR traduit « scorecard » en « fiche d'évaluation », le NL garde « scorecard » ; NL de Belgique : kmo, VTE, rapportering, vouvoiement « u ».

## 6. Gestion des versions

- Git est l'historique : un commit par lot cohérent, messages explicites.
- `version` (front matter) s'incrémente à chaque changement de fond ; les corrections typographiques n'incrémentent pas.
- Les index (`index/catalog.json`, `index/llms.txt`) sont générés par `scripts/build_index.py` — jamais édités à la main. Les régénérer après toute modification de fiche.

## 7. Règles de contenu (décisions actées le 27/08/2026)

1. **Source unique** : toutes les fiches proviennent de la même source propriétaire ESGIM (notes de François Dequenne), quelle que soit la mécanique de capture. `source: esgim-proprietary` partout.
2. **Track record ESGIM** : « 100+ projets » (la mention « 600+ » dans certaines notes était une coquille). Les autres chiffres portefeuille (87 % des clients améliorent leur score ; +13,8 points en moyenne) restent tels que dans les notes.
3. **Intervenants externes ponctuels** : les noms d'intervenants externes (notamment C. Savanco, N. Scheepens) ne sont pas repris dans les fiches.
4. **Anonymisation client** : les données de mission (indicateurs chiffrés) sont conservées pour leur valeur pédagogique, mais anonymisées — noms d'entreprises clientes et de personnes remplacés par une description générique (« un client ESGIM, imprimeur flexographique wallon de taille S »).
5. **Codes questions EcoVadis** (ENV7003, SUP307…) : métadonnées de liaison avec le questionnaire (`ecovadis_questions`), pas des titres ni des questions humaines.
6. **Liens externes** : aucun lien vers des consultances concurrentes ; les renvois se font vers d'autres fiches du catalogue (`related`). Les liens utilitaires (outils WRI Aqueduct, WWF Water Risk Filter…) sont conservés.
7. **Bloc « À propos d'ESGIM »** : un seul texte standard (celui de kb-0002 / kb-0003), pas de variantes marketing par fiche.
8. **Boutons / mentions « Qui sommes-nous »** : pointent vers la page À propos d'esgim.eu (hub de crédibilité).

## 8. Extension du catalogue

Nouvelle note → nouvelle fiche : suivre `README.md` § « Ajouter une connaissance ». Nouvelle valeur de taxonomie : l'ajouter d'abord à `taxonomy/taxonomy.yaml` (commit dédié), puis l'utiliser. Nouveau type d'objet (cas client, témoignage…) : définir sa plage d'IDs dans la taxonomie et son gabarit dans `schemas/`.
