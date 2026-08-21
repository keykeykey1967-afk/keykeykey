"""既見記事の管理と重複排除"""
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

from config import CACHE_FILE, CACHE_RETENTION_DAYS

logger = logging.getLogger(__name__)


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("キャッシュ読み込み失敗: %s", e)
        return {}


def _save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def _normalize_title(title: str) -> str:
    """タイトルを正規化して類似判定に使う"""
    import unicodedata, re
    title = unicodedata.normalize("NFKC", title).lower()
    title = re.sub(r"[\s　]+", " ", title).strip()
    return title


def _is_similar_title(t1: str, t2: str) -> bool:
    """先頭30文字が一致すれば同一記事とみなす"""
    n1, n2 = _normalize_title(t1)[:30], _normalize_title(t2)[:30]
    return n1 == n2 and len(n1) > 5


def filter_new_articles(articles: list) -> list:
    """新規記事のみを返し、キャッシュを更新する"""
    cache = _load_cache()
    cutoff = datetime.now(timezone.utc) - timedelta(days=CACHE_RETENTION_DAYS)

    # 古いキャッシュを削除
    cache = {
        url: meta
        for url, meta in cache.items()
        if datetime.fromisoformat(meta["seen_at"]) > cutoff
    }

    cached_titles = [meta["title"] for meta in cache.values()]
    new_articles = []

    for art in articles:
        if art.url in cache:
            continue
        # URL が違っても類似タイトルなら重複とみなす
        if any(_is_similar_title(art.title, ct) for ct in cached_titles):
            logger.debug("タイトル重複スキップ: %s", art.title)
            continue

        new_articles.append(art)
        cache[art.url] = {
            "title": art.title,
            "seen_at": datetime.now(timezone.utc).isoformat(),
        }
        cached_titles.append(art.title)

    _save_cache(cache)
    logger.info("新規記事: %d 件（重複除外後）", len(new_articles))
    return new_articles
