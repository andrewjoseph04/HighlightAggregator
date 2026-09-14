import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _path_setting(env_name, default_path):
    value = os.getenv(env_name)
    if value:
        return Path(value).expanduser()
    return default_path


RAW_HIGHLIGHTS_CSV = _path_setting(
    "HIGHLIGHTS_RAW_CSV",
    REPO_ROOT / "data" / "raw" / "highlights.csv",
)

GROUPED_HIGHLIGHTS_OUTPUT = _path_setting(
    "HIGHLIGHTS_GROUPED_OUTPUT",
    REPO_ROOT / "data" / "processed" / "grouped_highlights.md",
)

PIPELINE_RUN_LOG = _path_setting(
    "HIGHLIGHTS_RUN_LOG",
    Path(r"R:\ObsidianVault\Metadata\HighlightAgregatorRunlog.md"),
)

PIPELINE_RUN_LOG_TAG = os.getenv(
    "HIGHLIGHTS_RUN_LOG_TAG",
    "#highlightaggregator",
)

GOOGLE_SHEET_ID = os.getenv(
    "HIGHLIGHTS_GOOGLE_SHEET_ID",
    "1-i_8iqsEayj8A0hN_eQZ8v0WyjAUcE6LrEMWPgHpERU",
)

def get_google_sheet_csv_url():
    sheet_id = GOOGLE_SHEET_ID.strip()
    if not sheet_id or sheet_id == "YOUR_SHEET_ID":
        raise ValueError(
            "Google Sheet ID is not configured. Set HIGHLIGHTS_GOOGLE_SHEET_ID "
            "to your published Google Sheet ID."
        )
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"


GOOGLE_SHEET_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
)

VAULT_BOOKS_DIR = _path_setting(
    "HIGHLIGHTS_VAULT_DIR",
    Path(r"R:\ObsidianVault\Books"),
)

KINDLE_CLIPPINGS_FILE = _path_setting(
    "KINDLE_CLIPPINGS_FILE",
    REPO_ROOT / "My Clippings.txt",
)
