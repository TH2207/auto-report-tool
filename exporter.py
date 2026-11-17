import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import logging

logger = logging.getLogger(__name__)

def export_styled_excel(df: pd.DataFrame, output_path: str) -> None:
    """整形済みDataFrameを装飾付きExcelとして出力する"""
    if df.empty:
        logger.warning("出力データがないため、Excel生成をスキップします。")
        return

    # まずpandasで基礎データを書き出し
    df.to_excel(output_path, index=False, sheet_name="収集レポート")

    # openpyxlで読み直してデザインを適用
    wb = openpyxl.load_workbook(output_path)
    ws = wb["収集レポート"]

    # スタイル定義
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(name="Meiryo UI", size=11, bold=True, color="FFFFFF")
    pickup_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    body_font = Font(name="Meiryo UI", size=10)
    thin_side = Side(style="thin", color="BFBFBF")
    cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # 1行目（ヘッダー）の装飾
    ws.row_dimensions[1].height = 28
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = cell_border

    # データ行の装飾
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        is_pickup = (row[0].value == "★注目")
        for cell in row:
            cell.font = body_font
            cell.border = cell_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if is_pickup:
                cell.fill = pickup_fill

    # 列幅の調整（見やすい固定幅＋本文は広めに設定）
    col_widths = {"A": 10, "B": 22, "C": 10, "D": 28, "E": 65}
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # ウィンドウ枠の固定（1行目スクロール固定）とオートフィルタ設定
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    wb.save(output_path)
    logger.info(f"装飾済みExcelレポートを保存しました: {output_path}")
