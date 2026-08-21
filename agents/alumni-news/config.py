"""エージェント設定"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ---- 検索設定 ----
SEARCH_QUERIES = [
    "報徳学園",
    "報徳学園 出身 大学",
    "報徳学園 卒業 首都圏",
    "報徳学園 東京 活躍",
    "報徳学園OB 関東",
]

# 首都圏大学キーワード（スコアリング優先度付け用）
KANTO_UNIVERSITY_KEYWORDS = [
    "東京大学", "早稲田大学", "慶應義塾大学", "明治大学", "法政大学",
    "中央大学", "青山学院大学", "立教大学", "専修大学", "日本大学",
    "東京工業大学", "一橋大学", "筑波大学", "千葉大学", "横浜国立大学",
    "東京理科大学", "上智大学", "学習院大学", "津田塾大学", "東京農業大学",
    "首都大学", "東京都立大学", "神奈川大学", "関東学院大学",
]

# ---- Claude API 設定 ----
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUMMARIZE_MODEL = "claude-haiku-4-5-20251001"
SUMMARIZE_MAX_TOKENS = 300

# ---- ファイルパス ----
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
CACHE_FILE = DATA_DIR / "seen_articles.json"

# ---- メール設定（将来用）----
EMAIL_CONFIG = {
    "enabled": False,
    "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "username": os.getenv("EMAIL_USERNAME", ""),
    "password": os.getenv("EMAIL_PASSWORD", ""),
    "from_address": os.getenv("EMAIL_FROM", ""),
    "to_addresses": os.getenv("EMAIL_TO", "").split(",") if os.getenv("EMAIL_TO") else [],
}

# ---- Google News RSS ----
GNEWS_RSS_BASE = "https://news.google.com/rss/search"
GNEWS_PARAMS = {"hl": "ja", "gl": "JP", "ceid": "JP:ja"}

# 1回の収集で取得する最大記事数
MAX_ARTICLES_PER_QUERY = 20
# キャッシュ保持日数
CACHE_RETENTION_DAYS = 90
