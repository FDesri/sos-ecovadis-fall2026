#!/usr/bin/env python3
"""Place les références au plus près des affirmations (KC-C11) et renseigne
le champ `sources` du front matter.

Deux effets, un seul passage :

1. CORPS — la PREMIÈRE mention d'un référentiel nommé (CSDDD, CSRD, GRI,
   GHG Protocol, ISO 14001, SBTi, Pacte mondial, VSME, Baromètre EcoVadis…)
   devient un lien vers sa source canonique. La référence se trouve donc à
   l'endroit de l'affirmation, pas dans une bibliographie de fin de page —
   c'est exactement ce que KC-C11 exige. Les mentions suivantes restent en
   texte : un lien par notion et par fiche, pas un champ de mines.

2. FRONT MATTER — `sources: [ids]` liste les entrées de
   taxonomy/sources-registry.yaml effectivement citées, y compris celles
   qui n'ont pas d'URL (esgim-portfolio) et qui ne peuvent donc pas être
   liées dans le corps.

Ne touche jamais : les titres (# / ##), les blocs de code, les liens déjà
posés, le front matter hors du champ `sources`.

Politique de liens : voir taxonomy/sources-registry.yaml. Aucun lien vers
un concurrent d'ESGIM n'est possible — le registre n'en contient pas.

Usage:  python3 scripts/link_sources.py [--dry-run]
"""
import os, re, sys
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")
REGISTRY = os.path.join(REPO, "taxonomy", "sources-registry.yaml")

# Motifs de détection par source et par langue.
# La première capture est le texte qui devient le libellé du lien.
TERMS = {
    "eu-csddd": {
        "fr": r"\b(CSDDD|directive 2024/1760|devoir de vigilance)\b",
        "en": r"\b(CSDDD|Directive 2024/1760|corporate sustainability due diligence)\b",
        "nl": r"\b(CSDDD|richtlijn 2024/1760|zorgvuldigheidsplicht)\b",
    },
    "eu-csrd": {
        "fr": r"\b(CSRD|ESRS)\b",
        "en": r"\b(CSRD|ESRS)\b",
        "nl": r"\b(CSRD|ESRS)\b",
    },
    "ec-omnibus": {
        "fr": r"\b(paquet Omnibus|Omnibus)\b",
        "en": r"\b(Omnibus package|Omnibus)\b",
        "nl": r"\b(Omnibus-pakket|Omnibus)\b",
    },
    "efrag-vsme": {
        "fr": r"\b(VSME)\b", "en": r"\b(VSME)\b", "nl": r"\b(VSME)\b",
    },
    "gri-standards": {
        "fr": r"\b(GRI)\b", "en": r"\b(GRI)\b", "nl": r"\b(GRI)\b",
    },
    "ghg-protocol": {
        "fr": r"\b(GHG Protocol|Protocole GES)\b",
        "en": r"\b(GHG Protocol)\b",
        "nl": r"\b(GHG Protocol)\b",
    },
    "sbti": {
        "fr": r"\b(SBTi)\b", "en": r"\b(SBTi)\b", "nl": r"\b(SBTi)\b",
    },
    "ungc-cop": {
        "fr": r"\b(Pacte mondial(?: des Nations unies)?|UNGC)\b",
        "en": r"\b(UN Global Compact|Global Compact|UNGC)\b",
        "nl": r"\b(UN Global Compact|Global Compact|UNGC)\b",
    },
    "iso-14001": {"fr": r"\b(ISO 14001)\b", "en": r"\b(ISO 14001)\b", "nl": r"\b(ISO 14001)\b"},
    "iso-45001": {"fr": r"\b(ISO 45001)\b", "en": r"\b(ISO 45001)\b", "nl": r"\b(ISO 45001)\b"},
    "iso-50001": {"fr": r"\b(ISO 50001)\b", "en": r"\b(ISO 50001)\b", "nl": r"\b(ISO 50001)\b"},
    "ecovadis-barometer-2026": {
        "fr": r"\b(Baromètre (?:des )?Achats Responsables(?: EcoVadis)?(?: 2026)?)\b",
        "en": r"\b(Sustainable Procurement Barometer(?: 2026)?)\b",
        "nl": r"\b(Sustainable Procurement Barometer(?: 2026)?)\b",
    },
    "ecovadis-360-watch": {
        "fr": r"\b((?:V|v)eille 360°|360° Watch)\b",
        "en": r"\b(360° Watch)\b",
        "nl": r"\b(360° Watch)\b",
    },
    "fod-werkgelegenheid": {
        "fr": r"\b(SPF Emploi)\b", "en": r"\b(Belgian federal labour authority)\b",
        "nl": r"\b(FOD Werkgelegenheid)\b",
    },
    "unia": {"fr": r"\b(Unia)\b", "en": r"\b(Unia)\b", "nl": r"\b(Unia)\b"},
}

# Sources sans URL liable, ou trop diffuses pour un lien ponctuel :
# détectées pour le front matter uniquement.
#
# `ecovadis-methodology` couvre volontairement large. Presque toute fiche de
# ce catalogue décrit un mécanisme d'évaluation EcoVadis : son affirmation
# remonte à la méthodologie de l'éditeur, et le dire est plus honnête que de
# laisser la fiche sans provenance. Les fiches qui ne parlent que de l'offre
# ESGIM sont traitées par TYPE_SOURCES ci-dessous.
METADATA_ONLY = {
    "ecovadis-methodology": r"\b(EcoVadis|P-A-R|PAR|Politiques-Actions-Résultats|"
                            r"Policies-Actions-Results|Beleid-Acties-Resultaten|"
                            r"critères activés|activated criteria|geactiveerde criteria|"
                            r"pondération|weighting|weging|"
                            r"(?:GEN|LAB|ENV|CAR|FB|FBP|SUP)[0-9]{3,4})\b",
    "ecovadis-medals": r"\b(percentile|percentiel|Bronze|Brons|Argent|Zilver|Platine|Platinum|"
                       r"Committed|Fast Mover)\b",
    # Uniquement là où un CHIFFRE de portefeuille ESGIM est avancé, pas à chaque
    # mention du nom : citer sa propre donnée est une affirmation, se nommer non.
    "esgim-portfolio": (
        r"(100\+\s*(?:projets|projects|projecten)"
        r"|87\s*%"
        r"|13[,.]8\s*(?:points|punten)"
        r"|(?:seuils?|scores?)\s+indicatifs?"
        r"|indicati(?:ve|f)\s+(?:score|threshold)"
        r"|indicatieve\s+(?:score|drempel)"
        r"|benchmark(?:ing)?\s+ESGIM|ESGIM\s+benchmark"
        r"|portefeuille (?:clients? )?d['’]ESG"
        r"|portfolio (?:data|of ESG)"
        r"|données internes du portefeuille"
        r"|interne portefeuillegegevens"
        r"|client ESGIM|ESGIM client|ESGIM-klant"
        r"|imprimeur flexographique|flexographic printer|flexografische drukkerij"
        r"|techniques spéciales du bâtiment|special building techniques|bouwtechniek)"
    ),
}

# Sources attachées d'office selon le type d'objet : une fiche de service, de
# tarif ou d'expert avance des faits sur ESGIM, pas sur EcoVadis.
TYPE_SOURCES = {
    "service":  ["esgim-portfolio"],
    "pricing":  ["esgim-portfolio"],
    "expert":   ["esgim-portfolio"],
    # Tout article, FAQ ou entrée de glossaire de ce catalogue répond à une
    # question posée dans le cadre EcoVadis : sa provenance de fond est la
    # méthodologie de l'éditeur, même quand le corps ne le nomme pas.
    "article":  ["ecovadis-methodology"],
    "faq":      ["ecovadis-methodology"],
    "glossary": ["ecovadis-methodology"],
}

CODE_BLOCK = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")

def protect(body):
    """Masque les zones à ne pas toucher : titres, code, liens existants."""
    spans = []
    for m in CODE_BLOCK.finditer(body):
        spans.append(m.span())
    for m in LINK.finditer(body):
        spans.append(m.span())
    for m in re.finditer(r"^#{1,6} .*$", body, re.M):
        spans.append(m.span())
    return spans

def in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)

def main():
    dry = "--dry-run" in sys.argv
    reg = yaml.safe_load(open(REGISTRY, encoding="utf-8"))["sources"]

    touched = linked = 0
    per_source = {}
    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^(---\n)(.*?\n)(---\n)(.*)$", text, re.S)
            fm_text, body = m.group(2), m.group(4)
            fm = yaml.safe_load(fm_text)
            lang = fm["lang"]
            lang = lang if lang in ("fr", "en", "nl") else "fr"

            found = []
            new_body = body
            for sid, per_lang in TERMS.items():
                pat = per_lang.get(lang)
                if not pat:
                    continue
                url = (reg.get(sid) or {}).get("url")
                spans = protect(new_body)
                hit = None
                for mm in re.finditer(pat, new_body):
                    if not in_spans(mm.start(), spans):
                        hit = mm
                        break
                if not hit:
                    continue
                found.append(sid)
                per_source[sid] = per_source.get(sid, 0) + 1
                if url:
                    label = hit.group(1)
                    new_body = (new_body[:hit.start(1)] + f"[{label}]({url})"
                                + new_body[hit.end(1):])
                    linked += 1

            # Filet de sécurité : si aucune référence n'a pu être posée dans le
            # corps, la première mention d'EcoVadis ou d'un code question renvoie à
            # la méthodologie de l'éditeur. Une fiche ne reste pas sans référence.
            if not re.search(r"\]\(https?://", new_body):
                url = (reg.get("ecovadis-methodology") or {}).get("url")
                spans = protect(new_body)
                for mm in re.finditer(r"\bEcoVadis\b|\b(?:GEN|LAB|ENV|CAR|FB|FBP|SUP)[0-9]{3,4}\b", new_body):
                    if not in_spans(mm.start(), spans):
                        new_body = (new_body[:mm.start()] + f"[{mm.group(0)}]({url})"
                                    + new_body[mm.end():])
                        linked += 1
                        break

            for sid, pat in METADATA_ONLY.items():
                if re.search(pat, body) and sid not in found:
                    found.append(sid)
                    per_source[sid] = per_source.get(sid, 0) + 1

            for sid in TYPE_SOURCES.get(fm.get("type"), []):
                if sid not in found:
                    found.append(sid)
                    per_source[sid] = per_source.get(sid, 0) + 1

            found = sorted(set(found))
            fm_lines = fm_text.rstrip("\n").split("\n")
            fm_lines = [l for l in fm_lines if not re.match(r"^sources\s*:", l)]
            if found:
                idx = next((i for i, l in enumerate(fm_lines)
                            if re.match(r"^source_note\s*:", l)), len(fm_lines) - 1)
                fm_lines.insert(idx + 1, "sources: [" + ", ".join(found) + "]")

            new = "---\n" + "\n".join(fm_lines) + "\n---\n" + new_body
            if new != text:
                touched += 1
                if not dry:
                    open(path, "w", encoding="utf-8").write(new)

    print(f"{touched} fichiers modifiés, {linked} liens posés dans les corps"
          f"{' — dry-run' if dry else ''}")
    print("sources citées :")
    for sid, n in sorted(per_source.items(), key=lambda kv: -kv[1]):
        print(f"  {sid:26} {n} fiches")

if __name__ == "__main__":
    main()
