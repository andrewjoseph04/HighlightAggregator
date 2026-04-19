# Config

This folder now holds the shared path configuration for the project.

## Files

- `settings.py`: Centralized filesystem path settings used by the scripts

## Default Paths

`settings.py` defines these defaults relative to the repository root:

- `RAW_HIGHLIGHTS_CSV`: `data/raw/highlights.csv`
- `GROUPED_HIGHLIGHTS_OUTPUT`: `data/processed/grouped_highlights.md`
- `VAULT_BOOKS_DIR`: `Vault/Books`
- `KINDLE_CLIPPINGS_FILE`: `My Clippings.txt`

## Environment Variable Overrides

You can override any of those paths without editing code:

- `HIGHLIGHTS_RAW_CSV`
- `HIGHLIGHTS_GROUPED_OUTPUT`
- `HIGHLIGHTS_VAULT_DIR`
- `KINDLE_CLIPPINGS_FILE`

Example in PowerShell:

```powershell
$env:HIGHLIGHTS_VAULT_DIR = "R:\ObsidianVault\Books"
python Scripts\run_pipeline.py
```

## Why It Matters

Centralizing paths in one place makes the project easier to:

- Set up on a new machine
- Publish without exposing personal local paths
- Keep consistent across scripts
- Change without editing code in several places
