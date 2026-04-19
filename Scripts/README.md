# Scripts

This folder contains the project's Python scripts. They fall into two groups:

- Kindle parsing scripts
- CSV / Google Sheet import scripts

## CSV / Google Sheet Flow

### `run_pipeline.py`

Fetches a published Google Sheet as CSV, groups highlights by book, formats them as Markdown, and appends them to book files in a vault directory.

Current behavior:

- Downloads CSV from a hardcoded Google Sheets export URL
- Reads rows with `csv.DictReader`
- Formats tags from the `Tags` and `Favorite Highlight` columns
- Skips duplicates by checking whether the quote already exists in the target file
- Writes to the configured vault directory from `Config/settings.py`

Run with:

```powershell
python Scripts/run_pipeline.py
```

### `google_sheet_reader.py`

Small helper script for testing that the Google Sheet is reachable and returns rows.

Run with:

```powershell
python Scripts/google_sheet_reader.py
```

### `google_form_parser.py`

Reads `data/raw/highlights.csv`, groups highlights by book, and writes a debug-friendly combined Markdown file to `data/processed/grouped_highlights.md`.

Useful when:

- You want to verify CSV parsing before writing to the vault
- You want a single grouped output file for inspection

Run with:

```powershell
python Scripts/google_form_parser.py
```

### `import_to_vault.py`

Reads `data/raw/highlights.csv` and appends grouped Markdown into per-book files.

Current output path:

- `VAULT_BOOKS_DIR` from `Config/settings.py`

Run with:

```powershell
python Scripts/import_to_vault.py
```

## Kindle Flow

### `kindleParser.py`

Parses `My Clippings.txt` and creates one Markdown file per book with simple bullet-style highlights.

Current output path:

- `VAULT_BOOKS_DIR` from `Config/settings.py`

Run with:

```powershell
python Scripts/kindleParser.py
```

### `markdownFormatter.py`

Similar to `kindleParser.py`, but writes more polished Markdown using blockquotes, previews, and collapsible `<details>` sections.

Current output path:

- `VAULT_BOOKS_DIR` from `Config/settings.py`

Run with:

```powershell
python Scripts/markdownFormatter.py
```

## Shared Assumptions

Path configuration is centralized in `Config/settings.py`.

Available environment variable overrides:

- `HIGHLIGHTS_RAW_CSV`
- `HIGHLIGHTS_GROUPED_OUTPUT`
- `HIGHLIGHTS_VAULT_DIR`
- `KINDLE_CLIPPINGS_FILE`

Most scripts assume the following CSV columns exist:

- `Book`
- `Quote`
- `Page number`
- `Tags`
- `Favorite Highlight`

Most scripts also assume:

- Input files already exist
- Output folders can be created if missing
- Duplicate detection can be done by searching for the full quote text in the target file

## Current Caveats

- Script names reflect the project's evolution and are a little overlapping.
- There is duplicated logic across multiple files for formatting tags, formatting Markdown, and duplicate checking.
- Error handling is minimal for malformed rows, missing files, and missing columns.
