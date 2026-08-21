#!/usr/bin/env python3
"""
報徳学園出身者 ニュース収集エージェント
毎週実行して記事を収集・要約し、月次レポートを生成する。
"""
import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# agents/alumni-news をパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from collector import collect_articles, mock_articles
from deduplicator import filter_new_articles
from summarizer import summarize_articles
from reporter import generate_report
from emailer import send_report


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="報徳学園出身者ニュース収集エージェント")
    p.add_argument("--dry-run", action="store_true", help="Claude API を呼ばず要約をスキップ")
    p.add_argument("--no-email", action="store_true", help="メール送信をスキップ")
    p.add_argument("--verbose", "-v", action="store_true", help="デバッグログを表示")
    p.add_argument("--month", help="対象月（YYYY-MM形式、省略時は当月）")
    p.add_argument("--test", action="store_true", help="モック記事でエンドツーエンドテスト実行")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger("main")

    target_date: datetime | None = None
    if args.month:
        try:
            target_date = datetime.strptime(args.month, "%Y-%m").replace(tzinfo=timezone.utc)
        except ValueError:
            logger.error("--month の形式が不正です。YYYY-MM で指定してください。")
            sys.exit(1)

    logger.info("=== 報徳学園出身者ニュース収集開始 ===")

    # 1. 記事収集
    if args.test:
        logger.info("[テストモード] モック記事を使用します")
        articles = mock_articles()
    else:
        articles = collect_articles()
    if not articles:
        logger.info("記事が取得できませんでした。終了します。")
        return

    # 2. 重複排除
    new_articles = filter_new_articles(articles)
    if not new_articles:
        logger.info("新規記事なし。終了します。")
        return

    # 3. 要約
    summarized = summarize_articles(new_articles, dry_run=args.dry_run)

    # 4. レポート生成
    report_path = generate_report(summarized, target_date=target_date)
    logger.info("レポートファイル: %s", report_path)

    # 5. メール送信
    if not args.no_email:
        send_report(report_path)

    logger.info("=== 完了: %d 件の新規記事を処理しました ===", len(new_articles))
    print(f"\nレポート: {report_path}")


if __name__ == "__main__":
    main()
