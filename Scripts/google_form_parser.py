import csv
import sys
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Config.settings import GROUPED_HIGHLIGHTS_OUTPUT, RAW_HIGHLIGHTS_CSV


INPUT_FILE = RAW_HIGHLIGHTS_CSV
OUTPUT_FILE = GROUPED_HIGHLIGHTS_OUTPUT


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

            grouped_highlights[book].append(markdown)

    return grouped_highlights


def write_debug_output(grouped_data):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        for book, highlights in grouped_data.items():

            f.write(f"\n# {book}\n\n")

            for highlight in highlights:
                f.write(highlight)


def main():

    grouped_data = parse_csv()

    write_debug_output(grouped_data)

    print("Highlights grouped by book.\n")

    for book, highlights in grouped_data.items():
        print(f"{book}: {len(highlights)} highlights")

    print(f"\nDebug output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
