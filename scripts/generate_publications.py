#!/usr/bin/env python3
"""Generate src/data/publications.ts from src/data/publications.bib.

Ports the bucketing / author-formatting logic from the old Pelican plugin
(plugins/pubs.py) into a static, type-checked TS data file. Run once (or
whenever publications.bib changes):

    python3 scripts/generate_publications.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "src" / "data" / "publications.bib"
OUT = ROOT / "src" / "data" / "publications.ts"

# (type field value, section key, heading) in display order — mirrors pubs.py.
SECTIONS = [
    ("thesis", "thesis", "PhD Thesis"),
    ("publication", "publications", "Conference and Journal Papers"),
    ("arxiv", "arxiv", "arXiv"),
    ("workshop", "workshops", "Workshop Papers"),
    ("non-refereed", "nonRefereed", "Non-Refereed"),
    ("media", "media", "Media"),
    ("project", "projects", "Course Projects"),
]


def parse_entries(text: str):
    """Yield (entry_type, key, fields dict) for each @entry in the bib text."""
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        entry_type = text[at + 1 : brace].strip().lower()
        # Walk braces to find the matching close.
        depth = 0
        j = brace
        while j < n:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[brace + 1 : j]
        i = j + 1

        key, _, rest = body.partition(",")
        yield entry_type, key.strip(), parse_fields(rest)


def parse_fields(rest: str):
    """Parse `key = {value}` / `key = "value"` / `key = value` fields."""
    fields = {}
    i = 0
    n = len(rest)
    while i < n:
        m = re.match(r"\s*([A-Za-z_]+)\s*=\s*", rest[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= n:
            break
        ch = rest[i]
        if ch == "{":
            depth = 0
            start = i
            while i < n:
                if rest[i] == "{":
                    depth += 1
                elif rest[i] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            value = rest[start + 1 : i]
            i += 1  # skip closing brace
        elif ch == '"':
            start = i + 1
            i = start
            while i < n and rest[i] != '"':
                i += 1
            value = rest[start:i]
            i += 1
        else:
            start = i
            while i < n and rest[i] not in ",\n":
                i += 1
            value = rest[start:i].strip()
        fields[name] = value.strip()
        # advance past trailing comma/whitespace
        while i < n and rest[i] in ", \n\t":
            i += 1
    return fields


def fix_unicode(s: str) -> str:
    return s.replace("Joao", "João")


def strip_braces(s: str) -> str:
    return s.replace("{", "").replace("}", "")


def authors_list(raw: str):
    return [fix_unicode(a.strip()) for a in raw.split(" and ") if a.strip()]


def source_of(fields: dict) -> str:
    for k in ("booktitle", "journal", "school"):
        if k in fields:
            return fix_unicode(strip_braces(fields[k]))
    return ""


def rebuild_bibtex(entry_type: str, key: str, fields: dict) -> str:
    """Recreate a clean single-entry BibTeX string, dropping the `type` field."""
    lines = [f"@{entry_type}{{{key},"]
    for name, value in fields.items():
        if name in ("type", "award", "code"):
            continue
        lines.append(f"  {name} = {{{value}}},")
    lines.append("}")
    return "\n".join(lines)


def main():
    text = BIB.read_text()
    buckets = {key: [] for _, key, _ in SECTIONS}
    type_to_key = {t: key for t, key, _ in SECTIONS}

    total = 0
    for entry_type, key, fields in parse_entries(text):
        ptype = fields.get("type")
        if ptype not in type_to_key:
            print(f"  WARNING: skipping {key!r} with unknown type {ptype!r}")
            continue
        entry = {
            "id": "@" + key,
            "authors": authors_list(fields.get("author", "")),
            "title": fix_unicode(strip_braces(fields.get("title", "")).strip()),
            "url": fields.get("url", ""),
            "source": source_of(fields),
            "year": fields.get("year", ""),
            "award": fix_unicode(fields.get("award", "").strip()),
            "code": fields.get("code", "").strip(),
            "bibtex": rebuild_bibtex(entry_type, key, fields),
        }
        buckets[type_to_key[ptype]].append(entry)
        total += 1

    sections = [
        {"key": key, "heading": heading, "entries": buckets[key]}
        for _, key, heading in SECTIONS
        if buckets[key]
    ]

    body = json.dumps(sections, indent=2, ensure_ascii=False)
    ts = (
        "// AUTO-GENERATED by scripts/generate_publications.py from\n"
        "// src/data/publications.bib — do not edit by hand.\n\n"
        "export interface PubEntry {\n"
        "  id: string;\n"
        "  authors: string[];\n"
        "  title: string;\n"
        "  url: string;\n"
        "  source: string;\n"
        "  year: string;\n"
        "  award: string;\n"
        "  code: string;\n"
        "  bibtex: string;\n"
        "}\n\n"
        "export interface PubSection {\n"
        "  key: string;\n"
        "  heading: string;\n"
        "  entries: PubEntry[];\n"
        "}\n\n"
        f"export const publicationSections: PubSection[] = {body};\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(ts)
    print(f"Wrote {OUT.relative_to(ROOT)} with {total} entries in {len(sections)} sections.")


if __name__ == "__main__":
    main()
