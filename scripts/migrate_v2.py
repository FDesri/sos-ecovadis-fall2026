#!/usr/bin/env python3
"""Migration du front matter v1 → v2 (schéma 2026-09-01, vision v1.2).

Ajoute trois champs obligatoires à chaque fiche, en place, sans toucher au corps :

  description   meta description de 70 à 155 caractères (KC-T02) — rédigée à la
                main, une par fiche et par langue, lue depuis un fichier JSON.
  intent        niveau d'intention (KC-S03) — classé à la main par objet, donc
                identique dans les trois langues d'un même kb-XXXX.
  review_due    date de révision due (KC-M12), calculée depuis `date_updated`
                selon la cadence GOVERNANCE §3.

`canonical_url` n'est volontairement PAS écrit ici : il est dérivé de
taxonomy/url-plan.yaml par build_index.py (décision D13). Une seule source d'URL.

Le script est idempotent : relancé, il réécrit les mêmes valeurs.

Usage:
  python3 scripts/migrate_v2.py --descriptions <fichier.json> [--intents <fichier.json>] [--dry-run]
"""
import argparse, datetime, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")

# --- cadences de révision (GOVERNANCE §3) --------------------------------
QUARTERLY_TOPICS = {"methodologie", "medailles-percentiles", "rising-bar"}

def review_months(fm):
    """Mois avant révision due, selon le type et les sujets de la fiche."""
    topics = set(fm.get("topics") or [])
    if topics & QUARTERLY_TOPICS or fm.get("content_kind") == "methodology":
        return 3          # méthodologie, médailles, seuils : la barre monte en continu
    if fm.get("type") in ("pricing", "service", "expert", "glossary"):
        return 12         # tarifs et identités : révision annuelle ou sur instruction
    return 6              # articles et FAQ : semestriel

def add_months(d, months):
    y, m = d.year, d.month + months
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return datetime.date(y, m, day)

# --- édition du front matter ---------------------------------------------
FM_RE = re.compile(r"^(---\n)(.*?\n)(---\n)(.*)$", re.S)

def read_fm_block(path):
    text = open(path, encoding="utf-8").read()
    m = FM_RE.match(text)
    if not m:
        raise ValueError(f"{path}: pas de front matter")
    return m.group(2), m.group(4), text

def scalar(v):
    """Rend une valeur YAML scalaire sûre : on cite systématiquement en double
    quotes et on échappe. Les descriptions contiennent : — « » % etc."""
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'

def upsert(lines, key, value, after):
    """Insère `key: value` juste après la clé `after`, ou remplace la ligne existante."""
    out, done = [], False
    for ln in lines:
        if re.match(rf"^{re.escape(key)}\s*:", ln):
            out.append(f"{key}: {value}")
            done = True
            continue
        out.append(ln)
    if not done:
        idx = next((i for i, ln in enumerate(out)
                    if re.match(rf"^{re.escape(after)}\s*:", ln)), None)
        if idx is None:
            out.append(f"{key}: {value}")
        else:
            # sauter les lignes de continuation d'un bloc scalaire (>- / |)
            j = idx + 1
            while j < len(out) and (out[j].startswith("  ") or out[j].startswith("\t")):
                j += 1
            out.insert(j, f"{key}: {value}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--descriptions", required=True)
    ap.add_argument("--intents", default=None,
                    help="JSON {kb-XXXX: intent}; sinon lu depuis taxonomy/intents.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    descs = json.load(open(args.descriptions, encoding="utf-8"))
    intents_path = args.intents or os.path.join(REPO, "taxonomy", "intents.json")
    intents = json.load(open(intents_path, encoding="utf-8"))

    import yaml
    changed = missing = 0
    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            fm_text, body, whole = read_fm_block(path)
            fm = yaml.safe_load(fm_text)
            oid, lang = fm["id"], fm["lang"]

            desc = (descs.get(oid) or {}).get(lang)
            intent = intents.get(oid)
            if not desc or not intent:
                print(f"MANQUE {oid} [{lang}] "
                      f"{'description' if not desc else ''}{' intent' if not intent else ''}")
                missing += 1
                continue
            if not 70 <= len(desc) <= 155:
                print(f"HORS FENÊTRE {oid} [{lang}] : {len(desc)} caractères")
                missing += 1
                continue

            du = fm["date_updated"]
            du = du if isinstance(du, datetime.date) else datetime.date.fromisoformat(str(du))
            due = add_months(du, review_months(fm))

            lines = fm_text.rstrip("\n").split("\n")
            lines = upsert(lines, "description", scalar(desc), after="summary")
            lines = upsert(lines, "intent", intent, after="content_kind")
            lines = upsert(lines, "review_due", due.isoformat(), after="date_updated")

            new = "---\n" + "\n".join(lines) + "\n---\n" + body
            if new != whole:
                changed += 1
                if not args.dry_run:
                    open(path, "w", encoding="utf-8").write(new)

    print(f"{changed} fichiers modifiés, {missing} en défaut"
          f"{' (dry-run, rien écrit)' if args.dry_run else ''}")
    sys.exit(1 if missing else 0)

if __name__ == "__main__":
    main()
