"""Normalise form responses to the Obsidian master tag system."""

# A highlight deliberately uses only these three dimensions.  Importance is a
# legacy form field and is not part of the master tag taxonomy.
TAG_FIELD_ORDER = ("Topic", "Context", "Nature")

MASTER_TAGS = {
    "life", "philosophy", "psychology", "society", "culture",
    "career", "finance", "economics",
    "technology", "ai", "software", "engineering", "dataengineering",
    "creativity", "art", "music", "mentalmodels",
    "work", "leadership", "management", "productivity",
    "relationships", "friendship", "love",
    "learning", "growth", "selfimprovement", "decisionmaking", "strategy",
    "human-nature", "investing", "wealth",
    "wisdom", "principle", "lesson", "observation", "truth", "motivation",
    "warning", "bias", "story", "quote",
}

FIELD_ALIASES = {
    "Topic": (
        "Topic",
        "Topic tag",
        "Topic Tag - What is idea about",
    ),
    "Context": (
        "Context",
        "Context tag",
        "Context Tag - Where idea Applies",
    ),
    "Nature": (
        "Nature",
        "Nature tag",
        "Nature Tag - Type of Insight",
    ),
}

TAG_ALIASES = {
    "self improvement": "selfimprovement",
    "self improvment": "selfimprovement",
    "data engineering": "dataengineering",
    "human nature": "human-nature",
    "mental models": "mentalmodels",
    "decision making": "decisionmaking",
}


def _clean_tag_value(value):
    if value is None:
        return ""
    value = str(value).strip().lower().lstrip("#")
    return TAG_ALIASES.get(value, value)


def _get_field_value(row, field):
    """Support both the original and Microsoft Form question headings."""
    normalised_row = {
        " ".join(str(header).casefold().split()): value
        for header, value in row.items()
    }
    for header in FIELD_ALIASES[field]:
        value = normalised_row.get(" ".join(header.casefold().split()), "")
        if str(value).strip():
            return value
    return ""


def build_tag_list(row):
    """Return approved Topic -> Context -> Nature tags, omitting invalid input."""
    tags = []
    for field in TAG_FIELD_ORDER:
        value = _clean_tag_value(_get_field_value(row, field))
        if value in MASTER_TAGS:
            tags.append(f"#{value}")
    return tags


def format_tags(row):
    return " ".join(build_tag_list(row))
