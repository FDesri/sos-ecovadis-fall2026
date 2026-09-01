#!/usr/bin/env python3
import json, os, re, yaml

REPO = "/home/claude/sos-ecovadis-fall2026"
inv = json.load(open('/home/claude/kc/inventory.json'))

# collect front matter of canonical files (en + the mul glossary)
meta = {}
for root, _d, files in os.walk(os.path.join(REPO, "catalog")):
    for f in files:
        if not f.endswith(".md"): continue
        text = open(os.path.join(root, f), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m: continue
        fm = yaml.safe_load(m.group(1))
        if fm.get("lang") in ("en", "mul"):
            meta[fm["id"]] = fm

L = []
L.append("# SOURCES — Registre des sources du catalogue")
L.append("")
L.append("Registre de traçabilité : chaque objet de connaissance (kb-XXXX) ← note source Evernote ← corpus propriétaire ESGIM.")
L.append("")
L.append("## Corpus source")
L.append("")
L.append("- **Origine unique :** corpus propriétaire ESGIM (notes Evernote de François Dequenne — rédactions personnelles et captures retravaillées, sans distinction de statut ; décision de gouvernance du 27/08/2026, voir GOVERNANCE.md §7).")
L.append("- **Livraison :** export Evernote « Evernote notes sosecovadis repository v1.zip » (remis le 27/08/2026), 37 notes uniques après déduplication (les versions les plus récentes font foi). Les fichiers ENEX originaux restent dans l'Evernote / le Drive de François Dequenne.")
L.append("- **Parsing :** `scripts/parse_enex.py` (ENEX → markdown).")
L.append("- **Glossaire :** document projet Claude « glossaire-ecovadis-en-fr-nl.md » v2.0 — référence terminologique de toutes les traductions.")
L.append("- **Codes questions :** « Exemple de questionnaire de réévaluation entreprise manufacturière taille S » (xlsx, projet) → `taxonomy/ecovadis-question-codes.json` (46 codes).")
L.append("")
L.append("## Objets fondation (kb-0001 → kb-0005)")
L.append("")
L.append("| ID | Type | Note source (Evernote) | Langue src | Fiche canonique |")
L.append("|---|---|---|---|---|")
for k in sorted(inv):
    if k.startswith("_"): continue
    v = inv[k]
    if not (k <= "kb-0005"): continue
    fm = meta.get(k, {})
    lang_dir = "mul" if v["src_lang"] == "mul" else "en"
    slug = v["slugs"].get("en") or v["slugs"].get("mul", "")
    L.append(f"| {k} | {v['type']} | {v['src']} | {v['src_lang']} | `{slug}` |")
L.append("")
L.append("## Articles (kb-0010 → kb-0041)")
L.append("")
L.append("| ID | Note source (Evernote) | Langue src | Fiche canonique (EN) | Remarques |")
L.append("|---|---|---|---|---|")
remarks = {
    "kb-0019": "chiffres seuils = estimations datées",
    "kb-0020": "benchmarks publics conservés ; estimations datées, à recouper avec kb-0016",
    "kb-0022": "« 600+ » corrigé en « 100+ »",
    "kb-0023": "cas clients anonymisés (à valider — cf. GOVERNANCE §7)",
    "kb-0027": "sections prospection/personnes approchées retirées (repo public)",
    "kb-0031": "« 600+ » corrigé en « 100+ »",
    "kb-0034": "exemple client anonymisé (imprimeur flexo wallon S)",
    "kb-0035": "exemple client anonymisé (idem kb-0034)",
    "kb-0038": "nom du client retiré du titre et du contenu",
    "kb-0039": "exemple client anonymisé (idem kb-0034)",
}
for k in sorted(inv):
    if k.startswith("_") or not k.startswith("kb-00"): continue
    if not ("kb-0010" <= k <= "kb-0041"): continue
    v = inv[k]
    L.append(f"| {k} | {v['src']} | {v['src_lang']} | `{v['slugs']['en']}` | {remarks.get(k, '—')} |")
L.append("")
L.append("## FAQ (kb-0100 → kb-0167)")
L.append("")
L.append("68 objets FAQ issus du découpage de trois notes source (une question humaine = un objet autonome ; doublons entre notes fusionnés) :")
L.append("")
L.append("| Note source | Objets dérivés |")
L.append("|---|---|")
L.append("| FAQ 2025.md (webinaires ESG 2025) | kb-0100 → kb-0113 (kb-0100 fusionne aussi la règle « 55 par cycle » de FAQ 2026 (2)) |")
L.append("| EcoVadis FAQ 2026 (1).md | kb-0114 → kb-0160 (« 600+ » de l'intro corrigé en « 100+ » ; liens externes nexioprojects remplacés par des slugs internes) |")
L.append("| EcoVadis FAQ 2026 (2).md | kb-0161 → kb-0167 ; réponses redondantes fusionnées dans kb-0100, kb-0122, kb-0128, kb-0138, kb-0140, kb-0153, kb-0154, kb-0159 |")
L.append("")
L.append("Le champ `source_note` du front matter de chaque fiche précise la ou les notes d'origine. La liste question par question est reconstructible depuis `scripts/faq_data_*.py` (fichiers de génération, champ `source_note`).")
L.append("")
L.append("## Notes source non transformées")
L.append("")
L.append("| Note | Raison |")
L.append("|---|---|")
L.append("| Author identity (wout picture).md | intégrée dans kb-0002 (fiche expert) |")
L.append("| Risques environnementaux externes ENV7003 (v1) | remplacée par la v2 (kb-0032) |")
L.append("| Doublons du ZIP (versions antérieures) | versions les plus récentes retenues |")
L.append("")
open(os.path.join(REPO, "SOURCES.md"), "w", encoding="utf-8").write("\n".join(L))
print("SOURCES.md written,", len(L), "lines")
