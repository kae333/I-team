from flask import Flask, render_template, g
import sqlite3
import os
from pathlib import Path

from excel_loader import load_products
from solver import find_combinations

app = Flask(__name__)

# =========================
# パス設定（ここが変更点）
# =========================
BASE_DIR = Path(__file__).resolve().parent

EXCEL_PATH = BASE_DIR / "店頭商品食品ピックアップ.xlsx"  # ←ここ重要

DB_PATH = Path("/tmp/counter.db")


# =========================
# Excelキャッシュ
# =========================
try:
    PRODUCTS, CATEGORIES = load_products(EXCEL_PATH)
except Exception as e:
    print("Excel load error:", e)
    PRODUCTS, CATEGORIES = [], []


# =========================
# DB
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
# カウンター（高速）
# =========================
def increase_counter():
    db = get_db()
    cur = db.cursor()

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
@app.route("/", methods=["GET", "POST"])
def index():
    count = increase_counter()

    result = []

    safe_products = PRODUCTS[:50]  # Render対策

    try:
        if PRODUCTS:
            result = find_combinations(
                safe_products,
                target=1000,
                required_categories=set(),
            )
    except Exception as e:
        print("solver error:", e)
        result = []

    return render_template(
        "index.html",
        count=count,
        result=result
    )


@app.route("/count")
def count():
    return {"count": get_counter()}


# =========================
# 起動
# =========================
if __name__ == "__main__":
    init_db()

    app.run(
        debug=True,
        threaded=True,
        use_reloader=False
    )