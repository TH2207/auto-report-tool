# 📊 自動データ収集・Excelレポート生成ツール

Python（Requests / BeautifulSoup / Pandas / Openpyxl）および Streamlit を用いて、Web上のデータ収集から品質バリデーション、さらに人間が手作業で作ったような「装飾付きExcelレポートの自動生成・UI提供」までをワンストップで行う業務自動化プロダクトです。

## 🛠 主な機能

1. **自動データ収集 (Collector)**: 指定したURLからターゲットデータを自動でスクレイピング。
2. **検証・データ整形 (Processor)**: 必須項目の欠損チェックや重複排除など、システム検証の知見を活かした厳格なバリデーションを実施。
3. **魅せるExcel出力 (Exporter)**: `openpyxl` を用いて、ヘッダーの配色、罫線、条件付きハイライト（注目行の黄色背景）を自動適用。
4. **Web UI連携 (Streamlit)**: 黒い画面を使わず、ブラウザ上の直感的な操作で実行・プレビュー・ダウンロードが可能。

## 📁 フォルダ構成

auto_report_tool/
├── app.py # Streamlit Webアプリ本体
├── collector.py # データ収集モジュール
├── processor.py # バリデーション・整形モジュール
├── exporter.py # Excel装飾・出力モジュール
├── requirements.txt # 必要ライブラリ一覧
└── .gitignore # 除外設定
