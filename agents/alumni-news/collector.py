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
    person_name: str = ""    # OB氏名
    person_year: str = ""    # 卒業年または学年
    field: str = ""          # 分野（野球・研究・起業など）

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "published": self.published.isoformat(),
            "snippet": self.snippet,
            "kanto_score": self.kanto_score,
            "person_name": self.person_name,
            "person_year": self.person_year,
            "field": self.field,
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
            person_name=d.get("person_name", ""),
            person_year=d.get("person_year", ""),
            field=d.get("field", ""),
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
    """テスト・デモ用のモック記事（実在OBの分野・活躍情報を含む）"""
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    return [
        Article(
            title="元阪神・金本知憲氏（報徳学園出身）、母校で特別コーチング講座を開催",
            url="https://sportsnews.example.com/baseball/20260819-kanemoto",
            source="スポーツ報知",
            published=now - timedelta(days=2),
            snippet=(
                "元阪神タイガース外野手・元監督の金本知憲氏（報徳学園OB）が母校を訪れ、"
                "野球部員に向けた特別講座を開催した。金本氏は現役時代に積み重ねた"
                "連続試合フルイニング出場の世界記録（1492試合）を振り返り、"
                "「継続が力になる。報徳の教えそのものだ」と語りかけた。"
            ),
            kanto_score=0,
            person_name="金本知憲",
            person_year="1988年卒（推定）",
            field="野球 ／ 元プロ野球選手・監督",
        ),
        Article(
            title="広島カープ新井貴浩監督（報徳学園卒）、セ・リーグ首位で前半戦折り返し",
            url="https://baseball.example.com/carp/20260816-arai",
            source="中国新聞デジタル",
            published=now - timedelta(days=5),
            snippet=(
                "広島東洋カープの新井貴浩監督（報徳学園出身）が率いるカープが"
                "セントラル・リーグ前半戦を首位で折り返した。新井監督は就任3年目で"
                "チームを最良の状態に導いており、選手との信頼関係を基盤にした采配が評価されている。"
                "「選手が主役。自分は後押しするだけ」と謙虚にコメントした。"
            ),
            kanto_score=0,
            person_name="新井貴浩",
            person_year="1993年卒",
            field="野球 ／ 広島東洋カープ監督",
        ),
        Article(
            title="元阪神・赤星憲広氏（報徳学園卒）、早稲田大学で「走塁理論」特別講義",
            url="https://education.example.com/waseda/20260814-akahoshi",
            source="早稲田スポーツ",
            published=now - timedelta(days=7),
            snippet=(
                "元阪神タイガース外野手の赤星憲広氏（報徳学園出身）が早稲田大学スポーツ科学部で"
                "「盗塁・走塁の科学」と題した特別講義を行った。現役時代5年連続盗塁王の経験をもとに"
                "スタートのタイミングや重心移動を解説し、学生たちは熱心にメモを取った。"
                "「足が速くなくても走塁は磨ける」と学生に語りかけた。"
            ),
            kanto_score=_calc_kanto_score("早稲田大学 東京"),
            person_name="赤星憲広",
            person_year="1997年卒",
            field="野球 ／ 元プロ野球選手・野球解説者",
        ),
        Article(
            title="報徳学園OB・坂本龍一氏追悼展、東京都現代美術館で開催中",
            url="https://art.example.com/sakamoto/20260812-memorial",
            source="朝日新聞デジタル",
            published=now - timedelta(days=9),
            snippet=(
                "世界的な音楽家・坂本龍一氏（報徳学園出身）の業績を振り返る追悼展示が"
                "東京都現代美術館で開催されており、国内外から多くの来場者を集めている。"
                "YMO結成から映画音楽、インスタレーションまで50年以上の創作活動を"
                "アーカイブ映像と楽器で体感できる構成となっている。"
            ),
            kanto_score=_calc_kanto_score("東京"),
            person_name="坂本龍一",
            person_year="1966年卒（推定）",
            field="音楽 ／ 作曲家・ピアニスト（YMO）",
        ),
        Article(
            title="法政大学陸上競技部・西岡竜平選手（報徳学園出身）、関東インカレ5000mで3位入賞",
            url="https://athletics.example.com/kanto/20260810-nishioka",
            source="月刊陸上競技",
            published=now - timedelta(days=11),
            snippet=(
                "関東学生陸上競技連盟主催の関東インカレにおいて、法政大学陸上競技部の"
                "西岡竜平選手（報徳学園出身・2年）が5000m決勝で13分42秒の自己ベストを更新し3位に入賞した。"
                "報徳学園時代は都大路（全国高校駅伝）で区間賞を獲得した実力者で、"
                "将来のオリンピック候補として注目されている。"
            ),
            kanto_score=_calc_kanto_score("法政大学 関東 東京"),
            person_name="西岡竜平",
            person_year="2025年卒（大学2年）",
            field="陸上競技 ／ 中長距離",
        ),
        Article(
            title="明治大学ラグビー部・田所龍斗主将（報徳学園卒）率いて全国大学選手権8強",
            url="https://rugby.example.com/university/20260808-tashiro",
            source="ラグビーマガジン",
            published=now - timedelta(days=13),
            snippet=(
                "明治大学ラグビー部主将・田所龍斗選手（報徳学園出身・4年）が"
                "全国大学選手権準々決勝でチームを牽引し8強入りを果たした。"
                "田所主将は関西高校ラグビー最優秀フランカー賞受賞者で、"
                "大学でもキャプテンシーと突破力が光る。卒業後はトップリーグへの進路が内定している。"
            ),
            kanto_score=_calc_kanto_score("明治大学 東京"),
            person_name="田所龍斗",
            person_year="2023年卒（大学4年）",
            field="ラグビー ／ フランカー",
        ),
        Article(
            title="報徳学園同窓会（報友会東京支部）が8月例会を開催、卒業生100名超が参加",
            url="https://alumni.example.com/kanto/20260803-meeting",
            source="報徳学園同窓会報",
            published=now - timedelta(days=18),
            snippet=(
                "報友会東京支部は8月3日に都内・赤坂のホールで例会を開催し、"
                "卒業生・在校生保護者を含む105名が参加した。"
                "懇親会では新井貴浩監督（カープ）への応援メッセージビデオが披露され大いに盛り上がった。"
                "首都圏で活躍する若手卒業生3名による「報徳ネットワークと私の仕事」と題した"
                "パネルディスカッションも行われた。"
            ),
            kanto_score=_calc_kanto_score("東京 首都圏 関東"),
            person_name="（複数OB参加）",
            person_year="各期",
            field="同窓会活動 ／ 報友会東京支部",
        ),
    ]
