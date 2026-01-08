#!/usr/bin/env python3
"""
Blog Builder for fbemerson.com/new-york/blog/
Takes n8n JSON output and generates blog posts in French.

Usage:
    python3 build_blog.py path/to/post.json
    python3 build_blog.py --from-n8n '{"frontmatter": "...", "article": "..."}'
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuration
BLOG_DIR = Path(__file__).parent / "new-york" / "blog"
POSTS_JSON = BLOG_DIR / "posts.json"
TEMPLATE_FILE = BLOG_DIR / "_template.html"

# French month names
FRENCH_MONTHS = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "août",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
}


def parse_frontmatter(frontmatter_str: str) -> dict:
    """Parse YAML frontmatter string into dict."""
    result = {}
    for line in frontmatter_str.strip().split('\n'):
        if line.startswith('---'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Handle arrays like [tag1, tag2]
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
            # Remove quotes
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            result[key] = value
    return result


def markdown_to_html(markdown: str) -> str:
    """Convert markdown to HTML."""
    html = markdown

    # Remove H1 (title is in header)
    html = re.sub(r'^# .+\n', '', html, flags=re.MULTILINE)

    # H2 and H3
    html = re.sub(r'^## (.+)$', r'<h2 id="\1">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Clean up H2 IDs (lowercase, hyphenated, French-safe)
    def clean_id(match):
        text = match.group(1)
        # Remove accents for ID
        import unicodedata
        id_text = unicodedata.normalize('NFD', text)
        id_text = ''.join(c for c in id_text if unicodedata.category(c) != 'Mn')
        id_text = re.sub(r'[^a-zA-Z0-9\s]', '', id_text).lower().replace(' ', '-')
        return f'<h2 id="{id_text}">{text}</h2>'
    html = re.sub(r'<h2 id="[^"]+">(.+)</h2>', clean_id, html)

    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)

    # Lists (simple)
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    html = '\n'.join(result)

    # Paragraphs - wrap text blocks
    paragraphs = []
    current = []
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            if current:
                text = ' '.join(current)
                if not any(text.startswith(f'<{tag}') for tag in ['h2', 'h3', 'ul', 'ol', 'blockquote', 'aside']):
                    text = f'<p>{text}</p>'
                paragraphs.append(text)
                current = []
        else:
            if line.startswith('<h') or line.startswith('<ul') or line.startswith('<ol') or line.startswith('<blockquote') or line.startswith('</'):
                if current:
                    text = ' '.join(current)
                    if not any(text.startswith(f'<{tag}') for tag in ['h2', 'h3', 'ul', 'ol', 'blockquote']):
                        text = f'<p>{text}</p>'
                    paragraphs.append(text)
                    current = []
                paragraphs.append(line)
            else:
                current.append(line)
    if current:
        text = ' '.join(current)
        if not any(text.startswith(f'<{tag}') for tag in ['h2', 'h3', 'ul', 'ol', 'blockquote']):
            text = f'<p>{text}</p>'
        paragraphs.append(text)

    return '\n\n'.join(paragraphs)


def format_date_french(date_str: str) -> str:
    """Format date as '8 janvier 2026' (French)."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        day = dt.day
        month = FRENCH_MONTHS[dt.month]
        year = dt.year
        return f'{day} {month} {year}'
    except:
        return date_str


def build_post(data: dict) -> None:
    """Build a blog post from n8n data."""
    # Parse frontmatter
    fm = parse_frontmatter(data['frontmatter'])

    # Extract values
    title = fm.get('title', 'Sans titre')
    description = fm.get('description', '')
    slug = fm.get('slug', title.lower().replace(' ', '-'))
    date = fm.get('date', datetime.now().strftime('%Y-%m-%d'))
    date_formatted = format_date_french(date)
    category = fm.get('category', 'Général')
    tags = fm.get('tags', [])
    keyword = data.get('keyword', title)

    # Convert markdown to HTML
    content = markdown_to_html(data['article'])

    # Read template
    template = TEMPLATE_FILE.read_text()

    # Replace placeholders
    html = template
    html = html.replace('{{TITLE}}', title)
    html = html.replace('{{DESCRIPTION}}', description)
    html = html.replace('{{SLUG}}', slug)
    html = html.replace('{{DATE}}', date)
    html = html.replace('{{DATE_FORMATTED}}', date_formatted)
    html = html.replace('{{CATEGORY}}', category)
    html = html.replace('{{KEYWORD}}', keyword)
    html = html.replace('{{CONTENT}}', content)

    # Create post directory
    post_dir = BLOG_DIR / slug
    post_dir.mkdir(exist_ok=True)

    # Write HTML
    (post_dir / 'index.html').write_text(html)
    print(f"Créé: {post_dir / 'index.html'}")

    # Update posts.json
    posts = json.loads(POSTS_JSON.read_text()) if POSTS_JSON.exists() else []

    # Remove existing post with same slug
    posts = [p for p in posts if p.get('slug') != slug]

    # Add new post at beginning
    posts.insert(0, {
        'title': title,
        'description': description,
        'slug': slug,
        'date': date_formatted,
        'category': category,
        'tags': tags if isinstance(tags, list) else [tags]
    })

    POSTS_JSON.write_text(json.dumps(posts, indent=4, ensure_ascii=False))
    print(f"Mis à jour: {POSTS_JSON}")

    print(f"\n✅ Article créé: /new-york/blog/{slug}/")
    print(f"📸 N'oubliez pas d'ajouter l'image: /new-york/blog/{slug}/featured.jpg")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_blog.py path/to/post.json")
        print("       python3 build_blog.py --from-n8n '{json}'")
        sys.exit(1)

    if sys.argv[1] == '--from-n8n':
        # Direct JSON input
        data = json.loads(sys.argv[2])
    else:
        # Read from file
        with open(sys.argv[1]) as f:
            data = json.load(f)

    build_post(data)


if __name__ == '__main__':
    main()
