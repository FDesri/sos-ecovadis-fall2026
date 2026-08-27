#!/usr/bin/env python3
"""Generate trilingual FAQ knowledge objects (kb-0100+) from authored data files."""
import importlib.util, os, sys

REPO = "/home/claude/sos-ecovadis-fall2026"
LANGS = ["en", "fr", "nl"]

# EN article slug -> {fr, nl} equivalents (for `related` auto-mapping)
SLUG_MAP = {
    "ecovadis-essentials-guide": {"fr": "guide-essentiel-ecovadis", "nl": "ecovadis-essentials-gids"},
    "understanding-the-ecovadis-scorecard": {"fr": "comprendre-la-fiche-devaluation-ecovadis", "nl": "de-ecovadis-scorecard-begrijpen"},
    "read-share-maximise-your-ecovadis-scorecard": {"fr": "lire-partager-optimiser-sa-fiche-devaluation", "nl": "scorecard-lezen-delen-optimaliseren"},
    "ecovadis-rising-standards-2026": {"fr": "rising-bar-exigences-croissantes-2026", "nl": "rising-bar-strengere-normen-2026"},
    "whats-changing-in-2026": {"fr": "ce-qui-change-en-2026", "nl": "wat-verandert-in-2026"},
    "ecovadis-methodology-updates-q2-2026": {"fr": "evolutions-methodologiques-t2-2026", "nl": "methodologie-updates-q2-2026"},
    "improve-your-ecovadis-score-fast": {"fr": "ameliorer-son-score-ecovadis-rapidement", "nl": "ecovadis-score-snel-verbeteren"},
    "from-committed-badge-to-bronze": {"fr": "du-badge-committed-a-la-medaille-bronze", "nl": "van-committed-badge-naar-brons"},
    "from-bronze-to-silver": {"fr": "de-bronze-a-argent", "nl": "van-brons-naar-zilver"},
    "from-silver-to-gold": {"fr": "de-l-argent-a-l-or", "nl": "van-zilver-naar-goud"},
    "build-strong-ecovadis-submissions-consistently": {"fr": "soumissions-ecovadis-solides-et-regulieres", "nl": "sterke-ecovadis-indieningen-opbouwen"},
    "supporting-documents-for-xs-companies": {"fr": "documents-justificatifs-entreprises-xs", "nl": "bewijsstukken-voor-xs-ondernemingen"},
    "practical-ecovadis-tips": {"fr": "principaux-conseils-pratiques-ecovadis", "nl": "praktische-ecovadis-tips"},
    "ecovadis-activated-criteria-by-sector": {"fr": "criteres-actives-ecovadis-par-secteur", "nl": "geactiveerde-criteria-per-sector"},
    "ecovadis-and-ghg-baseline": {"fr": "ecovadis-et-bilan-ges-de-base", "nl": "ecovadis-en-co2-nulmeting"},
    "environmental-indicators-to-collect": {"fr": "indicateurs-environnementaux-a-collecter", "nl": "milieu-indicatoren-verzamelen"},
    "social-hr-indicators-to-collect": {"fr": "indicateurs-sociaux-rh-a-collecter", "nl": "sociale-hr-indicatoren-verzamelen"},
    "sustainable-procurement-measures-sup307": {"fr": "mesures-achats-responsables-sup307", "nl": "duurzame-inkoop-maatregelen-sup307"},
    "sustainable-procurement-where-to-start": {"fr": "achats-responsables-par-ou-commencer", "nl": "duurzame-inkoop-waar-beginnen"},
    "ecovadis-supplier-engagement-programmes": {"fr": "programmes-engagement-fournisseurs", "nl": "leveranciersengagement-programmas"},
    "self-assessment-vs-expert-guidance": {"fr": "auto-evaluation-ou-accompagnement-expert", "nl": "zelf-doen-of-expertbegeleiding"},
    "why-keeping-a-bronze-medal-is-harder": {"fr": "pourquoi-la-medaille-bronze-est-plus-difficile", "nl": "waarom-een-bronzen-medaille-moeilijker-wordt"},
    "why-ecovadis-strengthens-sustainability-management": {"fr": "pourquoi-se-lancer-dans-ecovadis", "nl": "waarom-aan-ecovadis-beginnen"},
    "b-corp-or-ecovadis": {"fr": "b-corp-ou-ecovadis", "nl": "b-corp-of-ecovadis"},
    "ethics-pack-corruption-harassment-discrimination": {"fr": "pack-corruption-harcelement-discrimination", "nl": "ethiekpakket-corruptie-intimidatie-discriminatie"},
    "evidence-templates-diversity-corruption-child-labour": {"fr": "canevas-diversite-corruption-travail-enfants", "nl": "sjablonen-diversiteit-corruptie-kinderarbeid"},
    "how-much-does-ecovadis-support-cost": {"fr": "combien-coute-un-accompagnement-ecovadis", "nl": "wat-kost-ecovadis-begeleiding"},
    "ecovadis-thresholds-belgian-packaging-pharma": {"fr": "seuils-ecovadis-emballage-pharma-belgique", "nl": "ecovadis-drempels-verpakking-farma-belgie"},
}

def map_related(en_slugs, lang):
    out = []
    for s in en_slugs:
        if lang == "en":
            out.append(s)
        else:
            m = SLUG_MAP.get(s)
            out.append(m[lang] if m else s)
    return out

def yaml_str(s):
    s = s.replace('"', '\\"')
    return f'"{s}"'

def yaml_list(items):
    return "[" + ", ".join(items) + "]"

def yaml_block(s, indent="  "):
    import textwrap
    lines = []
    for chunk in textwrap.wrap(s, width=76):
        lines.append(indent + chunk)
    return ">-\n" + "\n".join(lines)

def render(entry, lang):
    en_slug = entry["slug"]["en"]
    slug = entry["slug"][lang]
    fm = []
    fm.append(f"id: {entry['id']}")
    fm.append("type: faq")
    fm.append(f"lang: {lang}")
    fm.append("source_lang: en")
    fm.append(f"translation_of: {en_slug if lang != 'en' else 'null'}")
    fm.append(f"title: {yaml_str(entry['title'][lang])}")
    fm.append(f"slug: {slug}")
    fm.append(f"summary: {yaml_block(entry['summary'][lang])}")
    fm.append(f"situations: {yaml_list(entry.get('situations', ['S1','S2','S3']))}")
    fm.append(f"sizes: {yaml_list(entry.get('sizes', ['XS','S']))}")
    fm.append(f"content_kind: {entry.get('content_kind', 'general')}")
    fm.append(f"themes: {yaml_list(entry.get('themes', ['general']))}")
    fm.append(f"topics: {yaml_list(entry.get('topics', ['questionnaire']))}")
    fm.append(f"ecovadis_questions: {yaml_list(entry.get('ecovadis_questions', []))}")
    kw = entry.get("keywords", {}).get(lang, [])
    fm.append(f"keywords: {yaml_list(kw)}")
    fm.append(f"audience: {yaml_list(entry.get('audience', ['sustainability_lead','sme_owner']))}")
    fm.append("author: francois-dequenne")
    fm.append("expert_reviewer: francois-dequenne")
    fm.append("source: esgim-proprietary")
    fm.append(f"source_note: {yaml_str(entry['source_note'])}")
    fm.append("confidentiality: public")
    fm.append(f"reliability: {entry.get('reliability', 'expert-drafted')}")
    fm.append("date_created: 2026-08-27")
    fm.append("date_updated: 2026-08-27")
    fm.append("version: 1")
    fm.append("status: review")
    fm.append(f"related: {yaml_list(map_related(entry.get('related', []), lang))}")
    body = entry["body"][lang].strip()
    return "---\n" + "\n".join(fm) + f"\n---\n\n# {entry['title'][lang]}\n\n{body}\n"

def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FAQS

def main():
    data_files = sorted(f for f in os.listdir("/home/claude/kc") if f.startswith("faq_data_") and f.endswith(".py"))
    total = 0
    ids = set()
    for df in data_files:
        for entry in load(os.path.join("/home/claude/kc", df)):
            if entry["id"] in ids:
                print("DUPLICATE ID", entry["id"]); sys.exit(1)
            ids.add(entry["id"])
            for lang in LANGS:
                path = os.path.join(REPO, "catalog", lang, "faq", entry["slug"][lang] + ".md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(render(entry, lang))
                total += 1
    print(f"Wrote {total} files from {len(ids)} FAQ objects out of {len(data_files)} data files")

if __name__ == "__main__":
    main()
