"""
scraper.py
----------
Fetches a webpage and extracts the main readable article text,
stripping out navigation, ads, scripts, and other clutter.
"""

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Tags that almost never contain real article content
TAGS_TO_REMOVE = ["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]


class ScraperError(Exception):
    """Raised when a page cannot be fetched or no readable content is found."""
    pass


def fetch_html(url: str, timeout: int = 10) -> str:
    """Download raw HTML for a given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.MissingSchema:
        raise ScraperError("Invalid URL. Make sure it starts with http:// or https://")
    except requests.exceptions.ConnectionError:
        raise ScraperError("Could not connect to that URL. Check your internet or the link.")
    except requests.exceptions.Timeout:
        raise ScraperError("The request timed out. The site may be slow or blocking requests.")
    except requests.exceptions.HTTPError as e:
        raise ScraperError(f"The site returned an error: {e}")

    return response.text


def extract_article_text(html: str) -> str:
    """
    Parse HTML and pull out the main article text.
    Strategy: remove junk tags, then grab all <p> tags (most article
    content lives inside paragraph tags on the vast majority of sites).
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(TAGS_TO_REMOVE):
        tag.decompose()

    # Try to find a common "article body" container first for cleaner results
    candidates = soup.find_all(["article", "main"])
    search_root = candidates[0] if candidates else soup

    paragraphs = search_root.find_all("p")
    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    if len(text.split()) < 50:
        # Fallback: page might not use <article>/<main>, search whole soup
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    if len(text.split()) < 30:
        raise ScraperError(
            "Couldn't find enough readable article text on this page. "
            "It might be behind a login, paywall, or heavily JavaScript-rendered."
        )

    return text


def get_page_title(html: str) -> str:
    """Grab the page <title> for display purposes."""
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Untitled Page"


def scrape_article(url: str) -> dict:
    """
    Main entry point: given a URL, returns a dict with title and cleaned text.
    """
    html = fetch_html(url)
    title = get_page_title(html)
    text = extract_article_text(html)
    return {"title": title, "text": text, "url": url}
