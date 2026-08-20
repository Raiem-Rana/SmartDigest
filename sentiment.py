"""
sentiment.py
------------
Analyzes the overall sentiment/tone of the article text using
NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner).
Fully offline, no API key needed.
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def _ensure_vader_lexicon():
    """Download the VADER lexicon on first run if it's not already present."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


def analyze_sentiment(text: str) -> dict:
    """
    Returns a dict:
    {
        "label": "Positive" | "Neutral" | "Negative",
        "emoji": "😊" | "😐" | "☹️",
        "compound_score": float (-1 to 1),
        "scores": {neg, neu, pos, compound}
    }
    """
    _ensure_vader_lexicon()
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label, emoji = "Positive", "😊"
    elif compound <= -0.05:
        label, emoji = "Negative", "☹️"
    else:
        label, emoji = "Neutral", "😐"

    return {
        "label": label,
        "emoji": emoji,
        "compound_score": round(compound, 3),
        "scores": scores,
    }
