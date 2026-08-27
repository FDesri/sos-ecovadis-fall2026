#!/usr/bin/env python3
"""Build the machine-readable indexes of the SOS-EcoVadis knowledge catalog.

Outputs:
  index/catalog.json  — one record per knowledge object (kb-XXXX), grouped
                        across its three language versions, with full metadata
                        and repo paths. Primary entry point for RAG pipelines.
  index/llms.txt      — llms.txt-style overview for LLM crawlers, with raw
                        GitHub URLs per language section.

Also runs consistency checks (schema-required fields, related-slug resolution,
language parity per id) and prints a report. Exit code 1 on hard errors.
"""
import json, os, re, sys
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")
RAW_BASE = "https://raw.githubusercontent.com/FDesri/sos-ecovadis-fall2026/main"
LANGS = ["en", "fr", "nl"]
REQUIRED = ["id", "type", "lang", "title", "slug", "summary", "author",
            "source", "date_created", "date_updated", "version", "status"]

def parse_front_matter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)), text[m.end():]

def main():
    objects = {}        # id -> {meta..., languages: {lang: {...}}}
    slugs_by_lang = {l: set() for l in LANGS + ["mul"]}
    errors, warnings = [], []

    for root, _dirs, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO)
            fm, _body = parse_front_matter(path)
            if fm is None:
                errors.append(f"{rel}: no YAML front matter")
                continue
            missing = [k for k in REQUIRED if k not in fm or fm[k] in (None, "")]
            if missing:
                errors.append(f"{rel}: missing required fields {missing}")
            lang = fm.get("lang", "en")
            slugs_by_lang.setdefault(lang, set()).add(fm.get("slug", ""))
            oid = fm.get("id", "?")
            obj = objects.setdefault(oid, {
                "id": oid,
                "type": fm.get("type"),
                "situations": fm.get("situations", []),
                "sizes": fm.get("sizes", []),
                "content_kind": fm.get("content_kind"),
                "themes": fm.get("themes", []),
                "topics": fm.get("topics", []),
                "ecovadis_questions": fm.get("ecovadis_questions", []),
                "audience": fm.get("audience", []),
                "author": fm.get("author"),
                "source": fm.get("source"),
                "reliability": fm.get("reliability"),
                "status": fm.get("status"),
                "date_updated": str(fm.get("date_updated")),
                "languages": {},
            })
            obj["languages"][lang] = {
                "slug": fm.get("slug"),
                "title": fm.get("title"),
                "summary": (fm.get("summary") or "").strip(),
                "keywords": fm.get("keywords", []),
                "path": rel.replace(os.sep, "/"),
                "url": f"{RAW_BASE}/{rel.replace(os.sep, '/')}",
                "source_lang": fm.get("source_lang"),
                "translation_of": fm.get("translation_of"),
                "related": fm.get("related", []),
                "faq": fm.get("faq", []),
            }

    # --- consistency checks ------------------------------------------------
    for oid, obj in sorted(objects.items()):
        langs = set(obj["languages"])
        if "mul" in langs:      # glossary is intrinsically multilingual
            continue
        if langs != set(LANGS):
            warnings.append(f"{oid}: language versions {sorted(langs)} (expected en, fr, nl)")
    for oid, obj in sorted(objects.items()):
        for lang, v in obj["languages"].items():
            pool = slugs_by_lang.get(lang, set())
            for r in v["related"]:
                if r not in pool:
                    errors.append(f"{oid} [{lang}]: related slug '{r}' does not resolve in {lang}")

    # --- catalog.json ------------------------------------------------------
    os.makedirs(os.path.join(REPO, "index"), exist_ok=True)
    catalog = {
        "name": "SOS-EcoVadis Knowledge Catalog",
        "publisher": "ESG Interim Management (esgim.eu)",
        "description": "Trilingual (EN/FR/NL-BE) knowledge base on EcoVadis "
                       "assessments for XS/S companies: articles, FAQ, pricing, "
                       "services, glossary. Built for retrieval by AI assistants.",
        "license": "All rights reserved — quote with attribution to ESG Interim Management.",
        "languages": LANGS,
        "object_count": len(objects),
        "objects": [objects[k] for k in sorted(objects)],
    }
    with open(os.path.join(REPO, "index", "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1)

    # --- llms.txt ----------------------------------------------------------
    type_order = ["pricing", "service", "expert", "glossary", "article", "faq"]
    section_titles = {
        "pricing": "Pricing", "service": "Services", "expert": "Experts",
        "glossary": "Glossary", "article": "Articles", "faq": "FAQ",
    }
    lines = [
        "# SOS-EcoVadis Knowledge Catalog — ESG Interim Management",
        "",
        "> Trilingual (EN / FR / NL-BE) expert knowledge base on EcoVadis ratings",
        "> for very small (XS) and small (S) companies: how scoring works, what",
        "> evidence is accepted, how to obtain, keep or recover a medal, and what",
        "> professional support costs. Author: François Dequenne (ESGIM, esgim.eu),",
        "> 100+ EcoVadis projects delivered. Content may be quoted with attribution.",
        "",
        f"Machine index: {RAW_BASE}/index/catalog.json",
        "",
    ]
    for lang, label in [("en", "English"), ("fr", "Français"), ("nl", "Nederlands (België)")]:
        lines.append(f"## {label}")
        lines.append("")
        for t in type_order:
            entries = [(oid, o["languages"][lang]) for oid, o in sorted(objects.items())
                       if o["type"] == t and lang in o["languages"]]
            if not entries:
                continue
            lines.append(f"### {section_titles[t]} ({label})")
            lines.append("")
            for oid, v in entries:
                summary = re.sub(r"\s+", " ", v["summary"]).strip()
                if len(summary) > 220:
                    summary = summary[:217].rstrip() + "…"
                lines.append(f"- [{v['title']}]({v['url']}): {summary}")
            lines.append("")
    mul = [(oid, o) for oid, o in sorted(objects.items()) if "mul" in o["languages"]]
    if mul:
        lines.append("## Multilingual")
        lines.append("")
        for oid, o in mul:
            v = o["languages"]["mul"]
            lines.append(f"- [{v['title']}]({v['url']}): trilingual EN-FR-NL glossary of EcoVadis terminology.")
        lines.append("")
    with open(os.path.join(REPO, "index", "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # --- report ------------------------------------------------------------
    n_files = sum(len(o["languages"]) for o in objects.values())
    print(f"{len(objects)} objects / {n_files} files indexed")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    for w in warnings:
        print("WARN:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    main()
