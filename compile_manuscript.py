#!/usr/bin/env python3
"""
Compile all chapter drafts into a single manuscript document for review.
"""

from pathlib import Path
from datetime import datetime

# Base path for chapters
BASE_PATH = Path(__file__).parent / "_private" / "manuscript" / "chapters"

# Chapter order and folder names
CHAPTERS = [
    ("00_prologue", "Prologue"),
    ("01_arrivee", "Chapitre 1"),
    ("02_premiers_pas", "Chapitre 2"),
    ("03_sens", "Chapitre 3"),
    ("04_faim", "Chapitre 4"),
    ("05_quartiers", "Chapitre 5"),
    ("06_monuments", "Chapitre 6"),
    ("07_se_perdre", "Chapitre 7"),
    ("08_nuit", "Chapitre 8"),
    ("09_rencontres", "Chapitre 9"),
    ("10_devenir", "Chapitre 10"),
    ("11_secrets", "Chapitre 11"),
    ("12_apres", "Chapitre 12"),
]

def compile_manuscript():
    """Compile all chapters into a single markdown document."""

    output_lines = []

    # Title page
    output_lines.append("# Après New York")
    output_lines.append("")
    output_lines.append("**F.B. Emerson**")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append(f"*First Draft - Compiled {datetime.now().strftime('%B %d, %Y')}*")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("")

    total_words = 0
    chapters_found = 0

    for folder_name, chapter_label in CHAPTERS:
        chapter_path = BASE_PATH / folder_name / "CHAPTER_DRAFT.md"

        if chapter_path.exists():
            content = chapter_path.read_text(encoding="utf-8")

            # Count words (rough estimate)
            word_count = len(content.split())
            total_words += word_count
            chapters_found += 1

            # Add chapter content
            output_lines.append(content)
            output_lines.append("")
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
            output_lines.append("")

            print(f"Added {chapter_label}: {word_count:,} words")
        else:
            print(f"WARNING: {chapter_label} not found at {chapter_path}")

    # Add footer
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("## Manuscript Statistics")
    output_lines.append("")
    output_lines.append(f"- **Total Chapters:** {chapters_found}")
    output_lines.append(f"- **Total Words:** ~{total_words:,}")
    output_lines.append(f"- **Estimated Pages:** ~{total_words // 250}")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("*Fin*")

    # Write output
    output_path = Path(__file__).parent / "_private" / "COMPLETE_MANUSCRIPT_DRAFT.md"
    output_path.write_text("\n".join(output_lines), encoding="utf-8")

    print("")
    print("=" * 50)
    print(f"Manuscript compiled successfully!")
    print(f"Output: {output_path}")
    print(f"Total: {chapters_found} chapters, ~{total_words:,} words")
    print("=" * 50)

    return output_path

if __name__ == "__main__":
    compile_manuscript()
