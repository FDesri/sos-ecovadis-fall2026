#!/usr/bin/env python3
"""Faire passer une fiche de `status: review` à `status: published`.

Publier = valider humainement. Le script applique, sur les trois langues d'un
même objet (l'`id` est partagé) :
    status:      review  -> published
    reliability: *       -> expert-validated   (sauf --keep-reliability)
    date_updated:        -> date du jour
`version` n'est PAS incrémenté : publier n'est pas un changement de fond
(GOUVERNANCE §6). Régénérez ensuite les index : python3 scripts/build_index.py

Exemples
    python3 scripts/publish.py --list                 # ce qui attend en review
    python3 scripts/publish.py kb-0034               # une fiche (3 langues)
    python3 scripts/publish.py kb-0034 kb-0035       # plusieurs
    python3 scripts/publish.py --type faq            # tout un type
    python3 scripts/publish.py --all                 # tout ce qui est en review
    python3 scripts/publish.py kb-0001 --dry-run     # simulation
"""
import argparse, datetime, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")

def fiches():
    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not m:
                continue
            fm = m.group(1)
            def field(name):
                g = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
                return g.group(1).strip() if g else ""
            yield {"path": path, "rel": os.path.relpath(path, REPO), "text": text,
                   "fm": fm, "id": field("id"), "lang": field("lang"),
                   "type": field("type"), "status": field("status"),
                   "title": field("title").strip('"')}

def main():
    ap = argparse.ArgumentParser(description="review -> published")
    ap.add_argument("ids", nargs="*", help="identifiants kb-XXXX")
    ap.add_argument("--type", help="publier tout un type (article, faq, pricing…)")
    ap.add_argument("--all", action="store_true", help="publier tout ce qui est en review")
    ap.add_argument("--list", action="store_true", help="lister ce qui est en review")
    ap.add_argument("--keep-reliability", action="store_true",
                    help="ne pas passer reliability à expert-validated")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    items = list(fiches())
    if a.list:
        review = {}
        for it in items:
            if it["status"] == "review":
                review.setdefault(it["id"], {"type": it["type"], "langs": [], "title": ""})
                review[it["id"]]["langs"].append(it["lang"])
                if it["lang"] in ("fr", "mul"):
                    review[it["id"]]["title"] = it["title"]
        for oid in sorted(review):
            v = review[oid]
            print(f"{oid}  {v['type']:<8} [{','.join(sorted(v['langs']))}]  {v['title'][:70]}")
        print(f"\n{len(review)} objets en review ({sum(len(v['langs']) for v in review.values())} fichiers)")
        return

    if not (a.ids or a.type or a.all):
        ap.error("donnez des identifiants, --type, --all ou --list")

    targets = [it for it in items if it["status"] == "review" and (
        a.all or it["id"] in a.ids or (a.type and it["type"] == a.type))]
    if a.ids:
        unknown = set(a.ids) - {it["id"] for it in items}
        if unknown:
            print("Identifiants inconnus :", ", ".join(sorted(unknown)), file=sys.stderr); sys.exit(1)

    today = datetime.date.today().isoformat()
    for it in targets:
        new_fm = re.sub(r"^status:\s*review$", "status: published", it["fm"], flags=re.M)
        if not a.keep_reliability:
            new_fm = re.sub(r"^reliability:\s*.+$", "reliability: expert-validated", new_fm, flags=re.M)
        new_fm = re.sub(r"^date_updated:\s*.+$", f"date_updated: {today}", new_fm, flags=re.M)
        new_text = it["text"].replace(it["fm"], new_fm, 1)
        if a.dry_run:
            print("[dry-run]", it["rel"])
        else:
            open(it["path"], "w", encoding="utf-8").write(new_text)
            print("published", it["rel"])
    n_obj = len({it["id"] for it in targets})
    print(f"\n{n_obj} objets / {len(targets)} fichiers"
          + (" (simulation)" if a.dry_run else " publiés"))
    if targets and not a.dry_run:
        print("→ pensez à : python3 scripts/build_index.py && git commit && git push")

if __name__ == "__main__":
    main()
