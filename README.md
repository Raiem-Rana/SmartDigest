# 📰 SmartDigest — Offline Article & News Key-Points Extractor

**SmartDigest** scrapes any article, blog post, or news URL and instantly extracts the key points, sentiment, keywords, and estimated time saved — so readers can decide if it's worth reading in full before committing their time.

**100% offline analysis — no API keys, no rate limits, no external AI service required.**

🔗 **Live demo:** _[add your Streamlit Cloud link here after deploying]_

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🔗 **Scrapes any article URL** — cleans out nav bars, ads, scripts, and footers automatically
- 📌 **Key-point extraction** — offline extractive summarization using the LexRank algorithm (`sumy`)
- 😊 **Sentiment analysis** — detects overall tone (Positive / Neutral / Negative) using NLTK's VADER
- ☁️ **Keyword extraction + word cloud** — visualizes the most important terms in the article
- 🏷️ **Auto-category detection** — tags the article as Tech, Sports, Politics, Business, Health, Entertainment, or Science
- ⏱️ **Reading time saved** — compares original article length vs. summary to show time saved

## 🎯 Why I built this

Information overload is real — most people skim headlines and never read the full article, or waste time on articles that turn out to be irrelevant. SmartDigest bridges that gap by giving readers an honest, fast preview of what an article actually says before they invest their time in it — without depending on any paid or rate-limited external AI service.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Scraping | `requests`, `BeautifulSoup4` |
| Summarization | `sumy` (LexRank algorithm — fully offline) |
| Sentiment Analysis | NLTK `VADER` |
| Keyword Extraction / Visualization | `nltk`, `wordcloud`, `matplotlib` |
| Frontend & Deployment | `Streamlit` |

---

## 📁 Project Structure

```
smartdigest/
├── app.py                     # Streamlit UI — main entry point
├── src/
│   ├── scraper.py              # Fetches & cleans article text from a URL
│   ├── summarizer.py           # Offline LexRank summarization
│   ├── sentiment.py            # VADER sentiment analysis
│   ├── keywords.py             # Keyword extraction + word cloud + category detection
│   └── utils.py                 # Text cleaning, reading time calculations
├── tests/
│   └── test_scraper.py          # Unit tests (pytest)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/smartdigest.git
cd smartdigest
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
            
### 4. Run the app
```bash
streamlit run app.py
```

That's it — no API keys, no `.env` file, no sign-ups needed.

---

## 🧪 Running Tests
```bash
pip install pytest
pytest tests/
```

---

## 🌐 Deploying to Streamlit Community Cloud

1. Push this repo to your own GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub
3. Select the repo, set the main file to `app.py`
4. Deploy — you'll get a public link to add to your portfolio/resume

---

## 🔮 Future Improvements

- Add support for scraping paywalled/JS-heavy sites using `Selenium` or `Playwright`
- Multi-language support for non-English articles
- Browser extension version for one-click summarization
- Optional plug-in for a transformer-based summarizer for even sharper summaries

---

## 📄 License

MIT License — free to use and modify.

---

Built by [Your Name] as part of a personal Python project portfolio.
