import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 既存のモジュールをインポート
from collector import fetch_quotes
from processor import validate_and_process
from exporter import export_styled_excel

# ページの設定
st.set_page_config(
    page_title="自動データ収集・Excelレポート生成ツール",
    page_icon="📊",
    layout="centered"
)

st.title("📊 自動データ収集・レポート生成ツール")
st.markdown("""
このツールは、指定したWebサイトからデータを自動収集し、**品質チェック（バリデーション）**を行った上で、**見やすく装飾されたExcelレポート**をワンクリックで生成するツールです。
""")

st.divider()

# 操作パネル
st.subheader("1. 実行コントロール")
target_url = st.text_input("収集対象URL", value="http://quotes.toscrape.com/")

if st.button("🚀 データを収集してレポートを生成する", type="primary"):
    with st.spinner("データを収集し、整形・装飾処理を実行中です..."):
        # 1. 収集
        raw_data = fetch_quotes(target_url)
        
        if not raw_data:
            st.error("データの取得に失敗しました。URLを確認してください。")
        else:
            # 2. 整形・検証
            df = validate_and_process(raw_data)
            
            # 3. 出力ファイルパスの生成
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"quotes_report_{today_str}.xlsx")
        
        # Excel出力実行
        export_styled_excel(df, output_file)
        
        st.success(f"レポートの生成が完了しました！（有効データ数: {len(df)} 件）")
        
        # プレビュー表示
        st.subheader("2. 取得・整形データプレビュー")
        st.dataframe(df, use_container_width=True)
        
        # ダウンロードボタンの設置
        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 生成されたExcelレポートをダウンロード",
                data=f,
                file_name=os.path.basename(output_file),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )