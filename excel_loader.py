from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class Product:
    category: str
    name: str
    price: int


def load_products(path: Path):
    sheets = pd.read_excel(path, sheet_name=None)

    products = []

    for sheet_name, df in sheets.items():
        for _, row in df.iterrows():
            try:
                category = str(row.iloc[0]).strip()
                name = str(row.iloc[2]).strip()
                price = int(float(row.iloc[3]))

                products.append(Product(category, name, price))
            except:
                continue

    categories = sorted(set(p.category for p in products))
    return products, categories