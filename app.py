"""
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
app.py
------
SmartDigest — Offline Article & News Key-Points Extractor
Streamlit front-end that ties together scraping, summarization,
sentiment analysis, and keyword extraction. Fully offline — no API keys needed.
"""

import streamlit as st

from src.scraper import scrape_article, ScraperError
from src.utils import clean_text, reading_time_saved, word_count
from src.summarizer import summarize_to_points
from src.sentiment import analyze_sentiment
from src.keywords import extract_keywords, generate_wordcloud_image, detect_category

# ---------------- Page config ----------------
st.set_page_config(
    page_title="SmartDigest",
    page_icon="📰",
    layout="wide",
)

st.title("📰 SmartDigest")
st.caption("Paste any article or blog link — get the key points, sentiment, and keywords in seconds. 100% offline, no API keys.")

# ---------------- Input ----------------
url = st.text_input("Article URL", placeholder="https://example.com/some-article")
analyze_clicked = st.button("🔍 Analyze", type="primary")

if analyze_clicked and url:
    with st.spinner("Scraping the page..."):
        try:
            result = scrape_article(url)
        except ScraperError as e:
            st.error(f"⚠️ {e}")
            st.stop()

    raw_text = clean_text(result["text"])
    title = result["title"]

    st.success(f"Scraped: **{title}**")

    with st.spinner("Summarizing key points..."):
        summary_result = summarize_to_points(raw_text)

    with st.spinner("Analyzing sentiment..."):
        sentiment_result = analyze_sentiment(raw_text)

    with st.spinner("Extracting keywords..."):
        top_keywords = extract_keywords(raw_text)
        category = detect_category(raw_text)

    stats = reading_time_saved(raw_text, summary_result["raw_summary"])

    # ---------------- Top stats row ----------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Category", category)
    col2.metric("Sentiment", f"{sentiment_result['emoji']} {sentiment_result['label']}")
    col3.metric("Original Read Time", f"{stats['original_minutes']} min")
    col4.metric("Time Saved", f"{stats['percent_saved']}%")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📌 Key Points", "☁️ Keywords", "📊 Details"])

    with tab1:
        st.subheader("Key Points")
        for point in summary_result["points"]:
            st.markdown(f"- {point}")
        st.caption(f"Summarized using: {summary_result['method']}")

    with tab2:
        st.subheader("Top Keywords")
        wc_image = generate_wordcloud_image(raw_text)
        st.image(wc_image.to_array(), use_container_width=True)

        st.write("**Most frequent terms:**")
        keyword_cols = st.columns(3)
        for i, (word, freq) in enumerate(top_keywords):
            keyword_cols[i % 3].write(f"`{word}` — {freq}x")

    with tab3:
        st.subheader("Full Stats")
        st.write(f"**Original word count:** {word_count(raw_text)}")
        st.write(f"**Summary word count:** {word_count(summary_result['raw_summary'])}")
        st.write(f"**Sentiment compound score:** {sentiment_result['compound_score']}")
        st.json(sentiment_result["scores"])

        with st.expander("View original scraped text"):
            st.write(raw_text)

elif analyze_clicked and not url:
    st.warning("Please paste a URL first.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("About SmartDigest")
    st.write(
        "SmartDigest scrapes any article and instantly gives you the key points, "
        "sentiment, and keywords — so you can decide if it's worth reading in full."
    )
    st.write("**Built with:** BeautifulSoup, sumy (LexRank), NLTK VADER, WordCloud, Streamlit")
    st.success("Runs 100% offline — no API keys, no rate limits, no internet dependency for analysis.")
