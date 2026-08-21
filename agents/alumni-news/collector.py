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
    """テスト・デモ用のモック記事（現実的なサンプル）"""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    return [
        Article(
            title="報徳学園出身の渡辺投手、慶應義塾大学野球部でリーグ最多奪三振",
            url="https://sportsnews.example.com/baseball/20260818-waseda",
            source="スポーツ報知",
            published=now - timedelta(days=3),
            snippet=(
                "慶應義塾大学野球部の渡辺投手（報徳学園出身・3年）が東京六大学秋季リーグ開幕節で"
                "先発完投し9奪三振を記録した。昨秋のリーグ戦から通算奪三振数は48となり、"
                "現役選手でトップに立った。「報徳で鍛えた制球力が今に生きている」と話した。"
            ),
            kanto_score=_calc_kanto_score("慶應義塾大学 東京 六大学"),
        ),
        Article(
            title="早稲田大学理工学術院・中村准教授（報徳学園卒）が量子コンピュータ研究で文科省賞受賞",
            url="https://education.example.com/science/20260815-nakamura",
            source="日本教育新聞",
            published=now - timedelta(days=6),
            snippet=(
                "早稲田大学先進理工学部の中村健一准教授（報徳学園高校→東京大学大学院）が"
                "量子誤り訂正アルゴリズムの研究で令和8年度文部科学大臣賞（若手研究者部門）を受賞した。"
                "中村准教授は「報徳の『積小為大』の精神で一歩一歩研究を積み上げてきた」とコメントした。"
            ),
            kanto_score=_calc_kanto_score("早稲田大学 東京大学 東京"),
        ),
        Article(
            title="明治大学ラグビー部、報徳学園出身の田所主将率いて全国大学選手権8強",
            url="https://rugby.example.com/university/20260812-meiji",
            source="ラグビーマガジン",
            published=now - timedelta(days=9),
            snippet=(
                "明治大学ラグビー部主将・田所龍斗選手（報徳学園出身・4年）が"
                "全国大学選手権準々決勝でチームを牽引し8強入りを果たした。"
                "田所主将は高校時代から全国屈指のフランカーとして知られ、"
                "大学でもキャプテンシーと突破力でチームを引っ張っている。"
                "卒業後はトップリーグへの進路が内定している。"
            ),
            kanto_score=_calc_kanto_score("明治大学 東京"),
        ),
        Article(
            title="東京工業大学院生・鈴木氏（報徳学園卒）が国際ロボコンで金賞",
            url="https://tech.example.com/robotics/20260810-suzuki",
            source="産経新聞デジタル",
            published=now - timedelta(days=11),
            snippet=(
                "東京工業大学大学院の鈴木翔太氏（報徳学園出身）が率いるチームが"
                "国際ロボットコンテスト「RoboCup 2026 Bangkok」の自律移動部門で金賞を獲得した。"
                "鈴木氏は「中高時代に科学部で培ったものづくりの基礎が原点」と語った。"
            ),
            kanto_score=_calc_kanto_score("東京工業大学 東京"),
        ),
        Article(
            title="報徳学園OBの起業家・松本氏が神戸でフードテックスタートアップを設立",
            url="https://startup.example.com/kobe/20260808-matsumoto",
            source="神戸新聞",
            published=now - timedelta(days=13),
            snippet=(
                "報徳学園出身の松本誠司氏（34）が神戸市内でフードテクノロジー企業「Hotoku Foods」を設立した。"
                "同社は農業廃棄物を活用した代替タンパク質の製造技術を開発しており、"
                "設立初年度からベンチャーキャピタルより3億円の資金調達に成功した。"
            ),
            kanto_score=0,
        ),
        Article(
            title="法政大学陸上競技部・伊藤選手（報徳学園出身）、関東インカレ5000mで3位入賞",
            url="https://athletics.example.com/kanto/20260805-ito",
            source="月刊陸上競技",
            published=now - timedelta(days=16),
            snippet=(
                "関東学生陸上競技連盟主催の関東インカレにおいて、法政大学陸上競技部の"
                "伊藤涼太選手（報徳学園出身・2年）が5000m決勝で13分42秒の自己ベストを更新し3位に入賞した。"
                "報徳学園時代は都大路（全国高校駅伝）でも区間賞を獲得している実力者。"
            ),
            kanto_score=_calc_kanto_score("法政大学 関東 東京"),
        ),
        Article(
            title="報徳学園同窓会（関東支部）が8月例会を開催、卒業生100名超が参加",
            url="https://alumni.example.com/kanto/20260803-meeting",
            source="報徳学園同窓会報",
            published=now - timedelta(days=18),
            snippet=(
                "報徳学園同窓会関東支部（報友会東京支部）は8月3日に都内で例会を開催し、"
                "卒業生・在校生保護者を含む105名が参加した。懇親会では首都圏で活躍する"
                "若手卒業生による講演も行われ、大学・社会人問わず報徳ネットワークの"
                "強固さを示す会となった。"
            ),
            kanto_score=_calc_kanto_score("関東 東京"),
        ),
    ]
