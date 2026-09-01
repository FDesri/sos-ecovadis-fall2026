# Panel de questions — mesure de la découvrabilité

30 questions, dérivées du catalogue par `scripts/build_question_panel.py`. Ne pas éditer à la main : régénérer après toute évolution du catalogue.

## Comment mesurer

Chaque question est posée **3 fois** à chacun des moteurs (ChatGPT Search, Perplexity, Google AI Overviews, Claude (web search)). Une seule exécution ne mesure rien : les réponses varient d'un appel à l'autre.

Pour chaque exécution, relever :

| Mesure | Ce qu'on note |
|---|---|
| Citation (KC-M03) | La réponse contient-elle un lien vers sos-ecovadis.com ? |
| Mention (KC-M04) | ESGIM ou François Dequenne sont-ils nommés, même sans lien ? |
| Exactitude réponse (KC-M05) | Chiffres, conditions, dates et limites sont-ils justes ? |
| Exactitude attribution (KC-M06) | Le fait est-il attribué à la bonne fiche et à la bonne organisation ? |
| Part de voix (KC-M07) | Quelles sources sont citées à notre place ? |
| Fraîcheur (KC-M08) | Est-ce la version la plus récente de la donnée ? |

**Un relevé de référence doit être fait AVANT la mise en ligne du site.** Sans point de départ, aucune progression ne sera démontrable.

Cadence (KC-M12) : relevé de citation tous les deux mois, contrôle technique trimestriel, contrôle immédiat après toute migration ou changement de domaine.

## Les questions

### Q01 — Combien coûte un accompagnement externe pour une (ré)évaluation EcoVadis ?

- **EN** : How much does it cost to get external help for an EcoVadis (re)assessment?
- **NL** : Wat kost externe begeleiding bij een EcoVadis-(her)beoordeling?
- Fiche attendue : `kb-0001` · intention *choisir* · situations S1, S2, S3 · sujets tarifs, timing
- URL canonique attendue : (non publiée — pas encore d URL)

### Q02 — Au-delà de la demande d'un grand compte, pourquoi se lancer dans EcoVadis ?

- **EN** : Beyond a key account's request, why embark on EcoVadis at all?
- **NL** : Waarom aan EcoVadis beginnen, los van de vraag van een grote klant?
- Fiche attendue : `kb-0021` · intention *choisir* · situations S1, S2, S3 · sujets methodologie, medailles-percentiles
- URL canonique attendue : (non publiée — pas encore d URL)

### Q03 — Le reporting VSME est-il nécessaire pour une entreprise déjà notée EcoVadis — et quel score peut-il débloquer ?

- **EN** : Is VSME reporting necessary for a company already rated by EcoVadis — and what score can it unlock?
- **NL** : Is VSME-rapportering nodig voor een onderneming die al een EcoVadis-score heeft — en welke score kan ze ontgrendelen?
- Fiche attendue : `kb-0104` · intention *choisir* · situations S1, S2, S3 · sujets vsme-csrd, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q04 — À quel niveau faut-il faire l'évaluation : filiale, holding ou groupe entier ?

- **EN** : At what entity level should the assessment be performed: subsidiary, holding or full group?
- **NL** : Op welk niveau voert u de beoordeling uit: dochteronderneming, holding of volledige groep?
- Fiche attendue : `kb-0115` · intention *choisir* · situations S3 · sujets questionnaire, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q05 — Quel score faut-il pour chaque médaille, et peut-on prédire la médaille avant soumission ?

- **EN** : What score is needed for each medal, and can medals be predicted before submission?
- **NL** : Welke score is nodig voor elke medaille, en kan de medaille vóór indiening worden voorspeld?
- Fiche attendue : `kb-0131` · intention *choisir* · situations S1, S2, S3 · sujets medailles-percentiles, rising-bar
- URL canonique attendue : (non publiée — pas encore d URL)

### Q06 — Quelles certifications sont réalistes par thème — faut-il toutes les normes ISO ?

- **EN** : Which certifications are realistically achievable per theme — do we need all ISO standards?
- **NL** : Welke certificaten zijn realistisch per thema — hebt u alle ISO-normen nodig?
- Fiche attendue : `kb-0141` · intention *choisir* · situations S1, S2, S3 · sujets methodologie, preuves
- URL canonique attendue : (non publiée — pas encore d URL)

### Q07 — Une fois la fiche d'évaluation reçue, où concentrer l'effort — et le plan d'action correctif suffit-il ?

- **EN** : Once we have our scorecard, where do we focus first — and is the Corrective Action Plan enough?
- **NL** : Waar focust u eerst zodra u uw scorecard hebt — en volstaat het corrigerend actieplan?
- Fiche attendue : `kb-0159` · intention *choisir* · situations S1, S2 · sujets methodologie, questionnaire
- URL canonique attendue : (non publiée — pas encore d URL)

### Q08 — Auto-évaluation ou accompagnement expert — que choisir pour votre parcours EcoVadis ?

- **EN** : Self-assessment or expert guidance — which is right for your EcoVadis journey?
- **NL** : Zelf doen of expertbegeleiding — wat past bij uw EcoVadis-traject?
- Fiche attendue : `kb-0025` · intention *comparer* · situations S3 · sujets methodologie, timing, tarifs
- URL canonique attendue : (non publiée — pas encore d URL)

### Q09 — B Corp ou EcoVadis : quel est le meilleur choix pour votre entreprise ?

- **EN** : B Corp or EcoVadis: what's the best choice for your company?
- **NL** : B Corp of EcoVadis: wat is de beste keuze voor uw onderneming?
- Fiche attendue : `kb-0026` · intention *comparer* · situations S3 · sujets methodologie, b-corp, timing
- URL canonique attendue : (non publiée — pas encore d URL)

### Q10 — Lequel vaut le plus : le SBTi ou l'adhésion au Pacte mondial ?

- **EN** : Which is more valuable: SBTi or UN Global Compact membership?
- **NL** : Wat is meer waard: SBTi of UN Global Compact-lidmaatschap?
- Fiche attendue : `kb-0145` · intention *comparer* · situations S1, S2, S3 · sujets carbone-ghg, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q11 — Faut-il soumettre des analyses de cycle de vie (ACV) pour bien scorer en gouvernance au CDP ?

- **EN** : Must companies submit life cycle assessments (LCAs) for good governance scoring on CDP?
- **NL** : Moet u levenscyclusanalyses (LCA's) indienen voor een goede governancescore bij CDP?
- Fiche attendue : `kb-0112` · intention *verifier* · situations S1, S2, S3 · sujets carbone-ghg, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q12 — Quelles sont les exigences de qualité et de validité des documents, et qu'est-ce qu'une politique solide ?

- **EN** : What are the quality and validity requirements for documents, and what makes a strong policy?
- **NL** : Wat zijn de kwaliteits- en geldigheidseisen voor documenten, en wat maakt een beleid sterk?
- Fiche attendue : `kb-0122` · intention *verifier* · situations S1, S2, S3 · sujets preuves, questionnaire, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q13 — Les documents au nom d'une maison mère ou d'une société sœur sont-ils acceptés ?

- **EN** : Is documentation issued in the name of a parent or sister company accepted?
- **NL** : Worden documenten op naam van een moeder- of zusterbedrijf aanvaard?
- Fiche attendue : `kb-0123` · intention *verifier* · situations S1, S2, S3 · sujets preuves, questionnaire
- URL canonique attendue : (non publiée — pas encore d URL)

### Q14 — Faut-il supprimer ou garder les documents rejetés automatiquement ?

- **EN** : Should automatically rejected documents be deleted or kept?
- **NL** : Moet u automatisch verworpen documenten verwijderen of bewaren?
- Fiche attendue : `kb-0124` · intention *verifier* · situations S1, S2, S3 · sujets preuves, plateforme
- URL canonique attendue : (non publiée — pas encore d URL)

### Q15 — Pourquoi une pièce KPI acceptée une année est-elle rejetée à la resoumission ?

- **EN** : Why was a KPI attachment accepted one year but rejected on resubmission?
- **NL** : Waarom werd een KPI-bijlage het ene jaar aanvaard en bij herindiening verworpen?
- Fiche attendue : `kb-0125` · intention *verifier* · situations S1, S2 · sujets preuves, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q16 — Quel type de preuve démontre le mieux la mise en œuvre réelle, au-delà des politiques sur papier ?

- **EN** : What type of evidence best demonstrates actual implementation, versus just having policies on paper?
- **NL** : Welk type bewijs toont werkelijke uitvoering het best aan, voorbij beleid op papier?
- Fiche attendue : `kb-0126` · intention *verifier* · situations S1, S2, S3 · sujets preuves, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q17 — Les exigences de qualité documentaire se sont-elles durcies par rapport aux cycles précédents ?

- **EN** : Have documentation quality expectations become more stringent compared to previous cycles?
- **NL** : Zijn de kwaliteitseisen voor documentatie strenger geworden dan in vorige cycli?
- Fiche attendue : `kb-0129` · intention *verifier* · situations S1, S2, S3 · sujets rising-bar, preuves, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q18 — Qu'est-ce qui distingue les preuves d'un score de base de celles qui mènent au Bronze, à l'Argent, à l'Or ou au Platine ?

- **EN** : What distinguishes evidence for a basic score from evidence that drives Bronze, Silver, Gold or Platinum?
- **NL** : Wat onderscheidt bewijs voor een basisscore van bewijs dat naar Brons, Zilver, Goud of Platinum leidt?
- Fiche attendue : `kb-0132` · intention *verifier* · situations S1, S2 · sujets medailles-percentiles, preuves
- URL canonique attendue : (non publiée — pas encore d URL)

### Q19 — Nous avons eu 75 en Reporting sans rapport public — retomberons-nous à 50 la prochaine fois ?

- **EN** : We scored 75 in Reporting without a public report — will it drop to 50 next time?
- **NL** : We haalden 75 op Rapportering zonder publiek rapport — zakken we volgende keer naar 50?
- Fiche attendue : `kb-0139` · intention *verifier* · situations S1, S2 · sujets rising-bar, vsme-csrd, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q20 — Comment EcoVadis évalue-t-il les objectifs climatiques science-based non validés par le SBTi ?

- **EN** : How does EcoVadis evaluate science-based climate targets not formally validated by SBTi?
- **NL** : Hoe beoordeelt EcoVadis science-based klimaatdoelen die niet formeel door SBTi zijn gevalideerd?
- Fiche attendue : `kb-0146` · intention *verifier* · situations S1, S2, S3 · sujets carbone-ghg, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q21 — Que signifie réellement « conforme aux standards de reporting » — le GRI « with reference » suffit-il ?

- **EN** : What does "complies with reporting standards" actually require — is GRI "with reference" enough?
- **NL** : Wat vereist "conform de rapporteringsstandaarden" werkelijk — volstaat GRI "with reference"?
- Fiche attendue : `kb-0149` · intention *verifier* · situations S1, S2, S3 · sujets vsme-csrd, rising-bar, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q22 — Notre rapport RSE annuel n'est pas audité par un organisme accrédité — est-ce un frein au score ?

- **EN** : Our annual CSR report is not audited by an accredited body — is that a barrier to improving the score?
- **NL** : Ons jaarlijks MVO-rapport is niet geauditeerd door een geaccrediteerde instantie — is dat een rem op de score?
- Fiche attendue : `kb-0150` · intention *verifier* · situations S1, S2, S3 · sujets vsme-csrd, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q23 — La méthode ADEME « Act pas à pas » est-elle reconnue par EcoVadis ?

- **EN** : Is the ADEME "Act pas à pas" method recognised by EcoVadis?
- **NL** : Wordt de ADEME-methode "Act pas à pas" erkend door EcoVadis?
- Fiche attendue : `kb-0156` · intention *verifier* · situations S1, S2, S3 · sujets environnement, methodologie
- URL canonique attendue : (non publiée — pas encore d URL)

### Q24 — Comment passer du badge Committed à la médaille Bronze EcoVadis ?

- **EN** : How do you move from the EcoVadis Committed badge to a Bronze medal?
- **NL** : Hoe gaat u van de EcoVadis Committed Badge naar een Bronzen medaille?
- Fiche attendue : `kb-0010` · intention *mettre-en-oeuvre* · situations S3 · sujets medailles-percentiles, rising-bar, methodologie, ethique
- URL canonique attendue : (non publiée — pas encore d URL)

### Q25 — Quels sont les principaux conseils pratiques pour réussir son évaluation EcoVadis ?

- **EN** : What are the main practical tips for a successful EcoVadis assessment?
- **NL** : Wat zijn de belangrijkste praktische tips voor een geslaagde EcoVadis-beoordeling?
- Fiche attendue : `kb-0028` · intention *mettre-en-oeuvre* · situations S1, S2, S3 · sujets questionnaire, preuves, timing, methodologie, 360-watch
- URL canonique attendue : (non publiée — pas encore d URL)

### Q26 — Quelles sont les données environnementales à récolter pour EcoVadis ?

- **EN** : Which environmental data do you need to collect for EcoVadis?
- **NL** : Welke milieugegevens moet u verzamelen voor EcoVadis?
- Fiche attendue : `kb-0030` · intention *mettre-en-oeuvre* · situations S1, S2 · sujets environnement, preuves, questionnaire
- URL canonique attendue : (non publiée — pas encore d URL)

### Q27 — Quelles sont les données ressources humaines à récolter pour EcoVadis ?

- **EN** : Which HR and social data do you need to collect for EcoVadis?
- **NL** : Welke HR- en sociale gegevens moet u verzamelen voor EcoVadis?
- Fiche attendue : `kb-0036` · intention *mettre-en-oeuvre* · situations S1, S2 · sujets social-droits-humains, preuves, questionnaire
- URL canonique attendue : (non publiée — pas encore d URL)

### Q28 — Achats Responsables pour les entreprises de taille intermédiaire : par où commencer ?

- **EN** : Sustainable procurement for mid-market companies: where to start
- **NL** : Duurzame Inkoop voor middelgrote ondernemingen: waar beginnen?
- Fiche attendue : `kb-0040` · intention *mettre-en-oeuvre* · situations S1, S2 · sujets achats-responsables, methodologie, vsme-csrd, carbone-ghg
- URL canonique attendue : (non publiée — pas encore d URL)

### Q29 — Comment fonctionne la limite de 55 documents — et faut-il regrouper des documents en un seul ?

- **EN** : How does the 55-document limit work — and should we combine documents into one?
- **NL** : Hoe werkt de limiet van 55 documenten — en moet u documenten bundelen in één bestand?
- Fiche attendue : `kb-0100` · intention *mettre-en-oeuvre* · situations S1, S2, S3 · sujets questionnaire, preuves, plateforme
- URL canonique attendue : (non publiée — pas encore d URL)

### Q30 — Comment motiver les équipes achats à intégrer la durabilité dans leurs processus ?

- **EN** : How can procurement teams be motivated to integrate sustainability into their processes?
- **NL** : Hoe motiveert u inkoopteams om duurzaamheid in hun processen te integreren?
- Fiche attendue : `kb-0102` · intention *mettre-en-oeuvre* · situations S1, S2, S3 · sujets achats-responsables
- URL canonique attendue : (non publiée — pas encore d URL)
