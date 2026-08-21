"""Google News RSS / Yahoo Japan News から記事を収集する"""
import time
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlencode, quote_plus

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from config import (
    SEARCH_QUERIES,
    GNEWS_RSS_BASE,
    GNEWS_PARAMS,
    MAX_ARTICLES_PER_QUERY,
    KANTO_UNIVERSITY_KEYWORDS,
)

logger = logging.getLogger(__name__)

# Yahoo Japan ニュース RSS (HTTPS プロキシでも通りやすい)
YAHOO_RSS_BASE = "https://news.yahoo.co.jp/rss/search"

# 代替 RSS フィード
ALT_FEEDS = [
    # Bing News (英語インターフェース経由で日本語検索)
    "https://www.bing.com/news/search?q={query}&format=rss&mkt=ja-JP",
]


@dataclass
class Article:
    title: str
    url: str
    source: str
    published: datetime
    snippet: str
    kanto_score: int = 0

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "published": self.published.isoformat(),
            "snippet": self.snippet,
            "kanto_score": self.kanto_score,
        }

    @staticmethod
    def from_dict(d: dict) -> "Article":
        return Article(
            title=d["title"],
            url=d["url"],
            source=d.get("source", ""),
            published=date_parser.parse(d["published"]),
            snippet=d.get("snippet", ""),
            kanto_score=d.get("kanto_score", 0),
        )


def _calc_kanto_score(text: str) -> int:
    score = 0
    for kw in KANTO_UNIVERSITY_KEYWORDS:
        if kw in text:
            score += 10
    for kw in ["首都圏", "関東", "東京", "神奈川", "埼玉", "千葉", "茨城", "栃木", "群馬"]:
        if kw in text:
            score += 3
    return score


def _fetch_rss(url: str) -> bytes | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AlumniNewsBot/1.0)",
        "Accept-Language": "ja,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.content
    except requests.RequestException as e:
        logger.warning("RSS取得失敗: %s", e)
        return None


def _parse_entries(content: bytes) -> list[Article]:
    feed = feedparser.parse(content)
    articles = []

    for entry in feed.entries[:MAX_ARTICLES_PER_QUERY]:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        if not title or not link:
            continue

        source = ""
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            title, source = parts[0].strip(), parts[1].strip()

        snippet = BeautifulSoup(
            entry.get("summary", ""), "html.parser"
        ).get_text(separator=" ").strip()[:400]

        try:
            published = date_parser.parse(entry.get("published", ""))
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            published = datetime.now(timezone.utc)

        kanto_score = _calc_kanto_score(title + " " + snippet)
        articles.append(
            Article(title=title, url=link, source=source,
                    published=published, snippet=snippet, kanto_score=kanto_score)
        )

    return articles


def _search_gnews(query: str) -> list[Article]:
    params = {**GNEWS_PARAMS, "q": query}
    url = f"{GNEWS_RSS_BASE}?{urlencode(params, quote_via=quote_plus)}"
    content = _fetch_rss(url)
    return _parse_entries(content) if content else []


def _search_yahoo(query: str) -> list[Article]:
    url = f"{YAHOO_RSS_BASE}?p={quote_plus(query)}&ei=UTF-8"
    content = _fetch_rss(url)
    return _parse_entries(content) if content else []


def _search_bing(query: str) -> list[Article]:
    url = ALT_FEEDS[0].format(query=quote_plus(query))
    content = _fetch_rss(url)
    return _parse_entries(content) if content else []


def collect_articles() -> list[Article]:
    """複数ソースから記事を収集して首都圏スコア降順で返す"""
    seen_urls: set[str] = set()
    all_articles: list[Article] = []

    def add(arts: list[Article]) -> int:
        count = 0
        for art in arts:
            if art.url not in seen_urls:
                seen_urls.add(art.url)
                all_articles.append(art)
                count += 1
        return count

    for query in SEARCH_QUERIES:
        logger.info("Google News 検索: %s", query)
        added = add(_search_gnews(query))
        if added == 0:
            logger.info("Yahoo News フォールバック: %s", query)
            added = add(_search_yahoo(query))
        if added == 0:
            logger.info("Bing News フォールバック: %s", query)
            add(_search_bing(query))
        time.sleep(1.5)

    all_articles.sort(
        key=lambda a: (a.kanto_score, a.published.timestamp()), reverse=True
    )
    logger.info("収集記事数: %d", len(all_articles))
    return all_articles


def mock_articles() -> list[Article]:
    """テスト・デモ用のモック記事"""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    return [
        Article(
            title="報徳学園OBの田中選手が早稲田大学野球部で活躍",
            url="https://example.com/article/1",
            source="スポーツ新聞",
            published=now - timedelta(days=2),
            snippet="報徳学園出身の田中選手が早稲田大学野球部の主力として春季リーグで好成績を収めている。",
            kanto_score=_calc_kanto_score("早稲田大学 東京"),
        ),
        Article(
            title="報徳学園卒の研究者が東京大学でAI研究に従事",
            url="https://example.com/article/2",
            source="教育ニュース",
            published=now - timedelta(days=5),
            snippet="報徳学園を卒業後、東京大学大学院に進学した山田氏が最先端のAI研究に取り組んでいる。",
            kanto_score=_calc_kanto_score("東京大学 東京"),
        ),
        Article(
            title="報徳学園のOBが兵庫県で起業家として活躍",
            url="https://example.com/article/3",
            source="地方経済紙",
            published=now - timedelta(days=3),
            snippet="報徳学園出身の起業家が兵庫県内でスタートアップを設立し、地域経済の活性化に貢献している。",
            kanto_score=0,
        ),
    ]
