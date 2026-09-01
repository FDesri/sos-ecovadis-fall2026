#!/usr/bin/env python3
"""Réécrit les intertitres H2 des articles sous forme interrogative (KC-C05).

La grille LLM-ready vise au moins 30 % de H2 formulés comme des questions :
c'est ainsi qu'un moteur ou un agent isole la section qui répond à la
question posée. Le catalogue était à 1 % (9 H2 sur 639).

Entrée : un JSON {kb-XXXX: {lang: [nouveaux H2 dans l'ordre]}}. Le
remplacement est POSITIONNEL : le script refuse un objet dont le nombre de
H2 fournis ne correspond pas au nombre de H2 du fichier, dans chaque langue.
Rien d'autre que la ligne `## ` n'est touché : le corps reste intact.

Usage:
  python3 scripts/rewrite_headings.py <fichier.json> [--dry-run]
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")

def index_articles():
    import yaml
    idx = {}
    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
            fm = yaml.safe_load(m.group(1))
            if fm.get("type") != "article":
                continue
            idx.setdefault(fm["id"], {})[fm["lang"]] = path
    return idx

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mapping = json.load(open(sys.argv[1], encoding="utf-8"))
    dry = "--dry-run" in sys.argv
    idx = index_articles()

    errors, touched, converted, total = [], 0, 0, 0
    for oid, per_lang in mapping.items():
        if oid not in idx:
            errors.append(f"{oid}: objet inconnu")
            continue
        for lang, new_h2 in per_lang.items():
            path = idx[oid].get(lang)
            if not path:
                errors.append(f"{oid} [{lang}]: fichier absent")
                continue
            text = open(path, encoding="utf-8").read()
            head, body = text.split("\n---\n", 1)
            old = re.findall(r"^## (.+)$", body, re.M)
            if len(old) != len(new_h2):
                errors.append(f"{oid} [{lang}]: {len(old)} H2 dans le fichier, "
                              f"{len(new_h2)} fournis — remplacement refusé")
                continue
            it = iter(new_h2)
            new_body = re.sub(r"^## .+$", lambda _m: "## " + next(it), body, flags=re.M)
            total += len(new_h2)
            converted += sum(1 for h in new_h2 if h.strip().endswith("?"))
            if new_body != body:
                touched += 1
                if not dry:
                    open(path, "w", encoding="utf-8").write(head + "\n---\n" + new_body)

    for e in errors:
        print("ERREUR:", e)
    print(f"{touched} fichiers réécrits ; {converted}/{total} H2 interrogatifs "
          f"dans le lot ({100*converted/max(total,1):.0f} %)"
          f"{' — dry-run' if dry else ''}")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
