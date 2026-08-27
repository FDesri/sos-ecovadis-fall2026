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
taxonomy/     taxonomy.yaml (facettes: situations S1-S3, tailles, thèmes, sujets, audiences)
              ecovadis-question-codes.json (46 codes du questionnaire, avec thème et libellé)
schemas/      knowledge-object.schema.json (le modèle unique de toute fiche)
catalog/      en/ fr/ nl/ — un dossier par langue
                articles/  faq/  pricing/  services/  experts/
              glossary/ — le glossaire trilingue (objet unique)
index/        catalog.json (index machine complet, généré)
              llms.txt (répertoire pour LLMs, généré)
scripts/      parse_enex.py (ENEX → texte), build_index.py (fiches → index)
GOVERNANCE.md propriétaires, workflow de validation, révision, archivage, nommage
SOURCES.md    registre: chaque fiche ↔ sa note source ↔ son fichier d'origine
```

## Le modèle de fiche

Chaque fiche est un fichier Markdown avec front matter YAML validé par `schemas/knowledge-object.schema.json`. Une fiche = **un objet autonome** : elle porte son identité (`id` permanent partagé entre langues), sa classification (situations, tailles, thèmes, sujets), ses mots-clés multilingues, ses codes questions EcoVadis, ses relations (`related`), sa provenance (`source_note`), sa fiabilité et son statut de validation.

Le corps répond aux questions qu'une IA cherche : **quoi** (résumé answer-first « En bref »), **pourquoi**, **comment**, **qui**, **quand** — puis les questions fréquentes associées.

Types d'objets : `article`, `faq` (une question humaine = un objet), `pricing`, `service`, `expert`, `glossary`.

## Les trois langues

| Langue | Rôle | Règles clés |
|---|---|---|
| EN | Pivot terminologique | Termes de la plateforme (scorecard, assessment, supporting documents) |
| FR | Langue principale | « fiche d'évaluation (scorecard) », « Social et Droits Humains », « Achats Responsables » |
| NL | Néerlandais de Belgique | scorecard (non traduit), kmo (+ mkb en keywords), VTE, rapportering, vouvoiement « u » |

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
