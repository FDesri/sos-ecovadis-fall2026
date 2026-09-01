#!/usr/bin/env python3
"""Construit les index machine du Knowledge Catalog SOS-EcoVadis et valide le dépôt.

v2 (2026-09-01, vision v1.2). Ce script est la SEULE source des URL canoniques
et des index : rien de ce qu'il écrit ne doit être édité à la main.

Sorties
-------
index/catalog.json      Graphe complet — tous les objets, tous les statuts, avec
                        `canonical_url`, l'appartenance aux hubs, les sources
                        résolues et le statut de publication. Point d'entrée RAG.
index/jsonld.json       JSON-LD schema.org par objet (Article / FAQPage /
                        Organization / Person), à injecter par le build du site.
public/                 Ce qui sera servi à la RACINE du domaine :
  robots.txt            Politique de robots explicite (KC-A03 → A06).
  sitemap.xml           Objets PUBLIÉS uniquement (KC-T06).
  llms.txt              Répertoire agents : hubs d'abord, fiches ensuite (KC-L01→L04).
  llms-full.txt         Texte intégral des fiches publiées, généré (KC-L05).

Règle de publication (décision D19)
-----------------------------------
Seuls les objets en `status: published` reçoivent une URL canonique et entrent
au sitemap, dans llms.txt et dans llms-full.txt. Une fiche en `review` ou
`draft` reste dans catalog.json, marquée comme telle, et n'est pas indexable.
Tant que François n'a pas relu, les surfaces publiques sont vides — c'est le
comportement voulu, pas un bug.

Contrôles bloquants (KC-G15) — le script sort en code 1 :
  champ obligatoire manquant · description hors 70-155 · id ou slug dupliqué ·
  slug `related` non résolu · source inconnue du registre · parité de langues
  rompue · objet sans hub · fiche publiée dont `review_due` est dépassée.

Usage:  python3 scripts/build_index.py [--check-only]
"""
import datetime, json, os, re, sys
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(REPO, "catalog")
TAX = os.path.join(REPO, "taxonomy")
LANGS = ["en", "fr", "nl"]
REQUIRED = ["id", "type", "lang", "title", "slug", "summary", "description", "intent",
            "author", "source", "date_created", "date_updated", "review_due",
            "version", "status"]

def load(name):
    return yaml.safe_load(open(os.path.join(TAX, name), encoding="utf-8"))

def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)), m.group(2)

# --------------------------------------------------------------------------
def canonical(urlplan, lang, otype, slug):
    """URL canonique d'une fiche. Unique source : taxonomy/url-plan.yaml."""
    site = urlplan["site"]
    base = f"{site['scheme']}://{site['canonical_host']}"
    singles = urlplan["singletons"]
    if otype == "glossary":
        return base + singles["glossary"]["canonical"]
    if otype == "organization":
        return base + singles["organization"][lang]
    branch = urlplan["branches"][otype][lang]
    return f"{base}/{lang}/{branch}/{slug}/"

def hub_url(urlplan, lang, slug):
    site = urlplan["site"]
    branch = urlplan["branches"]["hub"][lang]
    return f"{site['scheme']}://{site['canonical_host']}/{lang}/{branch}/{slug}/"

# --------------------------------------------------------------------------
def main():
    check_only = "--check-only" in sys.argv
    urlplan = load("url-plan.yaml")
    hubs_cfg = load("hubs.yaml")
    registry = load("sources-registry.yaml")["sources"]
    today = datetime.date.today()

    objects, bodies = {}, {}
    slugs_by_lang = {l: {} for l in LANGS + ["mul"]}
    errors, warnings = [], []

    for root, _d, files in os.walk(CATALOG):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, REPO).replace(os.sep, "/")
            fm, body = parse(path)
            if fm is None:
                errors.append(f"{rel}: pas de front matter")
                continue

            missing = [k for k in REQUIRED if k not in fm or fm[k] in (None, "")]
            if missing:
                errors.append(f"{rel}: champs obligatoires manquants {missing}")
                continue
            if not 70 <= len(fm["description"]) <= 155:
                errors.append(f"{rel}: description de {len(fm['description'])} caractères "
                              f"(fenêtre 70-155)")
            for sid in fm.get("sources") or []:
                if sid not in registry:
                    errors.append(f"{rel}: source '{sid}' absente du registre")

            lang, oid = fm["lang"], fm["id"]
            if fm["slug"] in slugs_by_lang.setdefault(lang, {}):
                errors.append(f"{rel}: slug '{fm['slug']}' déjà utilisé en {lang} par "
                              f"{slugs_by_lang[lang][fm['slug']]}")
            slugs_by_lang[lang][fm["slug"]] = oid

            published = fm["status"] == "published"
            if published:
                due = fm["review_due"]
                due = due if isinstance(due, datetime.date) else datetime.date.fromisoformat(str(due))
                if due < today:
                    errors.append(f"{rel}: publiée et révision due depuis {due} (KC-M12)")

            obj = objects.setdefault(oid, {
                "id": oid, "type": fm["type"], "status": fm["status"],
                "intent": fm.get("intent"),
                "situations": fm.get("situations", []), "sizes": fm.get("sizes", []),
                "content_kind": fm.get("content_kind"), "themes": fm.get("themes", []),
                "topics": fm.get("topics", []),
                "ecovadis_questions": fm.get("ecovadis_questions", []),
                "audience": fm.get("audience", []), "author": fm.get("author"),
                "source": fm.get("source"), "reliability": fm.get("reliability"),
                "sources": sorted(set(fm.get("sources") or [])),
                "date_updated": str(fm["date_updated"]),
                "review_due": str(fm["review_due"]),
                "hubs": [], "languages": {},
            })
            obj["languages"][lang] = {
                "slug": fm["slug"], "title": fm["title"],
                "summary": re.sub(r"\s+", " ", (fm.get("summary") or "")).strip(),
                "description": fm["description"],
                "keywords": fm.get("keywords", []), "path": rel,
                "canonical_url": canonical(urlplan, lang, fm["type"], fm["slug"])
                                 if published else None,
                "source_lang": fm.get("source_lang"),
                "translation_of": fm.get("translation_of"),
                "related": fm.get("related", []),
                "relations": fm.get("relations", {}) or {},
                "faq": fm.get("faq", []),
            }
            bodies[(oid, lang)] = body

    # --- parité de langues -------------------------------------------------
    for oid, obj in sorted(objects.items()):
        langs = set(obj["languages"])
        if "mul" in langs:
            continue
        if langs != set(LANGS):
            errors.append(f"{oid}: versions linguistiques {sorted(langs)} (attendu en, fr, nl)")

    # --- résolution des `related` -----------------------------------------
    for oid, obj in sorted(objects.items()):
        for lang, v in obj["languages"].items():
            pool = slugs_by_lang.get(lang, {})
            for r in v["related"]:
                if r not in pool:
                    errors.append(f"{oid} [{lang}] : slug related '{r}' ne résout pas")
            for kind in ("alternatives", "prerequisites"):
                for r in (v["relations"].get(kind) or []):
                    if r not in pool:
                        errors.append(f"{oid} [{lang}] : {kind} '{r}' ne résout pas")

    # --- hubs (KC-S09, KC-T07 : aucune page orpheline) --------------------
    hub_defs = hubs_cfg["hubs"]
    hub_members = {h: [] for h in hub_defs}
    for oid, obj in sorted(objects.items()):
        mine = [t for t in obj["topics"] if t in hub_defs]
        if not mine:
            errors.append(f"{oid}: aucun sujet ne correspond à un hub — page orpheline")
            continue
        obj["hubs"] = mine
        obj["parent_hub"] = mine[0]          # hub principal = premier sujet déclaré
        for t in mine:
            hub_members[t].append(oid)

    published_ids = {oid for oid, o in objects.items() if o["status"] == "published"}

    if errors:
        for e in errors:
            print("ERREUR:", e)
        print(f"\n{len(objects)} objets — {len(errors)} erreurs, build refusé")
        sys.exit(1)
    if check_only:
        print(f"{len(objects)} objets, {sum(len(o['languages']) for o in objects.values())} "
              f"fichiers — 0 erreur, {len(warnings)} avertissement(s)")
        for w in warnings:
            print("WARN:", w)
        return

    # ======================================================================
    #  ÉCRITURES
    # ======================================================================
    os.makedirs(os.path.join(REPO, "index"), exist_ok=True)
    public = os.path.join(REPO, "public")
    os.makedirs(public, exist_ok=True)
    site = urlplan["site"]
    base = f"{site['scheme']}://{site['canonical_host']}"

    # --- catalog.json ------------------------------------------------------
    catalog = {
        "name": "SOS-EcoVadis Knowledge Catalog",
        "publisher": "ESG Interim Management (esgim.eu)",
        "description": "Trilingual (EN/FR/NL-BE) knowledge base on EcoVadis assessments "
                       "for XS/S companies: articles, FAQ, pricing, services, glossary. "
                       "Built for retrieval by AI assistants.",
        "license": {
            "content": "CC BY-NC 4.0",
            "content_url": "https://creativecommons.org/licenses/by-nc/4.0/",
            "code": "MIT",
            "note": "Quote with attribution to ESG Interim Management (esgim.eu).",
        },
        "canonical_site": base,
        "languages": LANGS,
        "generated": datetime.date.today().isoformat(),
        "object_count": len(objects),
        "published_count": len(published_ids),
        "sources": {sid: {k: v for k, v in s.items() if k in
                          ("title", "publisher", "kind", "url", "accessed")}
                    for sid, s in registry.items()},
        "hubs": [{
            "id": h, "slug": hub_defs[h]["slug"],
            "title": hub_defs[h]["title"],
            "url": {l: hub_url(urlplan, l, hub_defs[h]["slug"][l]) for l in LANGS},
            "member_count": len(hub_members[h]),
            "members": sorted(hub_members[h]),
        } for h in sorted(hub_defs, key=lambda k: -len(hub_members[k]))],
        "objects": [objects[k] for k in sorted(objects)],
    }
    json.dump(catalog, open(os.path.join(REPO, "index", "catalog.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

    # --- JSON-LD (KC-T04) --------------------------------------------------
    ORG = {
        "@type": "Organization", "@id": f"{base}/#organization",
        "name": "ESG Interim Management", "alternateName": "ESGIM",
        "url": "https://esgim.eu/",
    }
    PERSON = {
        "@type": "Person", "@id": f"{base}/#francois-dequenne",
        "name": "François Dequenne", "jobTitle": "EcoVadis Interim Manager",
        "worksFor": {"@id": f"{base}/#organization"},
    }
    jsonld = {"@context": "https://schema.org", "organization": ORG, "person": PERSON,
              "objects": {}}
    for oid, obj in sorted(objects.items()):
        for lang, v in obj["languages"].items():
            if not v["canonical_url"]:
                continue
            node = {
                "@context": "https://schema.org",
                "@type": "FAQPage" if obj["type"] == "faq" else "Article",
                "@id": v["canonical_url"], "url": v["canonical_url"],
                "headline": v["title"], "description": v["description"],
                "inLanguage": "nl-BE" if lang == "nl" else lang,
                "datePublished": str(obj["date_updated"]),
                "dateModified": str(obj["date_updated"]),
                "author": {"@id": f"{base}/#francois-dequenne"},
                "publisher": {"@id": f"{base}/#organization"},
                "license": "https://creativecommons.org/licenses/by-nc/4.0/",
                "keywords": v["keywords"],
                "citation": [registry[s]["url"] for s in obj["sources"]
                             if registry.get(s, {}).get("url")],
            }
            if obj["type"] == "faq":
                node["mainEntity"] = [{
                    "@type": "Question", "name": v["title"],
                    "acceptedAnswer": {"@type": "Answer", "text": v["description"]},
                }]
            elif v["faq"]:
                node["mainEntity"] = [{
                    "@type": "Question", "name": q["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
                } for q in v["faq"]]
            jsonld["objects"][f"{oid}:{lang}"] = node
    json.dump(jsonld, open(os.path.join(REPO, "index", "jsonld.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

    # --- robots.txt (KC-A03 → A06) ----------------------------------------
    robots = f"""# SOS-EcoVadis Knowledge Catalog — ESG Interim Management (esgim.eu)
# Politique de robots explicite. Toute décision ci-dessous est délibérée :
# aucun blocage n'est accidentel (KC-A06).

# --- Recherche assistée par IA : autorisée, c'est l'objectif du catalogue ---
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# --- Recherche classique ---------------------------------------------------
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Google-Extended
Allow: /

# --- Entraînement de modèles : décision distincte de la recherche -----------
# ESGIM autorise l'entraînement : être une source citée sert l'objectif de
# découvrabilité, et le contenu est une expertise publique que l'on veut voir
# attribuée. Remplacer par "Disallow: /" pour revenir sur ce choix.
User-agent: GPTBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot-Extended
Allow: /

# --- Tout le reste ---------------------------------------------------------
User-agent: *
Allow: /

Sitemap: {base}/sitemap.xml
"""
    open(os.path.join(public, "robots.txt"), "w", encoding="utf-8").write(robots)

    # --- sitemap.xml (KC-T06) ---------------------------------------------
    urls = []
    for h in sorted(hub_defs):
        if any(oid in published_ids for oid in hub_members[h]):
            for l in LANGS:
                urls.append((hub_url(urlplan, l, hub_defs[h]["slug"][l]),
                             datetime.date.today().isoformat()))
    for oid in sorted(published_ids):
        for lang, v in objects[oid]["languages"].items():
            if v["canonical_url"]:
                urls.append((v["canonical_url"], str(objects[oid]["date_updated"])))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(public, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

    # --- llms.txt (KC-L01 → L04, L06) -------------------------------------
    LANG_LABEL = {"en": "English", "fr": "Français", "nl": "Nederlands (België)"}
    TYPE_LABEL = {"pricing": {"en": "Pricing", "fr": "Tarifs", "nl": "Tarieven"},
                  "service": {"en": "Services", "fr": "Services", "nl": "Diensten"},
                  "expert": {"en": "Experts", "fr": "Experts", "nl": "Experts"},
                  "glossary": {"en": "Glossary", "fr": "Glossaire", "nl": "Woordenlijst"},
                  "article": {"en": "Articles", "fr": "Articles", "nl": "Artikels"},
                  "faq": {"en": "FAQ", "fr": "FAQ", "nl": "FAQ"},
                  "organization": {"en": "About", "fr": "À propos", "nl": "Over ons"}}
    L = ["# SOS-EcoVadis Knowledge Catalog — ESG Interim Management", "",
         "> Base de connaissances trilingue (EN / FR / NL-BE) sur la notation EcoVadis",
         "> pour les très petites (XS) et petites (S) entreprises : fonctionnement du",
         "> score, preuves acceptées, obtention, maintien et récupération d'une médaille,",
         "> coût d'un accompagnement. Auteur : François Dequenne (ESGIM, esgim.eu),",
         "> plus de 100 projets EcoVadis livrés.",
         "> Licence : CC BY-NC 4.0 — citation avec attribution à ESG Interim Management.",
         "",
         f"Index machine complet : {base}/catalog.json",
         f"Texte intégral : {base}/llms-full.txt", ""]
    L += ["## Index par sujet", ""]
    for h in sorted(hub_defs, key=lambda k: -len(hub_members[k])):
        pub = [o for o in hub_members[h] if o in published_ids]
        if not pub:
            continue
        L.append(f"- [{hub_defs[h]['title']['fr']}]"
                 f"({hub_url(urlplan, 'fr', hub_defs[h]['slug']['fr'])}) : "
                 f"{len(pub)} fiches")
    L.append("")
    for lang in LANGS:
        entries = [(oid, objects[oid]) for oid in sorted(published_ids)
                   if lang in objects[oid]["languages"]]
        if not entries:
            continue
        L += [f"## {LANG_LABEL[lang]}", ""]
        for t in ["organization", "pricing", "service", "expert", "glossary",
                  "article", "faq"]:
            rows = [(oid, o["languages"][lang]) for oid, o in entries if o["type"] == t]
            if not rows:
                continue
            L += [f"### {TYPE_LABEL[t][lang]}", ""]
            for oid, v in rows:
                L.append(f"- [{v['title']}]({v['canonical_url']}) : {v['description']}")
            L.append("")
    if len(published_ids) == 0:
        L += ["## Aucune fiche publiée à ce jour", "",
              "Les 105 objets du catalogue sont en relecture (`status: review`).",
              "Ce fichier se remplira à mesure des validations — voir GOVERNANCE.md §2.", ""]
    open(os.path.join(public, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))

    # --- llms-full.txt (KC-L05) -------------------------------------------
    F = [f"# SOS-EcoVadis Knowledge Catalog — texte intégral",
         f"# Généré le {datetime.date.today().isoformat()} — ne pas éditer à la main.",
         f"# Licence : CC BY-NC 4.0 — citation avec attribution à ESG Interim Management.",
         ""]
    for oid in sorted(published_ids):
        o = objects[oid]
        for lang in LANGS:
            v = o["languages"].get(lang)
            if not v or not v["canonical_url"]:
                continue
            F += [f"<!-- {oid} [{lang}] {v['canonical_url']} "
                  f"maj {o['date_updated']} -->", bodies[(oid, lang)].strip(), ""]
    open(os.path.join(public, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(F))

    # --- rapport -----------------------------------------------------------
    nfiles = sum(len(o["languages"]) for o in objects.values())
    print(f"{len(objects)} objets / {nfiles} fichiers — 0 erreur")
    print(f"publiés : {len(published_ids)} ; en relecture : {len(objects)-len(published_ids)}")
    print(f"hubs : {len(hub_defs)} ; objets orphelins : 0")
    print(f"écrit : index/catalog.json, index/jsonld.json, "
          f"public/{{robots.txt, sitemap.xml, llms.txt, llms-full.txt}}")
    if len(published_ids) == 0:
        print("NOTE : aucune fiche publiée, donc sitemap et llms.txt sont vides. "
              "C'est le comportement voulu (décision D19).")

if __name__ == "__main__":
    main()
