#!/usr/bin/env python3
"""One-time migration of Pelican markdown -> Astro content collections.

Reads content/posts/**/*.md and content/pages/*.md (Pelican colon-style
metadata) and writes Astro-compatible YAML-frontmatter markdown into
src/content/blog/ and src/content/pages/.

Run once from the repo root: python3 scripts/migrate_content.py
"""
import re
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_OUT = ROOT / "src" / "content" / "blog"
PAGES_OUT = ROOT / "src" / "content" / "pages"


def parse_pelican(text: str):
    """Split a Pelican markdown file into (metadata dict, body)."""
    lines = text.splitlines()
    meta = {}
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            body_start = i + 1
            break
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            meta[m.group(1).lower()] = m.group(2).strip()
        else:
            # No more metadata lines; body begins here.
            body_start = i
            break
    body = "\n".join(lines[body_start:]).strip() + "\n"
    return meta, body


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def normalize_date(raw: str) -> str:
    raw = raw.strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    # Fallback: handle non-zero-padded like 2017-2-22
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", raw)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        return f"{y:04d}-{mo:02d}-{d:02d}"
    raise ValueError(f"Unrecognized date: {raw!r}")


def fix_body(body: str) -> str:
    # Old Pelican CodeHilite directive: a ``` fence whose first line is ":::lang"
    # -> put the language on the fence (```lang) and drop the ":::" line.
    body = re.sub(r"^```[ \t]*\n:::(\w+)[ \t]*\n", r"```\1\n", body, flags=re.M)

    # {static}/... -> /...
    body = body.replace("{static}/", "/")
    # {attach}foo.png -> /static/blog/foo.png  (co-located post images)
    body = body.replace("{attach}", "/static/blog/")

    # attr_list images: ![alt](url){align=right width=600px} -> raw <img>
    def img_repl(m):
        alt, url, attrs = m.group(1), m.group(2), m.group(3)
        style = "max-width: 100%;"
        if "align=right" in attrs:
            style = "float: right; margin: 0 0 1rem 1.5rem; " + style
        elif "align=left" in attrs:
            style = "float: left; margin: 0 1.5rem 1rem 0; " + style
        w = re.search(r"width=(\S+)", attrs)
        if w:
            style += f" width: {w.group(1)};"
        return f'<img src="{url}" alt="{alt}" style="{style}" />'

    body = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)\{([^}]*)\}", img_repl, body)
    return body


def build_frontmatter(meta: dict, *, is_post: bool) -> str:
    fm = ["---"]
    fm.append(f"title: {yaml_quote(meta['title'])}")
    if is_post:
        fm.append(f"date: {normalize_date(meta['date'])}")
        tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        if tags:
            fm.append("tags: [" + ", ".join(yaml_quote(t) for t in tags) + "]")
        else:
            fm.append("tags: []")
    fm.append(f"slug: {yaml_quote(meta['slug'])}")
    author = meta.get("author") or meta.get("authors") or "Pedro Rodriguez"
    fm.append(f"author: {yaml_quote(author)}")
    if meta.get("description"):
        fm.append(f"description: {yaml_quote(meta['description'])}")
    if meta.get("template"):
        fm.append(f"template: {yaml_quote(meta['template'])}")
    fm.append("---")
    return "\n".join(fm)


def migrate(src: Path, out_dir: Path, *, is_post: bool):
    meta, body = parse_pelican(src.read_text())
    slug = meta["slug"]
    frontmatter = build_frontmatter(meta, is_post=is_post)
    body = fix_body(body)
    # Posts -> named by slug; pages -> keep filename (slug may differ from file).
    name = slug if is_post else src.stem
    out_path = out_dir / f"{name}.md"
    out_path.write_text(frontmatter + "\n\n" + body)
    print(f"  {src.relative_to(ROOT)} -> {out_path.relative_to(ROOT)}")


def main():
    BLOG_OUT.mkdir(parents=True, exist_ok=True)
    PAGES_OUT.mkdir(parents=True, exist_ok=True)

    print("Posts:")
    for src in sorted((ROOT / "content" / "posts").rglob("*.md")):
        migrate(src, BLOG_OUT, is_post=True)

    print("Pages:")
    for src in sorted((ROOT / "content" / "pages").glob("*.md")):
        migrate(src, PAGES_OUT, is_post=False)

    # Co-located post images referenced via {attach} -> public/static/blog/
    blog_assets = ROOT / "public" / "static" / "blog"
    blog_assets.mkdir(parents=True, exist_ok=True)
    for png in (ROOT / "content" / "posts").rglob("*.png"):
        dest = blog_assets / png.name
        dest.write_bytes(png.read_bytes())
        print(f"  asset {png.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
