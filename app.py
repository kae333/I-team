from pathlib import Path
import sqlite3

from flask import Flask, flash, render_template, request

from excel_loader import load_products
from solver import find_combinations


# =========================
# Flask
# =========================

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"


# =========================
# Path
# =========================

BASE_DIR = Path(__file__).resolve().parent

EXCEL_PATH = BASE_DIR / "店頭商品食品ピックアップ2607.xlsx"

DB_PATH = BASE_DIR / "counter.db"


# =========================
# Product Data
# =========================

_products = []
_categories = []
_load_error = None


# =========================
# Counter
# =========================

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS counter(
            id INTEGER PRIMARY KEY,
            visits INTEGER NOT NULL
        )
    """)

    cur.execute("""
        INSERT OR IGNORE INTO counter(id,visits)
        VALUES(1,0)
    """)

    conn.commit()

    conn.close()


def increase_counter():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""

        UPDATE counter

        SET visits = visits + 1

        WHERE id=1

    """)

    conn.commit()

    conn.close()


def get_counter():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("""

        SELECT visits

        FROM counter

        WHERE id=1

    """)

    count = cur.fetchone()[0]

    conn.close()

    return count


# =========================
# Excel
# =========================

def load_catalog():

    global _products
    global _categories
    global _load_error

    if not EXCEL_PATH.exists():

        _load_error = "Excelが見つかりません"

        return

    try:

        _products, _categories = load_products(EXCEL_PATH)

        _load_error = None

    except Exception as e:

        _load_error = str(e)

        _products = []

        _categories = []


# 初期化
init_db()
load_catalog()

print("商品数:", len(_products))
print("カテゴリ:", _categories)
print("エラー:", _load_error)


# =========================
# Route
# =========================

@app.route("/", methods=["GET", "POST"])

def index():

    increase_counter()

    visit_count = get_counter()

    result = None

    target = None

    selected = []

    if request.method == "POST":

        if _load_error:

            flash(_load_error, "error")

        else:

            try:

                target = int(request.form.get("target"))

            except:

                flash("予算を入力してください", "error")

                return render_template(
                    "index.html",
                    categories=_categories,
                    visits=visit_count
                )

            selected = request.form.getlist("categories")

            result = find_combinations(

                _products,

                target,

                set(selected)

            )

            if not result:

                flash("その組み合わせは見つかりませんでした。", "info")

    return render_template(

        "index.html",

        categories=_categories,

        result=result,

        target=target,

        selected=selected,

        visits=visit_count,

        product_count=len(_products),

        error=_load_error,

    )


# =========================
# Main
# =========================

if __name__ == "__main__":

    app.run(debug=True)