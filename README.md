# SOS-EcoVadis — Knowledge Catalog

*(EN) The structured, governed, trilingual (EN-FR-NL) knowledge base behind sos-ecovadis.com: EcoVadis expertise for Belgian SMEs, packaged as autonomous knowledge objects that humans, search engines and AI agents (RAG, assistants, LLM search) can retrieve and cite. Repo docs are in French; the catalog itself is trilingual.*

Ce dépôt est la **source de vérité** du projet SOS-EcoVadis (ESG Interim Management, [esgim.eu](https://esgim.eu)). Il transforme les connaissances EcoVadis d'ESGIM — jusqu'ici dispersées dans des notes Evernote — en un **actif structuré, gouverné et exploitable par des humains et des agents IA**.

Le site web n'est qu'une vue parmi d'autres sur cette connaissance. Les agents IA, les moteurs de recherche, les assistants commerciaux et les landing pages exploitent tous la même source, gouvernée et versionnée ici.

## Architecture en quatre couches

```
1. Knowledge Inventory   → SOURCES.md (registre des notes sources et de leur provenance)
2. Knowledge Catalogue   → catalog/  (fiches normalisées + métadonnées, EN-FR-NL)
3. Knowledge Graph       → champs `related`, `translation_of`, `ecovadis_questions`
                           + index/catalog.json (le graphe sérialisé)
4. AI Layer              → index/llms.txt, catalog.json ; à terme : embeddings
                           (pipeline GitHub Actions → Supabase pgvector → Netlify → agent IA)
```

## Structure du dépôt

```
taxonomy/     taxonomy.yaml            facettes: situations S1-S3, tailles, thèmes, sujets, audiences
              url-plan.yaml            LE plan d'URL canonique — source unique des URL
              hubs.yaml                16 hubs thématiques (index par sujet), avec leur texte
              sources-registry.yaml    18 sources citables + politique de liens sortants
              intents.json             niveau d'intention de chaque objet
              ecovadis-question-codes.json  46 codes du questionnaire
schemas/      knowledge-object.schema.json  le modèle unique de toute fiche (v2)
catalog/      en/ fr/ nl/ — un dossier par langue
                articles/  faq/  pricing/  services/  experts/  organization/
              glossary/ — le glossaire trilingue (objet unique)
index/        catalog.json             graphe machine complet, généré
              jsonld.json              JSON-LD schema.org par objet, généré
public/       robots.txt sitemap.xml llms.txt             ← servis à la RACINE du domaine, générés
measurement/  question-panel.md/.csv   panel de mesure de découvrabilité, généré
scripts/      build_index.py           index, hubs, sitemap, JSON-LD, llms.txt + VALIDATION
              publish.py               review → published
              migrate_v2.py            migration du front matter
              rewrite_headings.py      intertitres interrogatifs
              link_sources.py          références au plus près des affirmations
              build_question_panel.py  panel de mesure
              parse_enex.py            ENEX → texte
              check_build.mjs          contrôle du site produit (URL, balises, liens)
site/         _data/                   vue du catalogue pour les gabarits (générée à la volée)
              _includes/               gabarit unique + partial <head>
              lib/urls.js              construction des URL, même règle que build_index.py
              assets/css/main.css      feuille de base — l'identité ESGIM viendra avec la landing
              hub.njk topics.njk lang-home.njk feed.njk 404.njk
eleventy.config.js  le rendu HTML : quels fichiers, quels dossiers
netlify.toml  build, en-têtes de sécurité, redirections
GOVERNANCE.md propriétaires, validation, révision, archivage, nommage, décisions, robots
CONTRIBUTING.md  l'essentiel pour contribuer
CHANGELOG.md  ce qui a changé, version par version
LICENSE       CC BY-NC 4.0 pour le contenu, MIT pour le code
SOURCES.md    registre: chaque fiche ↔ sa note source ↔ son fichier d'origine
CITATION.cff  comment citer ce catalogue
```

**Ce qui est généré ne s'édite pas à la main** : tout `index/`, tout `public/`,
tout `measurement/`. Régénérer avec `python3 scripts/build_index.py`.

## Le rendu HTML

Le catalogue est publié en HTML sur son domaine : c'est la condition pour qu'un
moteur ou un assistant puisse le citer. Une URL `raw.githubusercontent.com`
n'est jamais canonique.

```bash
npm install            # une fois
npm run build          # produit _site/ (356 pages)
npm run check          # vérifie le résultat, sort en erreur si quelque chose manque
npm run serve          # aperçu local sur http://localhost:8080
```

Le rendu est **une vue, jamais une source**. Il ne décide rien :

| Ce qu'il affiche | D'où ça vient |
|---|---|
| L'URL de chaque page | `taxonomy/url-plan.yaml`, via la même fonction que `build_index.py` |
| Titre, description, résumé | le front matter de la fiche |
| JSON-LD | `index/jsonld.json` |
| Hubs et fiches rattachées | `index/catalog.json` |
| Ce qui est publié | `status: published` — le reste n'est pas rendu (décision D19) |

Conséquence : après toute modification d'une fiche, `python3 scripts/build_index.py`
d'abord, `npm run build` ensuite. L'inverse produit un site qui ment sur lui-même.

`npm run check` refuse le build si une URL du sitemap n'a pas de page, si une fiche
non publiée est rendue, s'il manque un canonique, un titre, une description, un H1
unique ou l'attribut `lang`, ou si un lien interne ne mène nulle part. Netlify lance
ce contrôle à chaque déploiement : un catalogue incohérent ne part pas en ligne.

## Le modèle de fiche

Chaque fiche est un fichier Markdown avec front matter YAML validé par `schemas/knowledge-object.schema.json`. Une fiche = **un objet autonome** : elle porte son identité (`id` permanent partagé entre langues), sa classification (situations, tailles, thèmes, sujets), ses mots-clés multilingues, ses codes questions EcoVadis, ses relations (`related`), sa provenance (`source_note`), sa fiabilité et son statut de validation.

Le corps répond aux questions qu'une IA cherche : **quoi** (résumé answer-first « En bref »), **pourquoi**, **comment**, **qui**, **quand** — puis les questions fréquentes associées.

Types d'objets : `article`, `faq` (une question humaine = un objet), `pricing`, `service`, `expert`, `glossary`.

## Les trois langues

| Langue | Rôle | Règles clés |
|---|---|---|
| EN | Pivot terminologique | Termes de la plateforme (scorecard, assessment, supporting documents) |
| FR | Langue principale | « fiche d'évaluation (scorecard) », « Social et Droits Humains », « Achats Responsables » |
| NL | **Flamand** (néerlandais de Belgique) | En cas d'écart avec l'usage des Pays-Bas, le flamand l'emporte toujours : scorecard (non traduit), kmo (+ mkb en keywords), VTE, rapportering, références FOD/Unia, vouvoiement « u » |

Le NL se traduit depuis l'anglais ou le concept, **jamais depuis le français**. Référence : le glossaire (`catalog/glossary/`), qui prime sur toute autre source terminologique.

## Ajouter une connaissance

1. Capturer dans Evernote avec l'en-tête standard (`Taxonomy: … / Size … / Situations: … / Thème` + `Human question-like: "…"`).
2. Exporter en `.enex` (une note par fichier) → Drive `sos_ecovadis_fall2026/01_inbox_enex` ou directement dans une conversation Claude du projet.
3. Claude convertit (`scripts/parse_enex.py`), crée la fiche normalisée dans les trois langues, met à jour `SOURCES.md`, `related` et les index.
4. François relit → « approved » → `status: published`, commit.

## Exploitation par les IA

- `index/llms.txt` : répertoire lisible par les LLMs (une ligne par fiche : URL future, titre-question, résumé).
- `index/catalog.json` : l'intégralité du graphe (objets, métadonnées, relations) pour RAG, chatbots et assistants.
- Chaque fiche est autonome : elle peut être servie seule comme contexte sans perdre son sens.

Vision produit complète : `SOS-ECOVADIS_project_vision_v1.1.md` (connaissance du projet Claude). Gouvernance : `GOVERNANCE.md`.
