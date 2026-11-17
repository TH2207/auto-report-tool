import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_and_process(raw_data: list[dict]) -> pd.DataFrame:
    """データのバリデーションと加工・集計を行う"""
    if not raw_data:
        logger.warning("処理対象のデータが空です。")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # 1. バリデーション（必須項目の欠損チェック）
    initial_count = len(df)
    df = df[df["quote"].str.len() > 0]
    df = df[df["author"].str.len() > 0]
    dropped_count = initial_count - len(df)
    if dropped_count > 0:
        logger.warning(f"不正または欠損データ {dropped_count} 件を除外しました。")

    # 2. 重複データの排除
    df = df.drop_duplicates(subset=["quote"]).copy()

    # 3. データ加工（文字数カウントと注目フラグの付与）
    df["char_count"] = df["quote"].str.len()
    # 例：100文字未満のコンパクトな名言を「注目（★）」とする
    df["pickup"] = df["char_count"].apply(lambda x: "★注目" if x < 100 else "")

    # カラム名を日本語のレポート用に変更
    df = df.rename(columns={
        "pickup": "判定",
        "author": "著者",
        "char_count": "文字数",
        "tags": "関連タグ",
        "quote": "名言本文"
    })

    # 列の並び順を整理
    df = df[["判定", "著者", "文字数", "関連タグ", "名言本文"]]
    logger.info(f"検証完了：有効データ {len(df)} 件を出力用に整形しました。")
    return df
