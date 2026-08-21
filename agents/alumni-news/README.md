# 報徳学園出身者 ニュース収集エージェント

報徳学園出身者の活動・活躍ニュースを毎週自動収集し、首都圏大学での活躍を優先して月次マークダウンレポートを生成するAIエージェントです。

## 機能

- **記事収集**: Google News RSS / Yahoo Japan News / Bing News から「報徳学園」関連記事を収集
- **首都圏優先**: 首都圏の大学（早稲田・東大・慶應など）に関連する記事を上位に配置
- **重複排除**: URL一致 + タイトル類似度でクロスソース重複を除去（90日間キャッシュ）
- **AI要約**: Claude API (claude-haiku) で各記事を100〜150文字に要約
- **月次レポート**: `reports/YYYY-MM.md` にマークダウン形式で蓄積
- **メール送信**: SMTP 経由で月次レポートを配信（将来実装・現在は設定で有効化可能）

## セットアップ

```bash
cd agents/alumni-news
pip install -r requirements.txt
```

### 環境変数

```bash
# 必須: Claude API キー（要約に使用）
export ANTHROPIC_API_KEY="sk-ant-..."

# メール送信を有効にする場合
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export EMAIL_USERNAME="your@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_FROM="your@gmail.com"
export EMAIL_TO="recipient1@example.com,recipient2@example.com"
```

## 使い方

```bash
# 通常実行（週次）
python3 main.py

# テストモード（モック記事・API不使用）
python3 main.py --test --dry-run --no-email

# 特定の月のレポートに追記
python3 main.py --month 2025-07

# Claude API を使わず要約をスキップ
python3 main.py --dry-run

# デバッグログ表示
python3 main.py --verbose
```

## ファイル構成

```
agents/alumni-news/
├── main.py            # エントリーポイント
├── config.py          # 設定（クエリ・API設定・パス）
├── collector.py       # ニュース記事収集（Google News / Yahoo / Bing RSS）
├── deduplicator.py    # 重複排除（URLキャッシュ＋タイトル類似度）
├── summarizer.py      # Claude API による要約生成
├── reporter.py        # マークダウンレポート生成・更新
├── emailer.py         # メール送信（SMTP）
├── requirements.txt   # Python 依存パッケージ
├── data/              # 重複排除キャッシュ（Git 管理外）
│   └── seen_articles.json
└── reports/           # 月次レポート（Git 管理）
    └── YYYY-MM.md
```

## レポート形式

```markdown
# 報徳学園出身者 活動レポート 2025年08月

## 首都圏大学での活躍
### 記事タイトル 🏫首都圏大学
- **日付**: 2025-08-15
- **出典**: [メディア名](URL)
- **収集日**: 2025-08-21
AI による要約（100〜150文字）

## その他の活動
...
```

## 週次自動化

### cron（ローカル環境）
```cron
# 毎週月曜 8:00 に実行
0 8 * * 1 cd /path/to/keykeykey && python3 agents/alumni-news/main.py >> /tmp/alumni-news.log 2>&1
```

### Claude Code Remote ルーティン
本リポジトリでは Claude Code Remote の週次ルーティンで自動実行されます。

## メール送信の有効化

`config.py` の `EMAIL_CONFIG["enabled"]` を `True` に変更し、上記環境変数を設定してください。
Gmail を使う場合は「アプリパスワード」を生成して `EMAIL_PASSWORD` に設定します。

> 将来的に Gmail API (OAuth) 版への移行も予定しています（`emailer.py` の TODO コメント参照）。
