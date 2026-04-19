import csv
import sys
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Config.settings import RAW_HIGHLIGHTS_CSV, VAULT_BOOKS_DIR


INPUT_FILE = RAW_HIGHLIGHTS_CSV
VAULT_PATH = VAULT_BOOKS_DIR


def format_tags(tag_string, favorite):
    tags = []

    if tag_string:
        for tag in tag_string.split(","):
            tag = tag.strip()
            if tag:
                tags.append(f"#{tag}")

    if favorite.strip().lower() == "yes":
        tags.append("#favorite")

    return " ".join(tags)


def format_markdown(quote, page, tags):

    markdown = f"""
> {quote}

{tags}

<details>
<summary>Full Highlight</summary>

{quote}

*p. {page}*

</details>

---

"""

    return markdown


def parse_csv():

    grouped_highlights = defaultdict(list)

    with open(INPUT_FILE, newline="", encoding="utf-8") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            book = row["Book"].strip()
            quote = row["Quote"].strip()
            page = row["Page number"].strip()
            tags = format_tags(row["Tags"], row["Favorite Highlight"])

            markdown = format_markdown(quote, page, tags)

            grouped_highlights[book].append((quote, markdown))

    return grouped_highlights


def highlight_exists(file_path, quote):

    if not file_path.exists():
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return quote in content


def write_to_vault(grouped_data):

    VAULT_PATH.mkdir(parents=True, exist_ok=True)

    for book, highlights in grouped_data.items():

        file_path = VAULT_PATH / f"{book}.md"

        for quote, markdown in highlights:

            if highlight_exists(file_path, quote):
                print(f"Skipping duplicate in {book}: {quote[:40]}...")
                continue

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(markdown)

            print(f"Added highlight to {book}")


def main():

    grouped_data = parse_csv()

    write_to_vault(grouped_data)

    print("\nImport complete.")


if __name__ == "__main__":
    main()
