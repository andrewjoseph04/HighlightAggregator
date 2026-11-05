Highlight Aggregator

Highlight Aggregator is a small Python project that turns reading highlights into structured Markdown notes for an Obsidian-style knowledge vault.

The goal of the project is to build a personal knowledge ingestion pipeline that automatically captures, processes, and organizes insights from books.

The repository currently supports two workflows:

Kindle Workflow
Parse Kindle My Clippings.txt exports.
Convert highlights into Markdown notes grouped by book.
Physical Book Workflow
Capture highlights via a Google Form.
Store responses in a Google Sheet.
Use a Python pipeline to convert them into Markdown notes automatically.
Project Motivation

When reading books, many people highlight interesting passages but rarely revisit them later.

This project solves that problem by building a simple system that:

captures highlights quickly
stores them in a structured format
organizes them by book and structured tags
makes them searchable in a knowledge base

Instead of this typical workflow:

Read book → highlight quote → forget it later

The system enables:

Read book
↓
Capture highlight
↓
Automatically organize
↓
Store in knowledge vault
↓
Explore ideas later

This approach is inspired by personal knowledge management systems such as Second Brain and Zettelkasten.

System Architecture

Below is the complete architecture of the highlight ingestion pipeline.

                         ┌────────────────────────┐
                         │      Physical Book     │
                         │                        │
                         │  User reads & finds    │
                         │  interesting quote     │
                         └─────────────┬──────────┘
                                       │
                                       │ enters quote
                                       ▼
                         ┌────────────────────────┐
                         │      Google Form       │
                         │                        │
                         │  Capture highlight     │
                         │  Book / Quote / Topic  │
                         │ Context / Nature / Importance │
                         └─────────────┬──────────┘
                                       │
                                       │ automatic response storage
                                       ▼
                         ┌────────────────────────┐
                         │      Google Sheet      │
                         │                        │
                         │  Highlight database    │
                         │  (Form responses)      │
                         └─────────────┬──────────┘
                                       │
                                       │ CSV endpoint
                                       ▼
                     ┌──────────────────────────────────┐
                     │     Highlight Aggregator         │
                     │       Python Pipeline            │
                     │                                  │
                     │ 1. Fetch sheet data              │
                     │ 2. Parse highlights              │
                     │ 3. Format Markdown               │
                     │ 4. Group by book                 │
                     │ 5. Skip duplicates               │
                     └─────────────┬────────────────────┘
                                   │
                                   │ writes notes
                                   ▼
                         ┌────────────────────────┐
                         │     Obsidian Vault     │
                         │                        │
                         │  Books/                │
                         │   ├─ Shantaram.md      │
                         │   └─ OpenToWork.md     │
                         └─────────────┬──────────┘
                                       │
                                       │ Obsidian auto-refresh
                                       ▼
                         ┌────────────────────────┐
                         │        Obsidian        │
                         │                        │
                         │ Dashboards             │
                         │ Tag search             │
                         │ Quote of the day       │
                         └─────────────┬──────────┘
                                       │
                                       │ Syncthing
                                       ▼
                       ┌────────────────────────────────┐
                       │       Device Synchronization   │
                       │                                │
                       │  Laptop                        │
                       │  Phone                         │
                       │  Tablet                        │
                       └────────────────────────────────┘
Project Structure
highlight-aggregator
│
├── Scripts/
│   ├── run_pipeline.py
│   ├── import_to_vault.py
│   ├── google_form_parser.py
│   ├── google_sheet_reader.py
│   ├── kindleParser.py
│   └── markdownFormatter.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── Vault/
│   └── Books/
│
├── Config/
│
└── README.md
Key directories

Scripts/
Contains Python scripts responsible for parsing, formatting, and importing highlights.

data/
Contains raw and processed data used during development.

Vault/
Example generated Markdown notes grouped by book.

Config/
Contains shared settings such as centralized filesystem paths.

Highlight Format

Rows from the Google Sheet are converted into Markdown blocks like this:

> Highlight text

#topic #context #nature

<details>
<summary>Full Highlight</summary>

Highlight text

*p. 42*

</details>

---

Tags always follow the Obsidian master-tag order:

- Topic
- Context
- Nature

Only the approved tags from the Obsidian master tag system are written. The
legacy `Importance` field is ignored; it is not part of the master taxonomy.
Common form spelling/spacing variants such as `self improvement` and `self
improvment` are normalised to `#selfimprovement`.

Each book is written to its own Markdown file.

Example:

Books/
   Open to Work - Ryan Roslansky.md
   Shantaram - Gregory David Roberts.md

Duplicate highlights are automatically skipped if they already exist.

Example Usage
Step 1 — Capture highlight

While reading a physical book, open the highlight capture form on your phone and enter:

Book name
Quote
Page number
Topic
Context
Nature
`Importance` is a legacy form field and is ignored.
Step 2 — Run the pipeline
python Scripts/run_pipeline.py
Step 3 — Notes automatically appear in Obsidian

The script writes Markdown notes to the vault.

Example output:

> Failure is not an option

#career #work #motivation

<details>
<summary>Full Highlight</summary>

Failure is not an option

*p. 4*

</details>

---

Obsidian automatically refreshes and the highlight becomes searchable.

Setup
Install Python

Python 3.10+ is recommended.

Install dependencies

Currently the project uses only one external dependency:

pip install requests
Running the Project
Run the Google Sheet pipeline
python Scripts/run_pipeline.py
Import highlights from a local CSV
python Scripts/import_to_vault.py
Generate grouped debug output
python Scripts/google_form_parser.py
Test Google Sheet connectivity
python Scripts/google_sheet_reader.py
Convert Kindle highlights
python Scripts/kindleParser.py
python Scripts/markdownFormatter.py
Current Limitations
Filesystem paths are centralized in Config/settings.py and can be overridden locally with environment variables.
The Google Sheet ID is still hardcoded in some scripts.
No pinned requirements.txt yet.
TODOs
Keep the Google Sheet private and stop committing the sheet ID in source control. Use environment variables or local secret storage for the sheet ID and any future Google credentials.
Do not commit service-account JSON files or other secrets. The repo already ignores Config/*.env and Config/*.json, which should be retained.
Add a GitHub Actions workflow later to automate the full end-to-end flow from Google Form submissions to the vault update pipeline, using GitHub Secrets for any required credentials.
Future Roadmap

Planned improvements include:

Architecture Improvements
Standardize vault output paths
Add requirements.txt
Pipeline Improvements
Process only new highlights instead of the full sheet
Add validation for malformed rows
Improve error handling
Knowledge Features
Build Obsidian dashboards
Add Quote of the Day
Create topic-based highlight views
Additional Sources

Future ingestion sources may include:

Apple Books highlights
Web article highlights
Podcast quotes
Music lyrics
License

This project is intended as a personal knowledge management tool and is shared for educational purposes.
