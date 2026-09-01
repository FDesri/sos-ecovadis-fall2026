# SOS-EcoVadis — Project Vision & Decisions (v1.2, 2026-09-01)

Statut : vision et décisions techniques D1–D21 actées. **Une nouvelle session doit lire ce fichier en entier avant d'agir ; rien ici ne demande à François de re-expliquer quoi que ce soit.**

**Change log v1.1 → v1.2.** Application des 95 contrôles de la grille « LLM-ready pour un Knowledge Catalogue publié sur GitHub » (fournie par François le 01/09/2026). Neuf décisions nouvelles (D13–D21). Le plan d'URL §5.1 est étendu de un à sept types d'objets — c'est le changement le plus lourd de conséquences. Le modèle de fiche §6 passe en v2. Une section §14 suit la conformité contrôle par contrôle. Le catalogue est passé en v2.0.0 (tag Git).

---

## 0. En un paragraphe

François Dequenne (co-fondateur d'ESGIM, ESG Interim Management, esgim.eu, Bruxelles) a transformé ~50 notes Evernote d'expertise EcoVadis en un **Knowledge Catalogue de 106 objets trilingues (EN-FR-NL), gouverné et versionné**, hébergé dans le dépôt public `FDesri/sos-ecovadis-knowledge-catalogue`. Le projet construit sur **sos-ecovadis.com** (1) la publication HTML de ce catalogue, conçue pour être trouvée et citée par les moteurs et les agents, et (2) **une landing page trilingue** présentant trois situations d'entreprise, chacune ouvrant une sous-page, toutes menant à un seul appel à l'action : réserver et prépayer un appel de découverte de 30 minutes (125 € HTVA) via le Calendly existant. Site statique (Eleventy) sur Netlify, identité ESGIM, suivi HubSpot Starter. **À ce jour le catalogue existe et est conforme au fond ; il n'est publié nulle part en HTML — c'est l'objet des étapes 1 à 5.**

---

## 1. Acteurs et actifs (faits)

| Élément | Valeur |
|---|---|
| Éditeur | **IMAGINATION@WORK SRL** — BCE et TVA 0774.373.269, Boulevard du Souverain 24 (chez Buzzy Nest), 1170 Watermael-Boitsfort, représentée par François Dequenne, administrateur. [esgim.eu/legal](https://esgim.eu/legal). **ESG INTERIM MANAGEMENT (ESGIM) est une marque** déposée auprès de l'Office Benelux de la Propriété Intellectuelle par cette société. |
| Auteur | François Dequenne. Contact site et expéditeur HubSpot : fd@esgim.eu. |
| Site hub (existant, agence, Nuxt.js) | https://esgim.eu — référence externe seulement. « Qui sommes-nous » pointe vers la page À propos d'esgim.eu. Aucun changement sur esgim.eu, aucune demande à l'agence. |
| Domaine de campagne | sos-ecovadis.com — enregistré chez one.com, DNS sous contrôle de François. Pas d'adresse e-mail (pas de MX). |
| Réservation | https://calendly.com/francois-dequenne/30min — Calendly Standard, Stripe, intégrations HubSpot et Zoom opérationnelles. 30 min, 125 € HTVA, prépayé. |
| CRM | HubSpot **Marketing Hub Starter**, portail **9391878**. |
| Netlify | Équipe « Sotrelco », slug `francois-dequenne`, plan Free, François Owner. |
| Supabase | Projet `etemxbhitvblzgzaalvg` (eu-central-1), en pause. Hors MVP. |
| Google Drive | Dossier de relecture `sos_ecovadis_fall2026`. |
| **Dépôt GitHub** | **`FDesri/sos-ecovadis-knowledge-catalogue` — PUBLIC.** 106 objets, 316 fichiers, branche `main`, tag `v2.0.0`. Écart assumé avec D2 (qui prévoyait un dépôt privé) : un catalogue privé ne peut être cité par personne. Renommé le 01/09 (D16). |
| Licence | Contenu **CC BY-NC 4.0**, code **MIT** (D15). |
| Apify | Connecté ; optionnel (mesure de citation, plus tard). |

---

## 2. Objectifs (les deux à la fois)

**A. Conversion (primaire, portée par les campagnes).** Les campagnes e-mail HubSpot envoient les prospects vers la sous-page de situation qui correspond à leur propriété HubSpot. La page décrit la situation et la solution, et mène à l'appel payant de 30 minutes. Objectif au-delà de l'appel : une mission de conseil de plusieurs jours. Le prix existe parce que « ce qui est gratuit n'a pas de valeur ». François possède la logique commerciale ; ne pas la redessiner.

**B. Découvrabilité (structurelle, long terme).** Être la *source* que les moteurs et les LLM trouvent et citent. Être cité a de la valeur même sans clic.

**Critère de mise en ligne (grille LLM-ready).** Le catalogue peut être dit « LLM-ready » quand : tous les contrôles P0 sont conformes ; au moins 80 % des P1 le sont sur les pages stratégiques ; chaque question prioritaire a une réponse canonique ; le panel de test IA et la mesure de trafic tournent ; aucune information critique n'est enfermée dans un PDF, une image ou du JavaScript. **Trois de ces cinq conditions sont remplies ; les deux autres dépendent de la publication HTML.**

---

## 3. Les trois situations (fixes, IDs permanents)

| ID | Situation | Notes |
|---|---|---|
| **S1** | Montée en médaille | Surtout Bronze visant l'Argent ; aussi badge Committed/Fast Mover → Bronze. |
| **S2** | Rétrogradation | Surtout Bronze retombé en badge ; aussi Argent → Bronze. |
| **S3** | Première évaluation exigée par un donneur d'ordres | PME sous pression du service achats d'un client. |
| A1 (phase 2) | Service achats grand compte (côté acheteur) | Audience distincte, page propre plus tard. Ne jamais confondre avec S3. |

S1–S3 sont utilisés à l'identique dans : la propriété HubSpot, la configuration d'URL, le front matter (`situations[]`), les UTM (`utm_content`), les noms de CTA HubSpot.

---

## 4. Hors périmètre du MVP

Pas d'assistant conversationnel, pas de RAG, pas d'embeddings, pas de Supabase dans le chemin critique. Pas de landing par situation (une landing, trois sous-pages). Pas de traduction simultanée forcée. Pas de formulaire HubSpot ni d'aimant à prospects gratuit. Pas de widget Calendly embarqué. Pas d'autre domaine. **Pas de publication sans relecture humaine** (D19 l'outille désormais). Aucun changement sur esgim.eu.

---

## 5. Architecture du site

### 5.1 Plan d'URL — **REMPLACE la version v1.1** (Décision D13)

La v1.1 ne logeait qu'un type d'objet, l'article. Le catalogue en compte sept et 106 objets, dont **68 FAQ** qui n'avaient aucune place dans le plan. Or le contrôle KC-C01 exige une URL stable par unité de connaissance. Les branches d'articles fixées en v1.1 sont **conservées telles quelles** : la v1.2 ajoute, elle ne contredit pas.

**La source unique du plan d'URL est `taxonomy/url-plan.yaml`.** `canonical_url` n'est pas un champ de front matter : il en est dérivé au build. Aucune dérive n'est possible.

```
sos-ecovadis.com/                    → 301 vers /fr/
www.sos-ecovadis.com/*               → 301 vers l'apex (canonique)

/fr/                                 landing
/fr/monter/  /fr/retrograde/  /fr/premiere-evaluation/     pages S1 / S2 / S3

/fr/savoir/<slug>/        article     (v1.1, inchangé)   /nl/kennis/     /en/knowledge/
/fr/questions/<slug>/     faq                            /nl/vragen/     /en/questions/
/fr/services/<slug>/      service                        /nl/diensten/   /en/services/
/fr/tarifs/<slug>/        pricing                        /nl/tarieven/   /en/pricing/
/fr/experts/<slug>/       expert                         /nl/experts/    /en/experts/
/fr/sujets/<slug>/        hub thématique                 /nl/onderwerpen/ /en/topics/
/fr/glossaire/            glossaire (page unique trilingue ; /nl/ et /en/ redirigent)
/fr/a-propos/             identité ESGIM                 /nl/over-ons/   /en/about/

/robots.txt  /sitemap.xml  /llms.txt  /llms-full.txt  /catalog.json  /feed.xml
```

**D13b — les hubs de situation n'existent pas.** Les pages S1/S2/S3 de la landing en font office : leur bloc « Pour aller plus loin » liste les fiches de la situation. Deux pages concurrentes par situation créeraient exactement la cannibalisation que KC-S08 interdit.

Règles : minuscules, tirets, slash final, pas de date dans l'URL. Les IDs S1–S3 et kb-XXXX n'apparaissent jamais dans une URL. Un slug publié ne change jamais : on redirige. **Les URL raw GitHub ne sont jamais canoniques.**

### 5.2 Landing `/fr/`
Hero (titre, sous-titre, CTA `SOS_FR_HERO_BOOK`) → trois cartes de situation → preuve et « Qui sommes-nous » (lien esgim.eu) → CTA → pied de page.

### 5.3 Sous-page de situation
Title et description propres, titre spécifique, la situation, la solution, ce que l'appel de 30 min apporte, CTA (`SOS_FR_S1_BOOK`…), **« Pour aller plus loin » alimenté par les fiches de la situation**, pied de page.

### 5.4 Page de fiche
H1 → bloc « En bref » (réponse d'abord) → sections structurées, **au moins 30 % d'intertitres interrogatifs** → FAQ → encadré auteur (François Dequenne, photo, bio, LinkedIn, lien esgim.eu) → **auteur, date de dernière révision et version VISIBLES** (KC-C13) → bloc « Votre situation » (liens S1/S2/S3 + CTA) → sources → pied de page.

### 5.5 Couche machine
Générée par `scripts/build_index.py`, jamais éditée à la main : `robots.txt` (politique explicite, GOVERNANCE §9), `sitemap.xml`, `llms.txt` (hubs d'abord, puis fiches), `llms-full.txt`, `catalog.json`, JSON-LD schema.org (Organization, Person, Article, FAQPage), hreflang + `x-default`, canonical, Open Graph.

### 5.6 Look & feel et qualité
Identité ESGIM via `esgim-design`. Construit avec `html-landing-netlify-hubspot`. Pages légales dédiées, adaptées d'esgim.eu.

---

## 6. Modèle de contenu — front matter v2

Source de vérité : le dépôt GitHub. Evernote = capture. Drive = bureau de relecture.

**Une note = un sujet = un objet.** Sept types : `article`, `faq`, `pricing`, `service`, `expert`, `glossary`, `organization`.

Champs obligatoires : `id`, `type`, `lang`, `title`, `slug`, `summary`, **`description`** (70–155 caractères, résume la réponse — KC-T02), **`intent`** (`comprendre` | `comparer` | `choisir` | `mettre-en-oeuvre` | `verifier` — KC-S03), `author`, `source`, `date_created`, `date_updated`, **`review_due`** (calculée depuis `date_updated` selon les cadences GOVERNANCE §3 — KC-M12), `version`, `status`.

Champs ajoutés non obligatoires : **`sources`** (ids de `taxonomy/sources-registry.yaml` — le build refuse un id inconnu) et **`relations`** (`alternatives`, `prerequisites` ; `parent` et `children` sont dérivés des hubs).

Facettes : `situations`, `sizes`, `content_kind`, `themes`, `topics`, `ecovadis_questions`, `keywords`, `audience`.

**Hubs (D18).** Un seul axe : le sujet. Les quatre thèmes officiels EcoVadis y figurent sous leur nom officiel. Un sujet devient un hub à partir de 4 objets — 16 hubs aujourd'hui, **0 objet orphelin sur 106**. Les hubs sont générés depuis `taxonomy/hubs.yaml`, pas rédigés en double.

**Néerlandais = flamand**, toujours (kmo, VTE, rapportering, FOD, Unia, vouvoiement « u »). Le NL se traduit depuis l'anglais ou depuis le concept, jamais depuis le français. Le glossaire prime.

---

## 7. Boucle de rédaction (Claude dans la boucle)

1. François ajoute l'en-tête standard à la note Evernote et l'exporte en `.enex`.
2. Il la dépose dans une conversation du projet Claude, ou dans Drive `01_inbox_enex`.
3. Claude convertit, rédige la fiche dans les trois langues, remplit le front matter v2, met à jour `SOURCES.md` et les index, puis crée un Google Doc de relecture.
4. François relit, puis écrit **« approved »** ou **« approved with changes »**.
5. Claude passe la fiche en `published` (`scripts/publish.py`), régénère les index, committe.
6. Netlify reconstruit sur push : sitemap, `llms.txt`, RSS se régénèrent seuls.

**Le build refuse** (D20) : champ obligatoire manquant, `description` hors fenêtre, id ou slug dupliqué, `related` non résolu, source inconnue du registre, parité de langues rompue, objet sans hub, fiche publiée dont la révision est due.

---

## 8. Conversion et mesure

**Conversion (inchangé v1.1).** E1 clic CTA → E2 page Calendly atteinte (UTM) → **E3 réservation payée (conversion web primaire)** → E4 présence / absence → E5 deal de conseil. HubSpot Starter, CTA nommés par contexte, propagation d'UTM jusqu'à Calendly.

**Découvrabilité — couche séparée, à brancher EN PREMIER.** Google Search Console et Bing Webmaster Tools sur le domaine. Et surtout : **`measurement/question-panel`** — 30 vraies questions clients dérivées du catalogue lui-même, × 3 langues × 4 moteurs × 3 exécutions = 1080 relevés. On note le taux de citation, le taux de mention, l'exactitude de la réponse, l'exactitude de l'attribution, la part de voix et la fraîcheur.

**Le relevé de référence se fait AVANT la mise en ligne.** Sans point de départ, aucune progression ne sera démontrable. C'est la seule étape de la grille qu'on ne peut pas rattraper après coup.

---

## 9. Journal des décisions techniques

D1–D12 : inchangées depuis la v1.1, sauf D1 (voir D13) et D2 (dépôt public, voir §1).

| # | Décision | Pourquoi | Réversibilité |
|---|---|---|---|
| **D13** | **Plan d'URL étendu aux sept types d'objets** ; branches d'articles v1.1 conservées ; source unique `taxonomy/url-plan.yaml` ; les pages S1/S2/S3 font office de hub de situation | KC-C01 exige une URL par unité de connaissance : 106, pas 32. Les 68 FAQ n'avaient nulle part où vivre | **Difficile** une fois indexé — c'est pourquoi elle est prise avant publication |
| **D14** | **Liens sortants vers référentiels, régulateurs et institutions publiques autorisés** ; concurrents toujours interdits. Révise la décision de gouvernance n° 6 du 27/08 | 93 articles sur 96 n'avaient aucune source alors qu'ils avançaient des chiffres datés. EcoVadis et la Commission ne sont pas des concurrents d'ESGIM : citer sa source prouve qu'on sait de quoi on parle | Facile |
| **D15** | **Licence : contenu CC BY-NC 4.0, code MIT.** Pas de clause « pas de modification » | Sans licence, le droit d'auteur par défaut s'applique et personne ne sait s'il peut citer. La clause ND ferait douter du droit de résumer — précisément l'usage recherché | **Sens unique** : on assouplit, on ne resserre pas ce qui a circulé |
| **D16** | **Renommer le dépôt** `sos-ecovadis-knowledge-catalogue` → `sos-ecovadis-knowledge-catalogue` | « fall2026 » date un actif permanent | Facile aujourd'hui, coûteux après le premier lien externe |
| **D17** | **Facette d'intention** sur chaque objet + **fiche d'identité de l'organisation** (kb-0006) | KC-S03 et KC-S12. Un catalogue sans page d'identité n'est pas rattachable à une entité | Facile |
| **D18** | **Hubs sur un axe unique, le sujet** ; seuil de 4 objets ; générés, pas rédigés | KC-S09 et KC-T07. Un hub « thème » et un hub « sujet » sur le même contenu, c'est la cannibalisation que KC-S08 interdit | Facile |
| **D19** | **Rien d'indexable hors `status: published`** : URL canonique, sitemap et `llms.txt` réservés aux fiches publiées | KC-G17. Les 106 objets sont en relecture : les surfaces publiques sont donc vides. C'est voulu, et cela se remplit à mesure des « approved » | Facile |
| **D20** | **Contrôles bloquants en intégration continue** | KC-G15. Une validation qu'on lance quand on y pense n'est pas une validation | Facile |
| **D21** | **Fraîcheur outillée** : `review_due` par fiche, et une fiche publiée en retard fait échouer le build | KC-M12. Le §3 de la gouvernance cesse d'être une intention | Facile |

**Décision de robots (GOVERNANCE §9).** OAI-SearchBot, PerplexityBot, ClaudeBot, Googlebot, Bingbot, Google-Extended : autorisés — ce sont eux qui font apparaître le catalogue comme source. GPTBot, CCBot, Applebot-Extended (entraînement) : **autorisés aussi**, décision distincte de la recherche, motivée par l'objectif de découvrabilité, réversible en une ligne.

---

## 10. Ce que François doit faire lui-même

**GitHub — fait le 01/09/2026**, sauf les topics (KC-G04, voir ci-dessous). L'API GitHub n'est pas accessible depuis les sessions Claude : ces trois champs se règlent dans l'UI du dépôt, bouton « Edit » à droite de « About ».

- **Description** : `Base de connaissances trilingue (EN-FR-NL) sur la notation EcoVadis pour les TPE et PME belges : méthode, preuves, médailles, coûts. Publiée par ESG Interim Management.`
- **Website** : `https://sos-ecovadis.com`
- **Topics** (12) : `ecovadis` · `esg` · `sustainability` · `csr` · `sme` · `belgium` · `knowledge-base` · `sustainable-procurement` · `vsme` · `csrd` · `llms-txt` · `trilingual`
- ~~**Renommer** le dépôt~~ — fait. `FDesri/sos-ecovadis-knowledge-catalogue`. GitHub maintient les redirections depuis l'ancien nom ; toutes les références internes ont été mises à jour.
- **Topics : toujours vides.** Le champ se remplit dans le même panneau « About » que la description. Les 12 valeurs sont ci-dessus.

**Jeton d'accès.** Pour que Claude puisse pousser, le PAT fine-grained a besoin de **Contents : Read and write** et, pour les fichiers `.github/workflows/`, de **Workflows : Read and write**.

~~**Identifiants légaux**~~ — **reçus le 01/09/2026.** kb-0006 porte désormais la distinction marque / personne morale, et le JSON-LD expose `legalName`, `vatID` et l'adresse postale. Numéro d'entreprise 0774.373.269, TVA BE0774.373.269 — confirmés par François le 01/09/2026.

**Lien depuis esgim.eu (KC-E01).** Reporté à l'étape de mise en ligne HTML, décidé le 01/09/2026 : le lien pointera vers le domaine, pas vers le dépôt.

**Plus tard, à l'étape correspondante :** HubSpot (propriété de situation, bandeau de consentement, 5 CTA, sync Calendly), Netlify (site depuis le dépôt, domaine, DNS), one.com (serveurs de noms), Search Console et Bing.

---

## 11. Ce qu'il manque encore

Photo de l'auteur (carrée, ≥ 800 px) ; bio de 2 lignes FR (NL/EN ensuite) ; URL LinkedIn ; URL de la page À propos d'esgim.eu ; nom et valeurs de la propriété de situation HubSpot.

~~Identifiants légaux~~ — **fournis le 01/09/2026**, kb-0006 est complétée et passée en relecture.

---

## 12. Plan de construction — état au 01/09/2026

| Étape | Livrable | État |
|---|---|---|
| **0 — Fondations** | Vision, dossiers Drive, guide Evernote, taxonomie | ✅ fait |
| **0b — Catalogue** | 106 objets trilingues, gouvernance, index machine | ✅ fait (v1.0.0, 27/08) |
| **0c — Conformité LLM-ready** | Front matter v2, intertitres interrogatifs, sources, hubs, licence, CI, panel de mesure | ✅ **fait (v2.0.0, 01/09)** |
| **0d — Relecture** | François valide les fiches → `status: published` | ⏳ **conversation dédiée, au signal de François.** Rien n'est publiable avant |
| **M — Mesure de référence** | Search Console, Bing, 1080 relevés du panel | ⏳ **à faire AVANT la mise en ligne** |
| **1 — Preuve de pipeline** | Squelette Eleventy, `netlify.toml`, une page déployée | ⏳ |
| **2 — Coquille de la landing** | `/fr/`, pages légales, HubSpot, design ESGIM | ⏳ |
| **Brainstorm pitch** | Titres et argumentaires S1/S2/S3, slugs définitifs | ⏳ |
| **3 — Pages de situation et CTA** | 3 sous-pages, CTA HubSpot, UTM validés jusqu'à Calendly | ⏳ |
| **4 — Publication des fiches** | Gabarit de fiche, JSON-LD, hubs, sitemap, `llms.txt` servis | ⏳ |
| **5 — Mise en ligne** | Domaine, HTTPS, redirections, Search Console, test e-mail bout en bout | ⏳ |
| **6 — Remplissage** | Fiches suivantes par lots ; NL et EN progressivement | ⏳ |

**L'étape suivante est 0d ou M, pas 1.** La relecture débloque tout le reste ; la mesure de référence est la seule chose qu'on ne peut plus faire après la mise en ligne.

---

## 13. Hygiène de conversation

Une conversation par étape, nommée `SOS-EcoVadis — Étape N`, commençant par « lis la vision v1.2 dans les fichiers du projet, nous sommes à l'étape N ». Mettre à jour ce fichier (nouvelle version) dès qu'une décision change.

---

## 14. Conformité à la grille LLM-ready

Audit initial : `claude/audit-llm-ready-catalogue-v1.md`. État après le travail du 01/09.

| Section | Avant | Après | Ce qui reste |
|---|---|---|---|
| **P0 — bloquants** (10) | 2 | 2 conformes, **6 prêts** | Tout dépend de la publication HTML. `robots.txt` est écrit et motivé, il n'est pas encore servi |
| **KC-C — extractibilité** (16) | 10 | **14** | C12 (fait vs analyse) et C13 (auteur/date visibles dans la page) relèvent du gabarit HTML |
| **KC-T — métadonnées** (12) | 2 | **9** | T10 (HTML sémantique) et T12 (404) n'ont pas d'objet sans site |
| **KC-S — couverture** (14) | 9 | **13** | S12 conforme depuis le 01/09 ; S14 (cohérence catalogue/réalité) reste une vérification de François |
| **KC-G — dépôt** (17) | 6 | **14** | G02/G03/G04 = 3 minutes dans l'UI GitHub ; G15 attend le scope Workflows du jeton |
| **KC-E — autorité** (8) | 0 | 1 | E01, le lien depuis esgim.eu, est le prochain geste utile |
| **KC-L — llms.txt** (6) | 2 | **6 prêts** | Générés ; se remplissent quand des fiches passent en `published` |
| **KC-M — mesure** (12) | 0 | **1** | Le panel existe ; les 1080 relevés restent à faire |

**Ce que la grille ne remet pas en cause.** Elle recommande GitHub Pages ; la vision retient Eleventy sur Netlify. Les deux satisfont KC-A02 et KC-A03 de la même façon, et Netlify fait mieux ce dont ce projet a besoin : en-têtes de sécurité, redirections, liste CSP pour HubSpot et Calendly. **Garder Netlify** — la prescription GitHub Pages est un moyen, pas un objectif.

**Chiffres de référence, avant → après.**

| Mesure | Avant | Après |
|---|---|---|
| Intertitres interrogatifs (articles) | 9 / 639 = 1 % | **447 / 639 = 70 %** |
| Articles portant une référence liée | 3 / 96 | **96 / 96** |
| Fiches avec `description` de 70–155 car. | 0 / 313 | **316 / 316** |
| Objets cités par aucun autre | 70 / 105 | **0 / 106** |
| Fiches avec `sources` renseignées | 0 | **316 / 316**, 0 id inconnu |
| Fichiers manquants au dépôt | LICENSE, CITATION.cff, CHANGELOG, CONTRIBUTING, CI, sitemap, JSON-LD, llms-full | **tous présents** |
| Releases taguées | 0 | **v2.0.0** |
