import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def fetch_quotes(url: str = "http://quotes.toscrape.com/") -> list[dict]:
    """指定URLから名言データを収集する"""
    logger.info(f"データ収集を開始します: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"通信エラーが発生しました: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")

    raw_data = []
    for block in quote_blocks:
        text_el = block.find("span", class_="text")
        author_el = block.find("small", class_="author")
        tags_el = block.find_all("a", class_="tag")

        raw_data.append({
            "quote": text_el.get_text(strip=True) if text_el else "",
            "author": author_el.get_text(strip=True) if author_el else "",
            "tags": ", ".join([t.get_text(strip=True) for t in tags_el])
        })

    logger.info(f"{len(raw_data)} 件の生データを取得しました。")
    return raw_data
