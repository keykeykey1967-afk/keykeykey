"""Claude API を使って記事を要約する"""
import logging

from config import ANTHROPIC_API_KEY, SUMMARIZE_MODEL, SUMMARIZE_MAX_TOKENS

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        try:
            import anthropic
            _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError("anthropic パッケージが必要です: pip install anthropic")
    return _client


def summarize_article(title: str, snippet: str, source: str = "") -> str:
    """タイトルとスニペットから日本語要約を生成する"""
    if not ANTHROPIC_API_KEY:
        return snippet[:150] + ("…" if len(snippet) > 150 else "")

    prompt = f"""以下は報徳学園（兵庫県宝塚市の中高一貫校）出身者に関するニュース記事です。
記事の内容を100〜150文字の日本語で簡潔に要約してください。
特に首都圏の大学での活動・活躍が含まれる場合はその点を強調してください。

タイトル: {title}
出典: {source}
本文抜粋: {snippet}

要約:"""

    try:
        client = _get_client()
        message = client.messages.create(
            model=SUMMARIZE_MODEL,
            max_tokens=SUMMARIZE_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.warning("要約失敗 (%s): %s — スニペットを使用", title[:30], e)
        return snippet[:150] + ("…" if len(snippet) > 150 else "")


def summarize_articles(articles: list, dry_run: bool = False) -> list:
    """全記事に要約を追加して返す"""
    results = []
    for i, art in enumerate(articles, 1):
        logger.info("要約中 [%d/%d]: %s", i, len(articles), art.title[:40])
        summary = (
            art.snippet[:150] if dry_run
            else summarize_article(art.title, art.snippet, art.source)
        )
        results.append({"article": art, "summary": summary})
    return results
