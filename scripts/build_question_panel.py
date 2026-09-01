#!/usr/bin/env python3
"""Construit le panel de questions de mesure de découvrabilité (KC-M01, KC-M02).

La grille demande 20 à 50 questions « formulées comme le feraient les clients »,
testées trois fois par moteur, avec relevé du taux de citation, du taux de
mention, de l'exactitude de la réponse et de l'exactitude de l'attribution.

Le catalogue contient déjà ces questions : chaque objet `faq` EST une question
humaine, et chaque titre d'article en est une aussi. Le panel est donc DÉRIVÉ
du catalogue, pas rédigé à côté — il ne peut pas diverger.

Sélection : 30 questions, priorité aux intentions commerciales (choisir,
comparer), puis couverture des trois situations S1/S2/S3 et étalement des
sujets. Les trois libellés linguistiques d'un même objet forment une question
du panel : c'est la même attente de réponse dans les trois langues.

Sorties :
  measurement/question-panel.md   lisible, pour lancer les tests à la main
  measurement/question-panel.csv  pour le relevé (une ligne par question × langue × moteur)

Usage:  python3 scripts/build_question_panel.py [--size 30]
"""
import argparse, csv, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "measurement")
ENGINES = ["ChatGPT Search", "Perplexity", "Google AI Overviews", "Claude (web search)"]
RUNS = 3

INTENT_PRIORITY = {"choisir": 0, "comparer": 1, "verifier": 2,
                   "mettre-en-oeuvre": 3, "comprendre": 4}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=30)
    args = ap.parse_args()

    cat = json.load(open(os.path.join(REPO, "index", "catalog.json"), encoding="utf-8"))
    # Seuls les objets dont le TITRE est une question posée par un humain.
    objs = [o for o in cat["objects"] if o["type"] in ("faq", "article", "pricing")
            and o["languages"].get("fr", {}).get("title", "").rstrip().endswith("?")]

    # tri : intention commerciale d'abord, puis étalement des sujets
    seen_topics, picked = {}, []
    for o in sorted(objs, key=lambda o: (INTENT_PRIORITY.get(o["intent"], 9), o["id"])):
        t = (o["topics"] or ["?"])[0]
        if seen_topics.get(t, 0) >= 3 and len(picked) > args.size // 2:
            continue
        seen_topics[t] = seen_topics.get(t, 0) + 1
        picked.append(o)
        if len(picked) >= args.size:
            break

    os.makedirs(OUT, exist_ok=True)

    md = [
        "# Panel de questions — mesure de la découvrabilité",
        "",
        f"{len(picked)} questions, dérivées du catalogue par "
        "`scripts/build_question_panel.py`. Ne pas éditer à la main : "
        "régénérer après toute évolution du catalogue.",
        "",
        "## Comment mesurer",
        "",
        f"Chaque question est posée **{RUNS} fois** à chacun des moteurs "
        f"({', '.join(ENGINES)}). Une seule exécution ne mesure rien : les réponses "
        "varient d'un appel à l'autre.",
        "",
        "Pour chaque exécution, relever :",
        "",
        "| Mesure | Ce qu'on note |",
        "|---|---|",
        "| Citation (KC-M03) | La réponse contient-elle un lien vers sos-ecovadis.com ? |",
        "| Mention (KC-M04) | ESGIM ou François Dequenne sont-ils nommés, même sans lien ? |",
        "| Exactitude réponse (KC-M05) | Chiffres, conditions, dates et limites sont-ils justes ? |",
        "| Exactitude attribution (KC-M06) | Le fait est-il attribué à la bonne fiche et à la bonne organisation ? |",
        "| Part de voix (KC-M07) | Quelles sources sont citées à notre place ? |",
        "| Fraîcheur (KC-M08) | Est-ce la version la plus récente de la donnée ? |",
        "",
        "**Un relevé de référence doit être fait AVANT la mise en ligne du site.** "
        "Sans point de départ, aucune progression ne sera démontrable.",
        "",
        "Cadence (KC-M12) : relevé de citation tous les deux mois, contrôle technique "
        "trimestriel, contrôle immédiat après toute migration ou changement de domaine.",
        "",
        "## Les questions",
        "",
    ]

    rows = []
    for i, o in enumerate(picked, 1):
        fr = o["languages"].get("fr") or list(o["languages"].values())[0]
        en = o["languages"].get("en") or fr
        nl = o["languages"].get("nl") or fr
        md += [
            f"### Q{i:02d} — {fr['title']}",
            "",
            f"- **EN** : {en['title']}",
            f"- **NL** : {nl['title']}",
            f"- Fiche attendue : `{o['id']}` · intention *{o['intent']}* · "
            f"situations {', '.join(o['situations']) or '—'} · sujets "
            f"{', '.join(o['topics']) or '—'}",
            f"- URL canonique attendue : "
            f"{fr['canonical_url'] or '(non publiée — pas encore d URL)'}",
            "",
        ]
        for lang, v in (("fr", fr), ("en", en), ("nl", nl)):
            for engine in ENGINES:
                for run in range(1, RUNS + 1):
                    rows.append({
                        "question_id": f"Q{i:02d}", "kb_id": o["id"], "lang": lang,
                        "question": v["title"], "engine": engine, "run": run,
                        "expected_url": v["canonical_url"] or "",
                        "cited": "", "mentioned": "", "answer_accurate": "",
                        "attribution_accurate": "", "competing_sources": "",
                        "freshness_ok": "", "date": "", "notes": "",
                    })

    open(os.path.join(OUT, "question-panel.md"), "w", encoding="utf-8").write("\n".join(md))
    with open(os.path.join(OUT, "question-panel.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    print(f"{len(picked)} questions × 3 langues × {len(ENGINES)} moteurs × {RUNS} exécutions "
          f"= {len(rows)} relevés à faire")
    print("écrit : measurement/question-panel.md, measurement/question-panel.csv")

if __name__ == "__main__":
    main()
