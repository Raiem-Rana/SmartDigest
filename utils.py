"""
utils.py
--------
Small helper functions used across the app: text cleaning and
reading-time estimation.
"""

import re

AVERAGE_READING_SPEED_WPM = 200  # average adult reading speed


def clean_text(text: str) -> str:
    """Remove extra whitespace, weird characters, and repeated newlines."""
    text = re.sub(r"\s+", " ", text)          # collapse whitespace
    text = re.sub(r"\[\d+\]", "", text)         # remove citation markers like [1]
    text = text.strip()
    return text


def word_count(text: str) -> int:
    return len(text.split())


def estimate_reading_time(text: str, wpm: int = AVERAGE_READING_SPEED_WPM) -> float:
    """Return estimated reading time in minutes (rounded to 1 decimal)."""
    words = word_count(text)
    minutes = words / wpm
    return round(minutes, 1)


def reading_time_saved(original_text: str, summary_text: str) -> dict:
    """Compare reading time of original vs summary."""
    original_time = estimate_reading_time(original_text)
    summary_time = estimate_reading_time(summary_text)
    saved = max(original_time - summary_time, 0)
    percent_saved = round((saved / original_time) * 100, 1) if original_time > 0 else 0

    return {
        "original_minutes": original_time,
        "summary_minutes": summary_time,
        "minutes_saved": round(saved, 1),
        "percent_saved": percent_saved,
    }


def truncate_for_api(text: str, max_words: int = 1000) -> str:
    """
    Free summarization APIs often have input limits.
    Truncate long articles safely at a word boundary.
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])
