#!/usr/bin/env python3
"""Validate required SEO signals for the static marketing site."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://fbemerson.com"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"


REQUIRED_SCHEMAS = {
    "/": ["\"@type\": \"Person\"", "\"@type\": \"WebSite\""],
    "/a-propos/": ["\"@type\": \"AboutPage\"", "\"@type\": \"BreadcrumbList\""],
    "/newsletter/": ["\"@type\": \"WebPage\"", "\"@type\": \"BreadcrumbList\""],
    "/new-york/": ["\"@type\": \"Book\"", "\"@type\": \"FAQPage\"", "\"@type\": \"BreadcrumbList\""],
    "/new-york/contact/": ["\"@type\": \"ContactPage\"", "\"@type\": \"BreadcrumbList\""],
    "/new-york/blog/": ["\"@type\": \"Blog\"", "\"@type\": \"BreadcrumbList\"", "\"@type\": \"ItemList\""],
    "/new-york/premier-voyage/": ["\"@type\": \"CollectionPage\"", "\"@type\": \"BreadcrumbList\""],
}


def page_url(path: Path) -> str:
    rel = path.relative_to(SITE_ROOT).as_posix()
    if rel == "index.html":
        return "/"
    return f"/{rel[:-10].rstrip('/')}/"


def is_indexable(content: str) -> bool:
    robots_match = re.search(r'<meta name="robots" content="([^"]+)"', content)
    if not robots_match:
        return True
    return "noindex" not in robots_match.group(1)


def load_sitemap_urls() -> set[str]:
    tree = ET.parse(SITEMAP_FILE)
    root = tree.getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {elem.text for elem in root.findall(".//sm:loc", namespace)}


def require(pattern: str, content: str, path: Path, errors: list[str], label: str) -> None:
    if not re.search(pattern, content, flags=re.S):
        errors.append(f"{path.relative_to(SITE_ROOT)}: missing {label}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SITEMAP_FILE.exists():
        errors.append("sitemap.xml is missing")
        sitemap_urls = set()
    else:
        sitemap_urls = load_sitemap_urls()

    for required_path in [
        SITE_ROOT / "llms.txt",
        SITE_ROOT / "new-york" / "blog" / "feed.xml",
        SITE_ROOT / "scripts" / "build_marketing_artifacts.py",
    ]:
        if not required_path.exists():
            errors.append(f"Missing required artifact: {required_path.relative_to(SITE_ROOT)}")

    html_files = sorted(path for path in SITE_ROOT.rglob("index.html") if ".git" not in path.parts and "build" not in path.parts)
    for path in html_files:
        content = path.read_text(encoding="utf-8")
        route = page_url(path)
        indexable = is_indexable(content)

        require(r"<title>.+?</title>", content, path, errors, "title tag")
        require(r'<meta name="description" content="[^"]+">', content, path, errors, "meta description")
        require(r'<link rel="canonical" href="https://fbemerson\.com[^"]*">', content, path, errors, "canonical")
        if indexable:
            require(r'twitter:card', content, path, errors, "twitter card")
            require(r'property="og:title"', content, path, errors, "og:title")

        if 'meta name="keywords"' in content:
            errors.append(f"{path.relative_to(SITE_ROOT)}: contains deprecated meta keywords tag")
        if "fetch('/new-york/blog/posts.json')" in content:
            errors.append(f"{path.relative_to(SITE_ROOT)}: still replaces server-rendered content via posts.json fetch")
        if "application/ld+json" not in content and indexable:
            errors.append(f"{path.relative_to(SITE_ROOT)}: missing JSON-LD")

        title_match = re.search(r"<title>(.*?)</title>", content, re.S)
        if title_match and len(title_match.group(1).strip()) > 75:
            warnings.append(f"{path.relative_to(SITE_ROOT)}: title longer than 75 characters")
        description_match = re.search(r'<meta name="description" content="([^"]*)">', content)
        if description_match and len(unescape(description_match.group(1)).strip()) > 160:
            warnings.append(f"{path.relative_to(SITE_ROOT)}: meta description longer than 160 characters")

        if indexable:
            if f"{SITE_URL}{route}" not in sitemap_urls:
                errors.append(f"{path.relative_to(SITE_ROOT)}: indexable page missing from sitemap")

            if route.startswith("/new-york/blog/") and route != "/new-york/blog/":
                for schema in ['"@type": "BlogPosting"', '"@type": "BreadcrumbList"']:
                    if schema not in content:
                        errors.append(f"{path.relative_to(SITE_ROOT)}: missing schema {schema}")
            elif route in REQUIRED_SCHEMAS:
                for schema in REQUIRED_SCHEMAS[route]:
                    if schema not in content:
                        errors.append(f"{path.relative_to(SITE_ROOT)}: missing schema {schema}")

    if errors:
        print("SEO validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        if warnings:
            print("\nWarnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  - {warning}", file=sys.stderr)
        return 1

    print("SEO validation passed.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
