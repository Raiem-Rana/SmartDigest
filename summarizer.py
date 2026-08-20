"""
summarizer.py
-------------
Generates key-point summaries of article text.

Fully offline.
No API key.
No NLTK.
No sumy.
No internet required.
"""

import re
from collections import Counter


def split_sentences(text: str) -> list:
    """Split text into clean sentences."""

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def summarize_to_points(
    text: str,
    sentence_count: int = 6
) -> dict:
    """
    Generate an offline extractive summary.

    Returns:
    {
        "points": [...],
        "method": "...",
        "raw_summary": "..."
    }
    """

    if not text or not text.strip():
        return {
            "points": [],
            "method": "Offline extractive summarizer",
            "raw_summary": "",
        }

    sentences = split_sentences(text)

    # If article is already short, return all sentences
    if len(sentences) <= sentence_count:
        points = [
            sentence if sentence.endswith((".", "!", "?"))
            else sentence + "."
            for sentence in sentences
        ]

        return {
            "points": points,
            "method": "Offline extractive summarizer",
            "raw_summary": " ".join(points),
        }

    # Common words that should not influence sentence importance
    stop_words = {
        "the", "a", "an", "and", "or", "but", "if", "then",
        "this", "that", "these", "those", "is", "are", "was",
        "were", "be", "been", "to", "of", "in", "on", "for",
        "with", "as", "by", "at", "from", "it", "its", "they",
        "their", "them", "he", "she", "his", "her", "we", "our",
        "you", "your", "i", "me", "my", "has", "have", "had",
        "will", "would", "can", "could", "should", "may", "might"
    }

    # Count important words
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    word_frequency = Counter(
        word for word in words
        if word not in stop_words
    )

    # Score each sentence
    scored_sentences = []

    for index, sentence in enumerate(sentences):

        sentence_words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            sentence.lower()
        )

        if not sentence_words:
            continue

        score = sum(
            word_frequency.get(word, 0)
            for word in sentence_words
            if word not in stop_words
        )

        # Slightly reward sentences near the beginning
        if index < 2:
            score *= 1.15

        scored_sentences.append(
            (score, index, sentence)
        )

    # Select the highest-scoring sentences
    top_sentences = sorted(
        scored_sentences,
        key=lambda x: x[0],
        reverse=True
    )[:sentence_count]

    # Restore original article order
    top_sentences.sort(key=lambda x: x[1])

    points = [
        sentence if sentence.endswith((".", "!", "?"))
        else sentence + "."
        for _, _, sentence in top_sentences
    ]

    summary_text = " ".join(points)

    return {
        "points": points,
        "method": "Offline extractive summarizer",
        "raw_summary": summary_text,
    }
