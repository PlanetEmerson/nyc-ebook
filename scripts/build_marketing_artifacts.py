#!/usr/bin/env python3
"""Rebuild shared marketing SEO artifacts from the static site source."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape as xml_escape

from PIL import Image


SITE_ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://fbemerson.com"
BLOG_DIR = SITE_ROOT / "new-york" / "blog"
POSTS_JSON = BLOG_DIR / "posts.json"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"
LLMS_FILE = SITE_ROOT / "llms.txt"
RSS_FILE = BLOG_DIR / "feed.xml"
BLOG_TEMPLATE = BLOG_DIR / "_template.html"


FRENCH_MONTHS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
}


STATIC_ROUTES = [
    ("index.html", "/", "monthly", "1.0"),
    ("a-propos/index.html", "/a-propos/", "monthly", "0.7"),
    ("newsletter/index.html", "/newsletter/", "monthly", "0.6"),
    ("new-york/index.html", "/new-york/", "weekly", "0.9"),
    ("new-york/contact/index.html", "/new-york/contact/", "monthly", "0.5"),
    ("new-york/blog/index.html", "/new-york/blog/", "weekly", "0.8"),
    ("new-york/premier-voyage/index.html", "/new-york/premier-voyage/", "monthly", "0.8"),
]


CORE_ASSET_MAP = {
    "images/book/cover.jpg": "images/book/cover.webp",
    "images/sections/author-desk.png": "images/sections/author-desk.webp",
    "images/hero/hero-main.jpg": "images/hero/hero-main.webp",
    "images/sections/warning.jpg": "images/sections/warning.webp",
    "images/sections/final-cta.jpg": "images/sections/final-cta.webp",
    "images/blog/cta-background.jpg": "images/blog/cta-background.webp",
}


HOME_PREVIEW_START = "<!-- GENERATED_HOME_BLOG_PREVIEW_START -->"
HOME_PREVIEW_END = "<!-- GENERATED_HOME_BLOG_PREVIEW_END -->"
BOOK_PREVIEW_START = "<!-- GENERATED_BOOK_BLOG_PREVIEW_START -->"
BOOK_PREVIEW_END = "<!-- GENERATED_BOOK_BLOG_PREVIEW_END -->"
BLOG_INDEX_START = "<!-- GENERATED_BLOG_INDEX_START -->"
BLOG_INDEX_END = "<!-- GENERATED_BLOG_INDEX_END -->"
BLOG_ITEMLIST_START = "<!-- GENERATED_BLOG_ITEMLIST_START -->"
BLOG_ITEMLIST_END = "<!-- GENERATED_BLOG_ITEMLIST_END -->"
RELATED_START = "<!-- GENERATED_RELATED_POSTS_START -->"
RELATED_END = "<!-- GENERATED_RELATED_POSTS_END -->"


@dataclass
class Post:
    title: str
    description: str
    slug: str
    date_display: str
    date_dt: datetime
    date_iso: str
    category: str
    tags: list[str]
    file_path: Path
    url: str
    lastmod: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def trim_meta_description(text: str, limit: int = 155) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= limit:
        return clean
    clipped = clean[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:-")
    return f"{clipped}…"


def parse_french_date(date_display: str) -> datetime:
    parts = date_display.strip().split(" ")
    if len(parts) != 3:
        raise ValueError(f"Unsupported date format: {date_display}")
    day = int(parts[0])
    month = FRENCH_MONTHS[parts[1].lower()]
    year = int(parts[2])
    return datetime(year, month, day, tzinfo=timezone.utc)


def load_posts() -> list[Post]:
    raw_posts = json.loads(read_text(POSTS_JSON))
    posts: list[Post] = []
    for raw in raw_posts:
        slug = raw["slug"]
        file_path = BLOG_DIR / slug / "index.html"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing blog post HTML for slug {slug}")
        date_dt = parse_french_date(raw["date"])
        lastmod = datetime.fromtimestamp(file_path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
        posts.append(
            Post(
                title=raw["title"],
                description=raw["description"],
                slug=slug,
                date_display=raw["date"],
                date_dt=date_dt,
                date_iso=date_dt.strftime("%Y-%m-%d"),
                category=raw["category"],
                tags=list(raw.get("tags", [])),
                file_path=file_path,
                url=f"{SITE_URL}/new-york/blog/{slug}/",
                lastmod=lastmod,
            )
        )
    posts.sort(key=lambda post: post.date_dt, reverse=True)
    return posts


def ensure_webp_assets() -> None:
    for src_str, target_str in CORE_ASSET_MAP.items():
        src = SITE_ROOT / src_str
        target = SITE_ROOT / target_str
        if not src.exists():
            continue
        if target.exists() and target.stat().st_mtime >= src.stat().st_mtime:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as image:
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            image.save(target, format="WEBP", quality=82, method=6)


def replace_between_markers(content: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(?P<indent>^[ \t]*){re.escape(start)}.*?^[ \t]*{re.escape(end)}",
        re.S | re.M,
    )
    match = pattern.search(content)
    if not match:
        raise ValueError(f"Missing marker block: {start}")
    indent = match.group("indent")
    block = f"{indent}{start}\n{replacement}\n{indent}{end}"
    return pattern.sub(block, content, count=1)


def render_home_blog_preview(posts: Iterable[Post]) -> str:
    lines = []
    for post in list(posts)[:3]:
        lines.extend(
            [
                f'                <a href="/new-york/blog/{post.slug}/" class="blog-preview-item">',
                f'                    <span class="blog-preview-category">{escape(post.category)}</span>',
                f'                    <span class="blog-preview-title">{escape(post.title)}</span>',
                "                </a>",
            ]
        )
    return "\n".join(lines)


def render_book_blog_preview(posts: Iterable[Post]) -> str:
    lines = []
    for post in list(posts)[:3]:
        lines.extend(
            [
                f'                    <a href="/new-york/blog/{post.slug}/" class="blog-preview-card">',
                '                        <div class="blog-preview-card-image">',
                f'                            <img src="/new-york/blog/{post.slug}/featured.jpg" alt="{escape(post.title)}" width="400" height="225" loading="lazy">',
                "                        </div>",
                '                        <div class="blog-preview-card-content">',
                '                            <div class="blog-preview-card-meta">',
                f'                                <span class="blog-preview-card-category">{escape(post.category)}</span>',
                f'                                <span>{escape(post.date_display)}</span>',
                "                            </div>",
                f'                            <h3>{escape(post.title)}</h3>',
                f'                            <p>{escape(post.description)}</p>',
                "                        </div>",
                "                    </a>",
            ]
        )
    return "\n".join(lines)


def render_blog_index_cards(posts: Iterable[Post]) -> str:
    lines = []
    for post in posts:
        lines.extend(
            [
                f'                <a href="/new-york/blog/{post.slug}/" class="blog-card">',
                '                    <div class="blog-card-image">',
                f'                        <img src="/new-york/blog/{post.slug}/featured.jpg" alt="{escape(post.title)}" width="400" height="225" loading="lazy">',
                "                    </div>",
                '                    <div class="blog-card-content">',
                '                        <div class="blog-card-meta">',
                f'                            <span class="blog-card-category">{escape(post.category)}</span>',
                "                            <span>•</span>",
                f'                            <span>{escape(post.date_display)}</span>',
                "                        </div>",
                f'                        <h2>{escape(post.title)}</h2>',
                f'                        <p>{escape(post.description)}</p>',
                "                    </div>",
                "                </a>",
            ]
        )
    return "\n".join(lines)


def render_blog_itemlist_schema(posts: Iterable[Post]) -> str:
    items = [
        {
            "@type": "ListItem",
            "position": index,
            "item": {
                "@type": "BlogPosting",
                "headline": post.title,
                "url": post.url,
            },
        }
        for index, post in enumerate(posts, start=1)
    ]
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Articles du blog New York de F.B. Emerson",
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "numberOfItems": len(items),
        "itemListElement": items,
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=4) + "\n    </script>"


def select_related_posts(current: Post, posts: list[Post]) -> list[Post]:
    same_category = [post for post in posts if post.slug != current.slug and post.category == current.category]
    remainder = [post for post in posts if post.slug != current.slug and post.category != current.category]
    selected = (same_category + remainder)[:3]
    return selected


def render_related_cards(current: Post, posts: list[Post]) -> str:
    related = select_related_posts(current, posts)
    lines = []
    for post in related:
        lines.extend(
            [
                f'            <a href="/new-york/blog/{post.slug}/" class="related-card">',
                f'                <img src="/new-york/blog/{post.slug}/featured.jpg" alt="{escape(post.title)}" width="320" height="180" loading="lazy">',
                '                <div class="related-card-content">',
                f'                    <p class="related-card-category">{escape(post.category)}</p>',
                f'                    <h3>{escape(post.title)}</h3>',
                "                </div>",
                "            </a>",
            ]
        )
    return "\n".join(lines)


def render_rss(posts: list[Post]) -> str:
    last_build = format_datetime(datetime.now(timezone.utc))
    items = []
    for post in posts[:15]:
        items.append(
            f"""    <item>
      <title>{xml_escape(post.title)}</title>
      <link>{post.url}</link>
      <description>{xml_escape(post.description)}</description>
      <pubDate>{format_datetime(post.date_dt)}</pubDate>
      <guid>{post.url}</guid>
    </item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Blog New York — F.B. Emerson</title>
    <link>{SITE_URL}/new-york/blog/</link>
    <description>Découvrez New York autrement. Secrets de quartiers, réflexions de voyage, et les coulisses du livre New York, Mon Éveil.</description>
    <language>fr-fr</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{SITE_URL}/new-york/blog/feed.xml" rel="self" type="application/rss+xml"/>

{chr(10).join(items)}
  </channel>
</rss>
"""


def render_sitemap(posts: list[Post]) -> str:
    entries = []
    for file_rel, url_path, changefreq, priority in STATIC_ROUTES:
        file_path = SITE_ROOT / file_rel
        if not file_path.exists():
            continue
        lastmod = datetime.fromtimestamp(file_path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
        entries.append((f"{SITE_URL}{url_path}", lastmod, changefreq, priority))
    for post in posts:
        entries.append((post.url, post.lastmod, "monthly", "0.8"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, priority in entries:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def render_llms(posts: list[Post]) -> str:
    lines = [
        "# F.B. Emerson — Auteure",
        "",
        "> F.B. Emerson est une auteure française installée à Amsterdam, connue pour « New York, Mon Éveil », un récit personnel sur New York, le voyage et la transformation.",
        "",
        "## Pages principales",
        f"- [Accueil]({SITE_URL}/): Site officiel de F.B. Emerson",
        f"- [New York, Mon Éveil]({SITE_URL}/new-york/): Le livre, ses extraits et l'achat",
        f"- [Premier voyage à New York]({SITE_URL}/new-york/premier-voyage/): Guide de lecture pour un premier séjour",
        f"- [À propos]({SITE_URL}/a-propos/): Biographie et contexte de l'auteure",
        f"- [Blog]({SITE_URL}/new-york/blog/): Articles sur New York, ses quartiers et ses saisons",
        f"- [Newsletter]({SITE_URL}/newsletter/): Inscription pour recevoir extraits et coulisses",
        "",
        "## Faits clés",
        "- Nom canonique : F.B. Emerson",
        "- Métier : auteure",
        "- Langue : français",
        "- Ville de référence : New York City",
        "- Livre principal : « New York, Mon Éveil »",
        "",
        "## Articles récents",
    ]
    for post in posts[:8]:
        lines.append(f"- [{post.title}]({post.url}): {post.description}")
    lines.append("")
    return "\n".join(lines)


def patch_home_page(posts: list[Post]) -> None:
    path = SITE_ROOT / "index.html"
    content = read_text(path)
    content = replace_between_markers(content, HOME_PREVIEW_START, HOME_PREVIEW_END, render_home_blog_preview(posts))
    content = content.replace("images/book/cover.jpg", "images/book/cover.webp")
    write_text(path, content)


def patch_book_page(posts: list[Post]) -> None:
    path = SITE_ROOT / "new-york" / "index.html"
    content = read_text(path)
    content = replace_between_markers(content, BOOK_PREVIEW_START, BOOK_PREVIEW_END, render_book_blog_preview(posts))
    content = re.sub(
        r"\n\s*// Load blog posts preview.*?loadBlogPreview\(\);\n",
        "\n",
        content,
        count=1,
        flags=re.S,
    )
    content = content.replace("../images/hero/hero-main.jpg", "../images/hero/hero-main.webp")
    content = content.replace("../images/sections/warning.jpg", "../images/sections/warning.webp")
    content = content.replace("../images/sections/final-cta.jpg", "../images/sections/final-cta.webp")
    content = content.replace("../images/book/cover.jpg", "../images/book/cover.webp")
    content = content.replace("/images/textures/paper.png", "/images/textures/paper.webp")
    write_text(path, content)


def patch_blog_index(posts: list[Post]) -> None:
    path = SITE_ROOT / "new-york" / "blog" / "index.html"
    content = read_text(path)
    content = replace_between_markers(content, BLOG_INDEX_START, BLOG_INDEX_END, render_blog_index_cards(posts))
    content = replace_between_markers(content, BLOG_ITEMLIST_START, BLOG_ITEMLIST_END, render_blog_itemlist_schema(posts))
    content = re.sub(
        r"\n\s*// Load blog posts.*?loadPosts\(\);\n",
        "\n",
        content,
        count=1,
        flags=re.S,
    )
    content = content.replace("../../images/textures/hero-texture.png", "../../images/textures/hero-texture.webp")
    content = content.replace("../../images/textures/grain.png", "../../images/textures/grain.webp")
    content = content.replace("../../images/blog/cta-background.jpg", "../../images/blog/cta-background.webp")
    content = content.replace("/images/textures/paper.png", "/images/textures/paper.webp")
    write_text(path, content)


def patch_blog_post(path: Path, post: Post, posts: list[Post]) -> None:
    content = read_text(path)
    seo_title = f"{post.title} | F.B. Emerson"
    meta_description = trim_meta_description(post.description)
    content = re.sub(r"<title>.*?</title>", f"<title>{escape(seo_title)}</title>", content, count=1, flags=re.S)
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escape(meta_description)}">',
        content,
        count=1,
    )
    content = re.sub(r"\n\s*<meta name=\"keywords\" content=\"[^\"]*\">\n", "\n", content, count=1)
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{escape(meta_description)}">',
        content,
        count=1,
    )
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{escape(meta_description)}">',
        content,
        count=1,
    )

    if RELATED_START not in content:
        content = re.sub(
            r'(<div class="related-grid" id="related-posts">\s*)(.*?)(\s*</div>\s*\n\s*<div class="related-more">)',
            rf'\1            {RELATED_START}\n            {RELATED_END}\n\3',
            content,
            count=1,
            flags=re.S,
        )
    content = replace_between_markers(content, RELATED_START, RELATED_END, render_related_cards(post, posts))
    content = re.sub(
        r"\n\s*// Load related posts.*?loadRelated\(\);\n",
        "\n",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r"<aside class=\"inline-book-cta\">.*?</aside>",
        (
            '<aside class="inline-book-cta">\n'
            '    <p><em>Ce sujet est au cœur de <a href="/new-york/">New York, Mon Éveil</a>.</em> '
            '<a href="/new-york/">Découvrir le livre →</a></p>\n'
            "</aside>"
        ),
        content,
        count=1,
        flags=re.S,
    )

    content = content.replace("../../../images/textures/grain.png", "../../../images/textures/grain.webp")
    content = content.replace("/images/textures/paper.png", "/images/textures/paper.webp")
    content = content.replace("/images/sections/author-desk.png", "/images/sections/author-desk.webp")
    content = content.replace("/images/book/cover.jpg", "/images/book/cover.webp")
    write_text(path, content)


def patch_blog_template(posts: list[Post]) -> None:
    placeholder_post = posts[0]
    content = read_text(BLOG_TEMPLATE)
    content = re.sub(r"<title>.*?</title>", "<title>{{TITLE}} | F.B. Emerson</title>", content, count=1, flags=re.S)
    content = re.sub(r"\n\s*<meta name=\"keywords\" content=\"[^\"]*\">\n", "\n", content, count=1)
    if RELATED_START not in content:
        content = re.sub(
            r'(\s*<div class="related-grid" id="related-posts">\s*)(?:<!-- Dynamically loaded -->\s*)?(</div>)',
            rf'\1{RELATED_START}\n{RELATED_END}\n        \2',
            content,
            count=1,
            flags=re.S,
        )
    content = replace_between_markers(content, RELATED_START, RELATED_END, render_related_cards(placeholder_post, posts))
    content = re.sub(
        r"\n\s*// Load related posts.*?loadRelated\(\);\n",
        "\n",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(
        r"<aside class=\"inline-book-cta\">.*?</aside>",
        (
            '<aside class="inline-book-cta">\n'
            '    <p><em>Ce sujet est au cœur de <a href="/new-york/">New York, Mon Éveil</a>.</em> '
            '<a href="/new-york/">Découvrir le livre →</a></p>\n'
            "</aside>"
        ),
        content,
        count=1,
        flags=re.S,
    )
    content = content.replace("../../../images/textures/grain.png", "../../../images/textures/grain.webp")
    content = content.replace("/images/textures/paper.png", "/images/textures/paper.webp")
    content = content.replace("/images/sections/author-desk.png", "/images/sections/author-desk.webp")
    content = content.replace("/images/book/cover.jpg", "/images/book/cover.webp")
    write_text(BLOG_TEMPLATE, content)


def main() -> None:
    ensure_webp_assets()
    posts = load_posts()

    patch_home_page(posts)
    patch_book_page(posts)
    patch_blog_index(posts)
    patch_blog_template(posts)
    for post in posts:
        patch_blog_post(post.file_path, post, posts)

    write_text(RSS_FILE, render_rss(posts))
    write_text(SITEMAP_FILE, render_sitemap(posts))
    write_text(LLMS_FILE, render_llms(posts))


if __name__ == "__main__":
    main()
