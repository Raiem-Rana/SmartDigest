"""
summarizer.py
-------------
Generates key-point summaries of article text.

Fully offline - uses sumy's LexRank algorithm.
No API key, no rate limits.
"""

import nltk

# Download required NLTK tokenizer data
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def summarize_to_points(text: str, sentence_count: int = 6) -> dict:
    """
    Returns a dict:
    {
        "points": [list of bullet-point strings],
        "method": "Offline extractive summarizer (sumy)",
        "raw_summary": full summary text
    }
    """

    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lex_rank import LexRankSummarizer

    # Create parser using English tokenizer
    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    # Create LexRank summarizer
    summarizer = LexRankSummarizer()

    # Generate summary
    summary_sentences = summarizer(
        parser.document,
        sentence_count
    )

    # Convert summary sentences to text
    summary_text = " ".join(
        str(sentence) for sentence in summary_sentences
    )

    # Convert summary into clean bullet points
    points = [
        s.strip()
        for s in summary_text.replace("\n", " ").split(". ")
        if s.strip()
    ]

    # Make sure every point ends with a period
    points = [
        p if p.endswith(".") else p + "."
        for p in points
    ]

    return {
        "points": points,
        "method": "Offline extractive summarizer (sumy - LexRank)",
        "raw_summary": summary_text,
    }
