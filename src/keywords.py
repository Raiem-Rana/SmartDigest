"""
keywords.py
-----------
Extracts the most important/frequent keywords from article text
and generates a word cloud image for visualization.
"""

import re
from collections import Counter

import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud


def _ensure_stopwords():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)


def extract_keywords(text: str, top_n: int = 12) -> list:
    """Returns a list of (word, frequency) tuples for the top N keywords."""
    _ensure_stopwords()
    stop_words = set(stopwords.words("english"))

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    filtered = [w for w in words if w not in stop_words]

    counts = Counter(filtered)
    return counts.most_common(top_n)


def generate_wordcloud_image(text: str, width: int = 800, height: int = 400):
    """
    Returns a matplotlib-compatible WordCloud object.
    Streamlit can render this directly with st.image(wc.to_array()).
    """
    _ensure_stopwords()
    stop_words = set(stopwords.words("english"))

    wc = WordCloud(
        width=width,
        height=height,
        background_color="white",
        stopwords=stop_words,
        colormap="viridis",
        max_words=60,
    ).generate(text)

    return wc


def detect_category(text: str) -> str:
    """
    Very lightweight keyword-based category guesser.
    Not ML-based — just a fun, fast heuristic layer.
    Could be swapped for a zero-shot HF classification model later.
    """
    categories = {
        "Technology": ["software", "app", "ai", "tech", "computer", "data", "startup", "internet", "device"],
        "Sports": ["match", "team", "player", "game", "season", "coach", "league", "tournament", "score"],
        "Politics": ["government", "election", "president", "policy", "senate", "minister", "vote", "law"],
        "Business/Finance": ["market", "stock", "economy", "company", "revenue", "investment", "trade", "bank"],
        "Health": ["health", "disease", "doctor", "medical", "hospital", "virus", "treatment", "patient"],
        "Entertainment": ["movie", "film", "music", "celebrity", "show", "actor", "album", "concert"],
        "Science": ["research", "study", "scientist", "space", "climate", "discovery", "experiment"],
    }

    text_lower = text.lower()
    scores = {cat: sum(text_lower.count(kw) for kw in kws) for cat, kws in categories.items()}
    best_category = max(scores, key=scores.get)

    return best_category if scores[best_category] > 0 else "General"
