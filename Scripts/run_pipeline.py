import requests
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')
from io import StringIO
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from time import perf_counter

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Config.settings import (
    PIPELINE_RUN_LOG,
    PIPELINE_RUN_LOG_TAG,
    VAULT_BOOKS_DIR,
    get_google_sheet_csv_url,
)
from Scripts.tagging import format_tags

VAULT_PATH = VAULT_BOOKS_DIR
RUN_LOG_PATH = PIPELINE_RUN_LOG
RUN_LOG_TAG = PIPELINE_RUN_LOG_TAG
RUN_SOURCE = "google_sheet"
RUN_LOG_OWNER = "highlight-pipeline"
RUN_LOG_HEADER = (
    "| Run Time | Source | Book Title | Books Updated | New Files | Rows Fetched | "
    "Rows Processed | Highlights Added | Duplicates Skipped | Duplicate Rate | Tags | "
    "Duration | Status | Vault Path | Notes |\n"
)
RUN_LOG_DIVIDER = (
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
)


def sanitize_table_cell(value):

    text = str(value).replace("\n", " ").strip()
    return text.replace("|", "/") if text else "-"

def fetch_sheet():
    csv_url = get_google_sheet_csv_url()

    # response = requests.get(csv_url)
    # response.raise_for_status()

    # csv_data = StringIO(response.text)

    response = requests.get(csv_url)

    response.raise_for_status()

    # Force correct UTF-8 decoding
    csv_data = StringIO(response.content.decode("utf-8"))

    reader = csv.DictReader(csv_data)

    rows = list(reader)

    return rows


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


def group_highlights(rows):

    grouped = defaultdict(list)
    processed_rows = 0
    invalid_rows = 0
    notes = []

    for row in rows:

        book = row.get("Book", "").strip()
        quote = row.get("Quote", "").strip()
        page = row.get("Page number", "").strip()

        if not book or not quote:
            invalid_rows += 1
            notes.append("Skipped rows missing Book or Quote")
            continue

        tags = format_tags(row)

        markdown = format_markdown(quote, page, tags)

        grouped[book].append((quote, markdown, tags))
        processed_rows += 1

    return grouped, {
        "rows_processed": processed_rows,
        "invalid_rows": invalid_rows,
        "notes": sorted(set(notes)),
    }


def highlight_exists(file_path, quote):

    if not file_path.exists():
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return quote in content


def write_to_vault(grouped_data):

    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    books_updated = set()
    titles_updated = set()
    new_files_created = 0
    highlights_added = 0
    duplicates_skipped = 0
    tags_added = set()

    for book, highlights in grouped_data.items():

        file_path = VAULT_PATH / f"{book}.md"
        file_previously_existed = file_path.exists()
        book_received_new_highlight = False

        for quote, markdown, tags in highlights:

            if highlight_exists(file_path, quote):
                print(f"Skipping duplicate: {quote[:40]}...")
                duplicates_skipped += 1
                continue

            with open(file_path, "a", encoding="utf-8") as f:
                f.write(markdown)

            print(f"Added highlight to {book}")
            books_updated.add(book)
            titles_updated.add(book)
            highlights_added += 1
            book_received_new_highlight = True
            if tags:
                tags_added.update(tags.split())

        if book_received_new_highlight and not file_previously_existed:
            new_files_created += 1

    return {
        "books_updated": len(books_updated),
        "titles_updated": " | ".join(sorted(titles_updated)) if titles_updated else "-",
        "new_files_created": new_files_created,
        "highlights_added": highlights_added,
        "duplicates_skipped": duplicates_skipped,
        "tags_added": " ".join(sorted(tags_added)) if tags_added else "-",
    }


def ensure_run_log_file():

    RUN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if RUN_LOG_PATH.exists():
        with open(RUN_LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        if RUN_LOG_HEADER in content:
            return
        content = upgrade_run_log_content(content)
    else:
        content = build_run_log_preamble()

    with open(RUN_LOG_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def build_run_log_preamble():

    return (
        f"{RUN_LOG_TAG}\n"
        f"source:: {RUN_SOURCE}\n"
        f"owner:: {RUN_LOG_OWNER}\n\n"
        f"{RUN_LOG_HEADER}"
        f"{RUN_LOG_DIVIDER}"
    )


def upgrade_run_log_content(content):

    lines = content.splitlines()
    rows = []

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "Run Time" in stripped or stripped.startswith("| ---"):
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) == 7:
            run_time, book_title, books_updated, rows_fetched, highlights_added, duplicates_skipped, tags = cells
            try:
                duplicate_rate = f"{(int(duplicates_skipped) / max(int(rows_fetched), 1)) * 100:.0f}%"
            except ValueError:
                duplicate_rate = "-"
            rows.append(
                {
                    "run_time": run_time,
                    "source": RUN_SOURCE,
                    "book_title": book_title,
                    "books_updated": books_updated,
                    "new_files": "-",
                    "rows_fetched": rows_fetched,
                    "rows_processed": rows_fetched,
                    "highlights_added": highlights_added,
                    "duplicates_skipped": duplicates_skipped,
                    "duplicate_rate": duplicate_rate,
                    "tags": tags,
                    "duration": "-",
                    "status": "success",
                    "vault_path": str(VAULT_PATH),
                    "notes": "-",
                }
            )

    upgraded = build_run_log_preamble()
    for row in sorted(rows, key=lambda row: row["run_time"], reverse=True):
        upgraded += format_run_log_row(**row)
    return upgraded


def prepend_run_log_row(row):

    ensure_run_log_file()
    with open(RUN_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    row_lines = [line for line in lines if line.lstrip().startswith("|") and "Run Time" not in line and not line.lstrip().startswith("| ---")]
    other_lines = [line for line in lines if not (line.lstrip().startswith("|") and "Run Time" not in line and not line.lstrip().startswith("| ---"))]
    new_row = format_run_log_row(**row)
    all_rows = row_lines + [new_row]

    def run_time(line):
        try:
            return datetime.fromisoformat(line.strip().strip("|").split("|")[0].strip())
        except ValueError:
            return datetime.min

    all_rows.sort(key=run_time, reverse=True)
    divider_index = next((i for i, line in enumerate(other_lines) if line.lstrip().startswith("| ---")), None)
    if divider_index is None:
        with open(RUN_LOG_PATH, "w", encoding="utf-8") as f:
            f.write(content)
            f.write(new_row)
        return

    updated = other_lines[:divider_index + 1] + all_rows + other_lines[divider_index + 1:]
    with open(RUN_LOG_PATH, "w", encoding="utf-8") as f:
        f.writelines(updated)


def format_run_log_row(
    run_time,
    source,
    book_title,
    books_updated,
    new_files,
    rows_fetched,
    rows_processed,
    highlights_added,
    duplicates_skipped,
    duplicate_rate,
    tags,
    duration,
    status,
    vault_path,
    notes,
):

    values = [
        run_time,
        source,
        book_title,
        books_updated,
        new_files,
        rows_fetched,
        rows_processed,
        highlights_added,
        duplicates_skipped,
        duplicate_rate,
        tags,
        duration,
        status,
        vault_path,
        notes,
    ]
    return f"| {' | '.join(sanitize_table_cell(value) for value in values)} |\n"


def append_run_log(
    run_time,
    source,
    book_title,
    books_updated,
    new_files,
    rows_fetched,
    rows_processed,
    highlights_added,
    duplicates_skipped,
    duplicate_rate,
    tags,
    duration,
    status,
    vault_path,
    notes,
):

    prepend_run_log_row(
        dict(
            run_time=run_time,
            source=source,
            book_title=book_title,
            books_updated=books_updated,
            new_files=new_files,
            rows_fetched=rows_fetched,
            rows_processed=rows_processed,
            highlights_added=highlights_added,
            duplicates_skipped=duplicates_skipped,
            duplicate_rate=duplicate_rate,
            tags=tags,
            duration=duration,
            status=status,
            vault_path=vault_path,
            notes=notes,
        )
    )


def main():

    start_time = perf_counter()
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "success"
    notes = []

    print("Fetching highlights from Google Sheet...")

    rows_fetched = 0
    rows_processed = 0
    stats = {
        "books_updated": 0,
        "titles_updated": "-",
        "new_files_created": 0,
        "highlights_added": 0,
        "duplicates_skipped": 0,
        "tags_added": "-",
    }

    try:
        rows = fetch_sheet()
        rows_fetched = len(rows)

        print(f"{rows_fetched} rows fetched")

        grouped, grouping_stats = group_highlights(rows)
        rows_processed = grouping_stats["rows_processed"]
        notes.extend(grouping_stats["notes"])
        if grouping_stats["invalid_rows"]:
            notes.append(f"Invalid rows skipped: {grouping_stats['invalid_rows']}")

        stats = write_to_vault(grouped)
        if rows_processed == 0 and rows_fetched > 0:
            notes.append("No valid rows were processed")
    except Exception as exc:
        status = "failed"
        notes.append(f"Error: {exc}")
        raise
    finally:
        duration = f"{perf_counter() - start_time:.2f}s"
        duplicate_rate = (
            f"{(stats['duplicates_skipped'] / rows_processed) * 100:.0f}%"
            if rows_processed
            else "-"
        )
        note_text = " ; ".join(dict.fromkeys(notes)) if notes else "-"
        append_run_log(
            run_time=run_time,
            source=RUN_SOURCE,
            book_title=stats["titles_updated"],
            books_updated=stats["books_updated"],
            new_files=stats["new_files_created"],
            rows_fetched=rows_fetched,
            rows_processed=rows_processed,
            highlights_added=stats["highlights_added"],
            duplicates_skipped=stats["duplicates_skipped"],
            duplicate_rate=duplicate_rate,
            tags=stats["tags_added"],
            duration=duration,
            status=status,
            vault_path=VAULT_PATH,
            notes=note_text,
        )

    print(f"Books updated: {stats['books_updated']}")
    print(f"New files created: {stats['new_files_created']}")
    print(f"Rows processed: {rows_processed}")
    print(f"Highlights added: {stats['highlights_added']}")
    print(f"Duplicates skipped: {stats['duplicates_skipped']}")
    print(f"Duplicate rate: {duplicate_rate}")
    print(f"Tags added: {stats['tags_added']}")
    print(f"Duration: {duration}")
    print(f"Status: {status}")
    print(f"Notes: {note_text}")
    print(f"Run log updated: {RUN_LOG_PATH}")

    print("\nPipeline completed.")


if __name__ == "__main__":
    main()
