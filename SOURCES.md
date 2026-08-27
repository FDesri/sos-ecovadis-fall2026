# SOURCES — Registre des sources du catalogue

Registre de traçabilité : chaque objet de connaissance (kb-XXXX) ← note source Evernote ← corpus propriétaire ESGIM.

## Corpus source

- **Origine unique :** corpus propriétaire ESGIM (notes Evernote de François Dequenne — rédactions personnelles et captures retravaillées, sans distinction de statut ; décision de gouvernance du 27/08/2026, voir GOVERNANCE.md §7).
- **Livraison :** export Evernote « Evernote notes sosecovadis repository v1.zip » (remis le 27/08/2026), 37 notes uniques après déduplication (les versions les plus récentes font foi). Les fichiers ENEX originaux restent dans l'Evernote / le Drive de François Dequenne.
- **Parsing :** `scripts/parse_enex.py` (ENEX → markdown).
- **Glossaire :** document projet Claude « glossaire-ecovadis-en-fr-nl.md » v2.0 — référence terminologique de toutes les traductions.
- **Codes questions :** « Exemple de questionnaire de réévaluation entreprise manufacturière taille S » (xlsx, projet) → `taxonomy/ecovadis-question-codes.json` (46 codes).

## Objets fondation (kb-0001 → kb-0005)

| ID | Type | Note source (Evernote) | Langue src | Fiche canonique |
|---|---|---|---|---|
| kb-0001 | pricing | EcoVadis ESGIM Princing.md | en | `how-much-does-ecovadis-support-cost` |
| kb-0002 | expert | Author identity (wout picture).md | fr | `francois-dequenne` |
| kb-0003 | service | EcoVadis ESGIM Princing.md | en | `full-ecovadis-support-mission` |
| kb-0004 | service | EcoVadis ESGIM Princing.md | en | `ecovadis-expert-advice-days` |
| kb-0005 | glossary | glossaire-ecovadis-en-fr-nl.md (projet) | mul | `glossaire-ecovadis-en-fr-nl` |

## Articles (kb-0010 → kb-0041)

| ID | Note source (Evernote) | Langue src | Fiche canonique (EN) | Remarques |
|---|---|---|---|---|
| kb-0010 | Committed Badge to Bronze.md | en | `from-committed-badge-to-bronze` | — |
| kb-0011 | Bronze to Silver.md | en | `from-bronze-to-silver` | — |
| kb-0012 | Silver to Gold.md | en | `from-silver-to-gold` | — |
| kb-0013 | Understanding the EcoVadis scorecard.md | en | `understanding-the-ecovadis-scorecard` | — |
| kb-0014 | EcoVadis scorecard How to read, share & maximise your rating.md | en | `read-share-maximise-your-ecovadis-scorecard` | — |
| kb-0015 | EcoVadis activated criteria by sector + FAQ.md | en | `ecovadis-activated-criteria-by-sector` | — |
| kb-0016 | EcoVadis’ rising standards in 2026.md | en | `ecovadis-rising-standards-2026` | — |
| kb-0017 | What's changing in 2026 + FAQ February.md | en | `whats-changing-in-2026` | — |
| kb-0018 | Methodology Updates Q2 2026.md | en | `ecovadis-methodology-updates-q2-2026` | — |
| kb-0019 | Évolution 2024  2025  2026 - Pourquoi est-ce plus difficile d'obtenir et de conserver une médaille de bronze.md | fr | `why-keeping-a-bronze-medal-is-harder` | chiffres seuils = estimations datées |
| kb-0020 | Évolution et dynamique de labellisation EcoVadis  Analyse prospective des seuils d'excellence et focus sur les marchés belges de l'emballage et de l'équipement pharmaceutique.md | fr | `ecovadis-thresholds-belgian-packaging-pharma` | benchmarks publics conservés ; estimations datées, à recouper avec kb-0016 |
| kb-0021 | EcoVadis drives stronger sustainability management.md | en | `why-ecovadis-strengthens-sustainability-management` | — |
| kb-0022 | EcoVadis essentials A guide for beginners and reassessed companies.md | en | `ecovadis-essentials-guide` | « 600+ » corrigé en « 100+ » |
| kb-0023 | Improve your EcoVadis score fast - Practical steps that work.md | en | `improve-your-ecovadis-score-fast` | cas clients anonymisés (à valider — cf. GOVERNANCE §7) |
| kb-0024 | How to build strong EcoVadis submissions consistently.md | en | `build-strong-ecovadis-submissions-consistently` | — |
| kb-0025 | Self-assessment vs. expert guidance - Which is right for you..md | en | `self-assessment-vs-expert-guidance` | — |
| kb-0026 | B Corp or EcoVadis, what's the best choice for your company.md | en | `b-corp-or-ecovadis` | — |
| kb-0027 | EcoVadis Sustain 2026 (light).md | en | `ecovadis-sustain-2026-takeaways` | sections prospection/personnes approchées retirées (repo public) |
| kb-0028 | Principaux conseils pratiques et tips.md | fr | `practical-ecovadis-tips` | — |
| kb-0029 | Quel type de documents justificatifs - EcoVadis - Entreprises XS.md | fr | `supporting-documents-for-xs-companies` | — |
| kb-0030 | Reporting indicateurs Environnement.md | fr | `environmental-indicators-to-collect` | — |
| kb-0031 | EcoVadis & GHG baseline Foundations & FAQ.md | en | `ecovadis-and-ghg-baseline` | « 600+ » corrigé en « 100+ » |
| kb-0032 | Risques environnementaux externes ENV7003 v2.md | fr | `external-climate-risk-assessment-env7003` | — |
| kb-0033 | Actions face aux perturbations environnementales externes - ENV7012.md | fr | `adapting-to-environmental-disruptions-env7012` | — |
| kb-0034 | Matières premières et produits chimiques - ENV3522.md | fr | `raw-materials-and-chemicals-env3522` | exemple client anonymisé (imprimeur flexo wallon S) |
| kb-0035 | Gestion des déchets - ENV3549.md | fr | `waste-management-env3549` | exemple client anonymisé (idem kb-0034) |
| kb-0036 | Reporting indicateurs Social et droits humains.md | fr | `social-hr-indicators-to-collect` | — |
| kb-0037 | Diversité  non-discrimination, Risque de corruption, prévention du travail des enfants  travail-forçé - Canevas.md | fr | `evidence-templates-diversity-corruption-child-labour` | — |
| kb-0038 | EcoVadis - Pack corruption - harcèlement - discrimination (Climacool).md | fr | `ethics-pack-corruption-harassment-discrimination` | nom du client retiré du titre et du contenu |
| kb-0039 | Achats Responsables - SUP307.md | fr | `sustainable-procurement-measures-sup307` | exemple client anonymisé (idem kb-0034) |
| kb-0040 | Sustainable procurement for mid-market companies Where to start.md | en | `sustainable-procurement-where-to-start` | — |
| kb-0041 | EcoVadis supplier engagement programmes From launch to lasting impact.md | en | `ecovadis-supplier-engagement-programmes` | — |

## FAQ (kb-0100 → kb-0167)

68 objets FAQ issus du découpage de trois notes source (une question humaine = un objet autonome ; doublons entre notes fusionnés) :

| Note source | Objets dérivés |
|---|---|
| FAQ 2025.md (webinaires ESG 2025) | kb-0100 → kb-0113 (kb-0100 fusionne aussi la règle « 55 par cycle » de FAQ 2026 (2)) |
| EcoVadis FAQ 2026 (1).md | kb-0114 → kb-0160 (« 600+ » de l'intro corrigé en « 100+ » ; liens externes nexioprojects remplacés par des slugs internes) |
| EcoVadis FAQ 2026 (2).md | kb-0161 → kb-0167 ; réponses redondantes fusionnées dans kb-0100, kb-0122, kb-0128, kb-0138, kb-0140, kb-0153, kb-0154, kb-0159 |

Le champ `source_note` du front matter de chaque fiche précise la ou les notes d'origine. La liste question par question est reconstructible depuis `scripts/faq_data_*.py` (fichiers de génération, champ `source_note`).

## Notes source non transformées

| Note | Raison |
|---|---|
| Author identity (wout picture).md | intégrée dans kb-0002 (fiche expert) |
| Risques environnementaux externes ENV7003 (v1) | remplacée par la v2 (kb-0032) |
| Doublons du ZIP (versions antérieures) | versions les plus récentes retenues |
