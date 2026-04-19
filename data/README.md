# Data

This folder contains sample input and intermediate output for the CSV-based highlight pipeline.

## Structure

- `raw/highlights.csv`: Source highlight export used by the CSV import scripts.
- `processed/grouped_highlights.md`: Debug output grouped by book.
- `processed/formatted_highlights.md`: Example formatted highlight output.

## Raw Data Format

The checked-in sample CSV uses these headers:

```text
Timestamp,Book,Quote,Page number,Tags,Favorite Highlight
```

Example row shape:

```text
19/04/2026 16:05:43,Open to Work - Ryan Roslansky,Test,2,life,
```

## How This Folder Is Used

- `Scripts/google_form_parser.py` reads `raw/highlights.csv` and writes `processed/grouped_highlights.md`.
- `Scripts/import_to_vault.py` reads `raw/highlights.csv` and writes book notes into a vault folder.

## Notes

- `processed` files are useful as inspection artifacts during development.
- The sample data currently represents book highlights for `Open to Work - Ryan Roslansky`.
- If you change the CSV schema, the parsing scripts will also need updates.
