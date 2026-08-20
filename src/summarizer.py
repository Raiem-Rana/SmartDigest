"""
summarizer.py
-------------
Generates key-point summaries of article text.

Fully offline - uses sumy's LexRank algorithm. No API key,
no internet call, no rate limits. Works anywhere, anytime.
"""


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

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)

    summary_text = " ".join(str(sentence) for sentence in summary_sentences)

    # Split into clean bullet points by sentence
    points = [s.strip() for s in summary_text.replace("\n", " ").split(". ") if s.strip()]
    points = [p if p.endswith(".") else p + "." for p in points]

    return {
        "points": points,
        "method": "Offline extractive summarizer (sumy - LexRank)",
        "raw_summary": summary_text,
    }
