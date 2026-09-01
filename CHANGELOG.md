# Changelog

Toutes les évolutions notables du Knowledge Catalog SOS-EcoVadis.
Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Versionnement : le catalogue suit un versionnement sémantique propre, distinct
du champ `version` de chaque fiche.

## [2.0.0] — 2026-09-01

Mise en conformité avec la grille de contrôle « LLM-ready » pour un Knowledge
Catalogue. Décisions D13 à D21, documentées dans la vision v1.2.

### Ajouté

- `taxonomy/url-plan.yaml` — plan d'URL canonique étendu aux sept types
  d'objets. Étend §5.1 de la vision v1.1 sans le contredire (KC-C01, KC-T03).
- `taxonomy/hubs.yaml` — 16 hubs thématiques sur un axe unique, le sujet. Plus
  aucun objet orphelin : 106 sur 106 sont rattachés (KC-S09, KC-T07, KC-L03).
- `taxonomy/sources-registry.yaml` — 18 sources citables, URL vérifiées,
  politique de liens sortants explicite (KC-C11, KC-T11).
- `taxonomy/intents.json` — classification des objets par niveau d'intention
  (KC-S03).
- Objet `kb-0006` — identité d'ESG Interim Management, en trois langues.
  Reste en `status: draft` tant que les identifiants légaux manquent (KC-S12).
- `measurement/question-panel.md` et `.csv` — 30 questions dérivées du
  catalogue, × 3 langues × 4 moteurs × 3 exécutions (KC-M01, KC-M02).
- `public/` — ce qui sera servi à la racine du domaine : `robots.txt` avec une
  politique de robots explicite, `sitemap.xml`, `llms.txt`, `llms-full.txt`
  (KC-A03 à A06, KC-T06, KC-L01 à L06).
- `index/jsonld.json` — JSON-LD schema.org par objet (KC-T04).
- `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, ce fichier, et un workflow
  GitHub Actions de validation bloquante (KC-G11 à G16).

### Modifié

- Front matter v2 : `description` (70-155 caractères), `intent` et `review_due`
  deviennent obligatoires ; `sources` et `relations` sont ajoutés. 316 fichiers
  migrés (KC-T02, KC-S03, KC-S10, KC-M12).
- 316 meta descriptions rédigées à la main, une par fiche et par langue.
- Intertitres des 32 articles reformulés en questions : 9 H2 interrogatifs sur
  639 avant, 447 sur 639 après, aucune fiche sous le seuil de 30 % (KC-C05).
- 259 références posées dans les corps, à l'endroit de l'affirmation : 96
  articles sur 96 portent désormais une référence liée, contre 3 avant
  (KC-C11).
- `scripts/build_index.py` réécrit : dérive les URL canoniques du plan d'URL,
  génère les hubs, le sitemap, le JSON-LD, `llms.txt` et `llms-full.txt`, et
  refuse le build sur toute erreur de cohérence (KC-G15).
- Licence explicitée : CC BY-NC 4.0 pour le contenu, MIT pour le code.

### Décidé

- **D14** — révision de la décision de gouvernance n° 5 du 27/08 : les liens
  vers les référentiels, régulateurs et institutions publiques sont autorisés ;
  ceux vers les concurrents d'ESGIM restent interdits.
- **D19** — seuls les objets en `status: published` reçoivent une URL canonique
  et entrent au sitemap et dans `llms.txt`. Les 106 objets étant en relecture,
  les surfaces publiques sont volontairement vides à ce jour.

## [1.0.0] — 2026-08-27

Première version opérationnelle : 105 objets de connaissance trilingues
EN-FR-NL, taxonomie, schéma, index machine, gouvernance et registre des
sources, issus de 37 notes Evernote dédupliquées.
