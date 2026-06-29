from flask import Flask, render_template, g
import sqlite3
import os
from pathlib import Path

from excel_lorder import load_products
from solver import find_combinations

app = Flask(__name__)

# =========================
# パス
# =========================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "counter.db"
EXCEL_PATH = BASE_DIR / "data.xlsx"


# =========================
# 🔥 Excelキャッシュ（最重要）
# =========================
PRODUCTS, CATEGORIES = load_products(EXCEL_PATH)


# =========================
# DB（軽量維持）
# =========================
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL
        )
    """)

    cur.execute("SELECT count(*) FROM counter")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO counter (id, count) VALUES (1, 0)")

    db.commit()
    db.close()


# =========================
# カウンター（最適化版）
# =========================
def increase_counter():
    db = get_db()
    cur = db.cursor()

    # SQLでインクリメント（高速）
    cur.execute("""
        UPDATE counter
        SET count = count + 1
        WHERE id = 1
    """)

    db.commit()

    cur.execute("SELECT count FROM counter WHERE id = 1")
    return cur.fetchone()[0]


def get_counter():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT count FROM counter WHERE id = 1")
    return cur.fetchone()[0]


# =========================
# ルート
# =========================
@app.route("/")
def index():
    count = increase_counter()

    # solver呼び出し（必要ならここで使う）
    # result = find_combinations(PRODUCTS, target=1000, required_categories={"A"})

    return render_template("index.html", count=count)


@app.route("/count")
def count():
    return {"count": get_counter()}


# =========================
# 起動
# =========================
if __name__ == "__main__":
    init_db()

    # 🚀 軽量起動設定
    app.run(
        debug=True,
        threaded=True,
        use_reloader=False
    )