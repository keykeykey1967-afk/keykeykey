"""月次マークダウンレポートを生成・更新する"""
import logging
from datetime import datetime, timezone
from pathlib import Path

from config import REPORTS_DIR

logger = logging.getLogger(__name__)


def _report_path(year: int, month: int) -> Path:
    return REPORTS_DIR / f"{year:04d}-{month:02d}.md"


def _section_header(year: int, month: int) -> str:
    return f"# 報徳学園出身者 活動レポート {year}年{month:02d}月\n\n"


def _article_block(art, summary: str, run_date: str) -> str:
    date_str = art.published.strftime("%Y-%m-%d")
    kanto_tag = " 🏫首都圏大学" if art.kanto_score >= 10 else ""
    lines = [
        f"### {art.title}{kanto_tag}",
        f"- **日付**: {date_str}",
        f"- **出典**: [{art.source or art.url}]({art.url})",
        f"- **収集日**: {run_date}",
    ]
    if getattr(art, "person_name", ""):
        lines.append(f"- **OB氏名**: {art.person_name}")
    if getattr(art, "person_year", ""):
        lines.append(f"- **卒業年**: {art.person_year}")
    if getattr(art, "field", ""):
        lines.append(f"- **分野**: {art.field}")
    lines += ["", summary, "", "---", ""]
    return "\n".join(lines)


def generate_report(summarized: list, target_date: datetime | None = None) -> Path:
    """当月レポートに新規記事を追記し、ファイルパスを返す"""
    now = target_date or datetime.now(timezone.utc)
    year, month = now.year, now.month
    run_date = now.strftime("%Y-%m-%d")
    report_path = _report_path(year, month)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if not report_path.exists():
        header = _section_header(year, month)
        header += (
            f"> 生成: {run_date}  \n"
            f"> 対象: 報徳学園出身者の活動・活躍ニュース（首都圏大学優先）\n\n"
        )
        report_path.write_text(header, encoding="utf-8")
        logger.info("新規レポート作成: %s", report_path)

    if not summarized:
        logger.info("新規記事なし。レポートは更新しません。")
        return report_path

    # 首都圏記事を先に、その他を後に並べる
    kanto = [s for s in summarized if s["article"].kanto_score >= 10]
    others = [s for s in summarized if s["article"].kanto_score < 10]
    ordered = kanto + others

    blocks = []
    if kanto and others:
        blocks.append(f"## 首都圏大学での活躍 ({run_date} 更新)\n\n")
        for s in kanto:
            blocks.append(_article_block(s["article"], s["summary"], run_date))
        blocks.append("## その他の活動\n\n")
        for s in others:
            blocks.append(_article_block(s["article"], s["summary"], run_date))
    else:
        blocks.append(f"## 活動ニュース ({run_date} 更新)\n\n")
        for s in ordered:
            blocks.append(_article_block(s["article"], s["summary"], run_date))

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(blocks))

    logger.info("レポート更新: %s (%d 件追加)", report_path, len(summarized))
    return report_path
