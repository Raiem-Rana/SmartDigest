"""
summarizer.py
-------------
Generates key-point summaries of article text.

Uses sumy's LexRank algorithm with a simple custom
sentence tokenizer, so it does not depend on NLTK.
"""

import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer


class SimpleSentenceTokenizer:
    """
    Simple sentence tokenizer compatible with sumy.
    Avoids NLTK dependency.
    """

    def to_sentences(self, text):
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [sentence.strip() for sentence in sentences if sentence.strip()]


class SimpleLanguage:
    """
    Minimal language wrapper required by sumy.
    """

    @property
    def sentence_tokenizer(self):
        return SimpleSentenceTokenizer()


def summarize_to_points(text: str, sentence_count: int = 6) -> dict:
    """
    Returns a dictionary containing key-point summaries.
    """

    if not text or not text.strip():
        return {
            "points": [],
            "method": "Offline extractive summarizer (sumy - LexRank)",
            "raw_summary": "",
        }

    # Split text into sentences ourselves
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    # If there are very few sentences, return them directly
    if len(sentences) <= sentence_count:
        points = [
            sentence if sentence.endswith((".", "!", "?"))
            else sentence + "."
            for sentence in sentences
        ]

        summary_text = " ".join(points)

        return {
            "points": points,
            "method": "Offline extractive summarizer",
            "raw_summary": summary_text,
        }

    # Create a simple document for sumy
    parser = PlaintextParser.from_string(
        text,
        SimpleSentenceTokenizer()
    )

    # LexRank summarizer
    summarizer = LexRankSummarizer()

    summary_sentences = summarizer(
        parser.document,
        sentence_count
    )

    summary_text = " ".join(
        str(sentence)
        for sentence in summary_sentences
    )

    # Convert summary into bullet points
    points = re.split(
        r"(?<=[.!?])\s+",
        summary_text.strip()
    )

    points = [
        point.strip()
        for point in points
        if point.strip()
    ]

    return {
        "points": points,
        "method": "Offline extractive summarizer (sumy - LexRank)",
        "raw_summary": summary_text,
    }
