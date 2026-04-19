import re
import sys
from pathlib import Path
from collections import defaultdict
import textwrap

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Config.settings import KINDLE_CLIPPINGS_FILE, VAULT_BOOKS_DIR


INPUT_FILE = KINDLE_CLIPPINGS_FILE
OUTPUT_FOLDER = VAULT_BOOKS_DIR

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
    content = f.read()

entries = content.split("==========")
books = defaultdict(list)


for entry in entries:
    lines = [l.strip() for l in entry.strip().split("\n") if l.strip()]

    if len(lines) < 3:
        continue

    book = lines[0]
    meta = lines[1]
    highlight = lines[2]

    books[book].append((meta, highlight))


def create_preview(text):
    wrapped = textwrap.wrap(text, width=80)
    preview_lines = wrapped[:3]
    return "\n".join(preview_lines) + "..."


for book, highlights in books.items():
    safe_name = re.sub(r'[\\/*?:"<>|]', "", book)
    file_path = OUTPUT_FOLDER / f"{safe_name}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {book}\n\n")
        f.write("## Kindle Highlights\n\n")

        for meta, highlight in highlights:

            preview = create_preview(highlight)

            f.write("> " + preview.replace("\n", "\n> ") + "\n\n")

            f.write("<details>\n")
            f.write("<summary>Full Highlight</summary>\n\n")
            f.write(highlight + "\n\n")
            f.write(f"*{meta}*\n\n")
            f.write("</details>\n\n")

print("Highlights exported successfully!")
