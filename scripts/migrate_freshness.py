#!/usr/bin/env python3
"""Migration unique — ajoute `volatility` et `verified_at`, réaligne `review_due`.

Décisions D32 et D33 (vision v2.3). À lancer UNE fois, puis à supprimer ou à
laisser dormir : les fiches suivantes naissent avec les trois champs.

Ce que le script écrit dans chaque fichier, juste après `date_updated` :

    verified_at: 2026-09-01      # = date_updated à la migration
    volatility: annual           # classe déduite du type et des sujets
    review_due: 2027-09-01       # = verified_at + cadence (freshness.yaml)

La classe déduite est un point de départ, pas un verdict. François corrige à la
main les fiches dont il sait qu'elles vieillissent plus vite : c'est une ligne.

Usage:  python3 scripts/migrate_freshness.py [--dry-run]
"""
import os, re, sys
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")
CADENCE = yaml.safe_load(open(os.path.join(REPO, "taxonomy", "freshness.yaml"),
                              encoding="utf-8"))["cadence_months"]

# Priorité décroissante : la première règle qui matche gagne.
RULES = [
    ("event-driven",   {"topics": {"vsme-csrd"}}),
    ("ecovadis-cycle", {"topics": {"medailles-percentiles", "rising-bar"},
                        "types": {"pricing"}}),
    ("evergreen",      {"types": {"glossary", "expert", "organization"}}),
]
DEFAULT = "annual"


def add_months(d, months):
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    day = min(d.day, [31, 29 if (y % 4 == 0 and (y % 100 or y % 400 == 0)) else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return d.replace(year=y, month=m, day=day)


def classify(fm):
    topics = set(fm.get("topics") or [])
    for name, rule in RULES:
        if topics & rule.get("topics", set()) or fm["type"] in rule.get("types", set()):
            return name
    return DEFAULT


def main():
    dry = "--dry-run" in sys.argv
    seen = {}
    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if not m:
                continue
            fm = yaml.safe_load(m.group(1))
            if "volatility" in fm and "verified_at" in fm:
                continue

            vol = classify(fm)
            verified = fm["date_updated"]
            due = add_months(verified, CADENCE[vol])
            block = (f"verified_at: {verified}\n"
                     f"volatility: {vol}\n"
                     f"review_due: {due}")

            head = m.group(1)
            if re.search(r"^review_due:.*$", head, re.M):
                head = re.sub(r"^review_due:.*$", block, head, count=1, flags=re.M)
            else:
                head = re.sub(r"^(date_updated:.*)$", r"\1\n" + block, head,
                              count=1, flags=re.M)
            if not dry:
                open(path, "w", encoding="utf-8").write(
                    f"---\n{head}\n---\n" + text[m.end():])
            seen[vol] = seen.get(vol, 0) + 1

    total = sum(seen.values())
    print(("simulation — " if dry else "") + f"{total} fichiers traités")
    for k in sorted(seen):
        print(f"  {k:16s} {seen[k]}")


if __name__ == "__main__":
    main()
