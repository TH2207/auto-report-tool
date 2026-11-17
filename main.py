import logging
from datetime import datetime
from collector import fetch_quotes
from processor import validate_and_process
from exporter import export_styled_excel

# ログ出力のフォーマット設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    # 1. 収集
    raw_data = fetch_quotes("http://quotes.toscrape.com/")

    # 2. 整形・検証
    df = validate_and_process(raw_data)

    # 3. 出力（ファイル名に実行日付を付与）
    today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/quotes_report_{today_str}.xlsx"
    export_styled_excel(df, output_file)

if __name__ == "__main__":
    main()
