# Vault

This folder holds example generated Markdown notes for books.

## Structure

- `Books/`: One Markdown file per book

Example:

- `Books/Open to Work - Ryan Roslansky.md`

## Purpose

The repository uses this folder as the default local vault output.

Current behavior:

- All scripts now use `VAULT_BOOKS_DIR` from `Config/settings.py`.
- By default, `VAULT_BOOKS_DIR` points to `Vault/Books` inside this repository.
- You can override it with the `HIGHLIGHTS_VAULT_DIR` environment variable.

## File Format

Book files contain repeated highlight blocks with:

- A blockquoted preview or full quote
- Approved master tags in `Topic -> Context -> Nature` order
- A collapsible `<details>` section
- A page reference when available

## Notes

- This folder is useful for checking formatting without needing a separate external Obsidian vault.
- If you want to target an external vault, set `HIGHLIGHTS_VAULT_DIR` before running the scripts.
