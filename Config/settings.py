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
    "YOUR_SHEET_ID",
)

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
