"""月次レポートのメール送信（将来実装）"""
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import EMAIL_CONFIG

logger = logging.getLogger(__name__)


def send_report(report_path: Path, subject: str | None = None) -> bool:
    """
    月次レポートをメールで送信する。
    EMAIL_CONFIG の enabled が False の場合は何もしない。

    必要な環境変数:
        SMTP_HOST, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD,
        EMAIL_FROM, EMAIL_TO (カンマ区切り複数アドレス可)
    """
    cfg = EMAIL_CONFIG
    if not cfg["enabled"]:
        logger.info("メール送信は無効 (EMAIL_CONFIG.enabled=False)。スキップします。")
        return False

    if not cfg["to_addresses"] or not cfg["username"]:
        logger.error("メール設定が不完全です。環境変数を確認してください。")
        return False

    report_text = report_path.read_text(encoding="utf-8")
    month_label = report_path.stem  # 例: 2025-08
    subject = subject or f"【報友会東京支部】報徳学園出身者 活動レポート {month_label}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = cfg["from_address"]
    msg["To"] = ", ".join(cfg["to_addresses"])

    # プレーンテキスト版
    msg.attach(MIMEText(report_text, "plain", "utf-8"))

    # HTML 版（マークダウンを簡易変換）
    try:
        import markdown
        html_body = markdown.markdown(report_text, extensions=["tables"])
    except ImportError:
        html_body = f"<pre>{report_text}</pre>"
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(cfg["username"], cfg["password"])
            server.sendmail(cfg["from_address"], cfg["to_addresses"], msg.as_string())
        logger.info("メール送信完了: %s 宛", cfg["to_addresses"])
        return True
    except smtplib.SMTPException as e:
        logger.error("メール送信失敗: %s", e)
        return False


# TODO: Gmail API を使った OAuth 認証版を追加予定
# def send_report_via_gmail_api(report_path, credentials_file): ...
