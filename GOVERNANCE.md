# Gouvernance du Knowledge Catalog SOS-EcoVadis

Version 1.0 — 27 août 2026. Propriétaire du document : François Dequenne (ESGIM).

Sans gouvernance, un catalogue devient obsolète. Ce document fixe qui possède quoi, quand on révise, comment on valide, comment on archive, comment on nomme et comment on versionne.

## 1. Rôles et propriétaires

| Rôle | Titulaire | Responsabilité |
|---|---|---|
| Éditeur (personne morale) | **IMAGINATION@WORK SRL**, BCE 0774.373.269, Boulevard du Souverain 24 (chez Buzzy Nest), 1170 Watermael-Boitsfort — [mentions légales](https://esgim.eu/legal) | Contracte, facture, engage sa responsabilité. **ESG INTERIM MANAGEMENT (ESGIM) est une marque** déposée auprès de l'Office Benelux de la Propriété Intellectuelle par cette société, pas une société elle-même |
| Propriétaire du catalogue | François Dequenne (fd@esgim.eu), administrateur | Décisions finales, validation de toute fiche, tarifs |
| Propriétaire par domaine | François Dequenne (par défaut) ; un expert ESGIM peut être désigné par thème via `expert_reviewer` | Exactitude méthodologique du domaine |
| Rédaction et maintenance | Claude (sessions du projet « Create and promote ESG consultancy services ») | Conversion ENEX → fiches, traductions, index, cohérence |
| Source de vérité | Ce dépôt GitHub (`FDesri/sos-ecovadis-knowledge-catalogue`) | Evernote = capture uniquement ; Drive = bureau de relecture |

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

**En pratique** — `scripts/publish.py` applique la transition sur les trois langues d'un objet à la fois :

```bash
python3 scripts/publish.py --list          # ce qui attend en review
python3 scripts/publish.py kb-0034         # publier un objet (3 langues)
python3 scripts/publish.py --type pricing  # publier tout un type
python3 scripts/publish.py --all           # tout publier (après relecture complète)
python3 scripts/build_index.py             # régénérer les index — obligatoire
git commit -am "Publish kb-0034" && git push
```

Le script passe `status: review → published`, `reliability → expert-validated`, met `date_updated` au jour, et laisse `version` inchangé (publier n'est pas un changement de fond). `--dry-run` simule, `--keep-reliability` publie sans requalifier la fiabilité (utile pour kb-0001 tant qu'un point tarifaire reste ouvert).

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

**Depuis le 02/09/2026 (D33), cette table est outillée par un champ.** Chaque fiche
déclare une `volatility` et une date `verified_at` ; `review_due` en est dérivée par
`taxonomy/freshness.yaml`. Les cadences : `evergreen` 24 mois, `annual` 12,
`ecovadis-cycle` 6, `event-driven` 3.

`date_updated` change à chaque modification, une virgule comprise. `verified_at` ne
change que lorsque les **faits** ont été revérifiés. Corriger une coquille ne rajeunit
pas un seuil de médaille.

**Ce que fait le build quand une révision est due (D32).** Il avertit trente jours
avant. Il avertit encore une fois l'échéance passée. Si la fiche est volatile
(`ecovadis-cycle` ou `event-driven`), il la retire des surfaces indexables et la marque
`review_required` : elle reste dans `catalog.json`, elle n'est plus servie. Elle ne
devient une **erreur** que dans le commit qui la modifie — on ne retouche pas une fiche
périmée sans regarder ses faits. En aucun cas une date n'arrête la chaîne de
construction : un correctif de sécurité passe toujours.

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
4. **Noms de clients — deux régimes distincts** (précisé le 01/09/2026) :
   - **Références commerciales** (nom du client + résultat obtenu) : on garde **un maximum de noms réels**, avec le résultat exact et son statut (obtenu / en cours). Exemple : kb-0023. Une mission menée par un consultant ESGIM sous une enseigne antérieure est signalée comme telle.
   - **Cas techniques détaillés** (dossier de preuves, documents internes, tonnages, écarts, trous) : **anonymisés** en description sectorielle — « imprimeur flexographique wallon, taille S » (kb-0034/0035/0039), « installateur en techniques spéciales du bâtiment wallon, taille XS » (kb-0038). Les indicateurs chiffrés sont conservés pour leur valeur pédagogique ; les noms de personnes ne le sont jamais.
   Un même client peut relever des deux régimes : CIREPA est nommé comme référence dans kb-0023 et anonymisé comme cas technique dans kb-0034.
5. **Codes questions EcoVadis** (ENV7003, SUP307…) : métadonnées de liaison avec le questionnaire (`ecovadis_questions`), pas des titres ni des questions humaines.
6. **Liens externes — RÉVISÉ le 01/09/2026 (décision D14).** La règle initiale excluait tout lien sortant. Elle visait les concurrents, mais elle privait les fiches de leurs sources : 93 articles sur 96 n'en portaient aucune, alors qu'ils avançaient des chiffres datés et vérifiables. Le contrôle KC-C11 de la grille LLM-ready demande la référence immédiatement après l'affirmation, et c'est un des critères que les moteurs pèsent le plus lourd pour juger une source fiable.
   - **Autorisé** : référentiels (EcoVadis, GRI, GHG Protocol, ISO), régulateurs (Commission européenne, EUR-Lex), normalisateurs (EFRAG), institutions publiques (SPF Emploi / FOD Werkgelegenheid, Unia), outils publics d'analyse de risque. Citer sa source ne renvoie pas le lecteur ailleurs : cela prouve qu'on sait de quoi on parle.
   - **Interdit** : cabinets de conseil concurrents, plateformes de notation concurrentes, agrégateurs et comparateurs commerciaux.
   - Les sources autorisées sont énumérées dans `taxonomy/sources-registry.yaml`. Une fiche les référence par `id` ; le build refuse un `id` inconnu. Une donnée issue du portefeuille ESGIM est attribuée à ESGIM (`esgim-portfolio`), jamais présentée comme un chiffre publié par EcoVadis.
7. **Bloc « À propos d'ESGIM »** : un seul texte standard (celui de kb-0002 / kb-0003), pas de variantes marketing par fiche.
8. **Boutons / mentions « Qui sommes-nous »** : pointent vers la page À propos d'esgim.eu (hub de crédibilité).
9. **Néerlandais = flamand** : en cas d'écart entre l'usage flamand (Belgique) et l'usage des Pays-Bas, **le flamand l'emporte**, toujours. Cela vaut pour le vocabulaire (kmo et non mkb, VTE, rapportering, welzijn op het werk), les institutions et références légales (FOD Werkgelegenheid, Unia, arbeidsreglement), la syntaxe et le registre (vouvoiement « u »). Les termes néerlandais des Pays-Bas ne sont admis qu'en `keywords`, pour la recherche. La colonne NL du glossaire (kb-0005) fait foi ; le NL se traduit depuis l'anglais ou le concept, jamais depuis le français.
10. **Tarifs (kb-0001)** : grille et modalités validées par François le 01/09/2026 — paiement en trois tranches **20 % / 60 % / 20 %**, la dernière tranche conditionnée à l'atteinte du niveau convenu. Prix S1 (montée) pour une XS : **8 000 €** — le tableau de la note source fait foi (arbitré le 01/09/2026).

## 8. Décisions techniques du 01/09/2026 (grille LLM-ready — vision v1.2)

Prises après application des 95 contrôles de la grille « LLM-ready » au dépôt.
Le détail, avec contexte et réversibilité, est dans la vision v1.2 §9.

| # | Décision | Où elle vit |
|---|---|---|
| D13 | **Plan d'URL étendu aux sept types d'objets.** La vision v1.1 ne logeait que les articles ; le catalogue en compte sept types et 106 objets, or KC-C01 exige une URL par unité de connaissance. Les branches articles (`/fr/savoir/`, `/nl/kennis/`, `/en/knowledge/`) sont conservées telles quelles. Les hubs de situation ne sont pas des objets : les pages S1/S2/S3 de la landing en font office, pour éviter la cannibalisation. | `taxonomy/url-plan.yaml` |
| D14 | **Liens sortants vers les sources institutionnelles autorisés**, concurrents toujours interdits. Révise la décision n° 6 ci-dessus. | `taxonomy/sources-registry.yaml` |
| D15 | **Licence explicite** : contenu en CC BY-NC 4.0, code en MIT. Pas de clause « pas de modification » : elle ferait douter du droit de résumer, qui est précisément l'usage recherché. Une licence s'assouplit, ne se resserre pas. | `LICENSE` |
| D16 | **Renommage du dépôt** en `sos-ecovadis-knowledge-catalogue` : « fall2026 » date un actif permanent. À faire tant qu'aucun lien externe n'existe. | action GitHub de François |
| D17 | **Facette d'intention** (`comprendre`, `comparer`, `choisir`, `mettre-en-oeuvre`, `verifier`) sur chaque objet, et **fiche d'identité de l'organisation** (kb-0006), que la grille réclame (KC-S03, KC-S12). | `taxonomy/intents.json`, `catalog/*/organization/` |
| D18 | **Hubs thématiques sur un axe unique, le sujet.** Les quatre thèmes officiels EcoVadis y figurent sous leur nom officiel : un hub « thème » distinct d'un hub « sujet » sur le même contenu serait de la cannibalisation. Un sujet devient un hub à partir de 4 objets. Les hubs sont générés, pas rédigés en double. | `taxonomy/hubs.yaml` | *Portée révisée par D31.*
| D19 | **Rien d'indexable hors `status: published`.** Seuls les objets publiés reçoivent une URL canonique et entrent au sitemap, dans `llms.txt` et dans `llms-full.txt`. Les 106 objets étant en relecture, les surfaces publiques sont vides — c'est voulu, pas un défaut. | `scripts/build_index.py` |
| D20 | **Contrôles bloquants en intégration continue.** Champ obligatoire manquant, id ou slug dupliqué, `related` non résolu, source inconnue, sujet inconnu, fiche sans aucun sujet, volatilité inconnue : le build échoue. | `.github/workflows/validate.yml` |
| D21 | **Fraîcheur outillée.** `review_due` porte l'échéance de révision de chaque fiche. *Mécanisme et sanction révisés par D32 et D33.* | champ `review_due` |
| D28 | **Les quotas de forme sont indicatifs.** Aucun quota d'intertitres interrogatifs. `description` hors de la fenêtre 70-155 : avertissement. `description` absente : bloquant — c'est un fait manquant, pas un jugement de style. | `scripts/build_index.py` |
| D31 | **Le hub n'est pas dû.** Un sujet devient un hub à partir de 4 objets ; en dessous il reste une facette. Une fiche sans hub n'est pas une erreur : elle vit dans l'index général des sujets, au sitemap, dans `llms.txt` et dans les pages de situation. Ce qui reste bloquant est le fait : aucune fiche sans sujet, aucun sujet inconnu de la taxonomie. Un sujet qui atteint le seuil déclenche un avertissement de promotion. | `scripts/build_index.py`, `taxonomy/hubs.yaml` |
| D32 | **Une date ne bloque pas une chaîne de construction.** Avertissement à J−30, avertissement à l'échéance, retrait automatique en `review_required` pour les contenus volatils, erreur sur la seule fiche modifiée alors que sa révision est due. Jamais d'échec global. | `scripts/build_index.py`, `taxonomy/freshness.yaml` |
| D33 | **Champ `volatility` et date `verified_at`.** Quatre classes : `evergreen`, `annual`, `ecovadis-cycle`, `event-driven`. `review_due` en est dérivée. Une fiche ne vieillit plus au même rythme qu'une autre parce qu'une table le disait quelque part. | `taxonomy/freshness.yaml`, `schemas/knowledge-object.schema.json` |

## 9. Politique de robots

Décidée le 01/09/2026, appliquée par `public/robots.txt`, régénéré à chaque build.

| Robot | Décision | Motif |
|---|---|---|
| OAI-SearchBot, PerplexityBot, ClaudeBot | **Autorisé** | Ce sont les robots qui font apparaître le catalogue comme source dans les réponses. C'est l'objectif B de la vision. |
| Googlebot, Bingbot, Google-Extended | **Autorisé** | Recherche classique et alimentation des AI Overviews. Bing compte doublement : il alimente ChatGPT et Copilot. |
| GPTBot, CCBot, Applebot-Extended | **Autorisé** | Décision distincte de la recherche. Être présent dans les données d'entraînement sert la découvrabilité, et le contenu est une expertise publique qu'ESGIM veut voir attribuée. Réversible en une ligne. |
| Tout autre | **Autorisé** | Aucun blocage accidentel (KC-A06). |

## 10. Extension du catalogue

Nouvelle note → nouvelle fiche : suivre `README.md` § « Ajouter une connaissance ». Nouvelle valeur de taxonomie : l'ajouter d'abord à `taxonomy/taxonomy.yaml` (commit dédié), puis l'utiliser. Nouveau type d'objet (cas client, témoignage…) : définir sa plage d'IDs dans la taxonomie et son gabarit dans `schemas/`.
