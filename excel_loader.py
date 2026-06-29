from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class Product:
    category: str
    name: str
    price: int


def load_products(path: Path):
    """
    Excelから商品を読み込む（高速版）
    - iterrows → itertuples に変更（高速化）
    - 無駄な変換処理を削減
    """

    # Excel全シート読み込み
    sheets = pd.read_excel(path, sheet_name=None)

    products = []

    for _, df in sheets.items():

        # NaN対策＋高速ループ
        df = df.fillna("")

        for row in df.itertuples(index=False):

            try:
                category = str(row[0]).strip()
                name = str(row[2]).strip()

                # 価格変換（安全＆軽量）
                price = int(float(row[3]))

                # 空データ除外（軽量化）
                if not category or not name:
                    continue

                products.append(Product(category, name, price))

            except:
                continue

    # カテゴリ一覧（setで高速化）
    categories = sorted({p.category for p in products})

    return products, categories