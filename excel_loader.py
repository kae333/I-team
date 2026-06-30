from dataclasses import dataclass
from pathlib import Path

import pandas as pd


# =========================
# Product
# =========================

@dataclass(frozen=True)
class Product:
    category: str
    name: str
    price: int


# =========================
# Excel Loader
# =========================

def load_products(path: Path):

    # すべてのシートを読み込む
    sheets = pd.read_excel(path, sheet_name=None)

    products = []

    added = set()

    for _, df in sheets.items():

        for _, row in df.iterrows():

            try:

                # A列
                category = str(row.iloc[0]).strip()

                # C列
                name = str(row.iloc[2]).strip()

                # D列
                price = int(row.iloc[3])

            except Exception:
                continue

            # 空白は無視
            if not category or category == "nan":
                continue

            if not name or name == "nan":
                continue

            if price <= 0:
                continue

            # 同じ商品の重複登録を防ぐ
            key = (name, price)

            if key in added:
                continue

            added.add(key)

            products.append(

                Product(

                    category=category,

                    name=name,

                    price=price,

                )

            )

    # カテゴリ一覧
    categories = sorted(

        {p.category for p in products}

    )

    return products, categories