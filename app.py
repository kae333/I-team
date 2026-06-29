from pathlib import Path
import random
from flask import Flask, flash, render_template, request

from excel_loader import load_products
from solver import find_combinations


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "店頭商品食品ピックアップ.xlsx"

_products = []
_categories = []
_load_error = None


def load_catalog():
    global _products, _categories, _load_error

    if not EXCEL_PATH.exists():
        _load_error = "Excelが見つかりません"
        _products, _categories = [], []
        return

    try:
        _products, _categories = load_products(EXCEL_PATH)
        _load_error = None
    except Exception as e:
        _load_error = str(e)
        _products, _categories = [], []


load_catalog()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    target = None
    selected = []

    if request.method == "POST":

        if _load_error:
            flash(_load_error, "error")
        else:
            try:
                target = int(request.form.get("target", ""))
            except:
                flash("数字を入力してね", "error")
                return render_template("index.html")

            selected = request.form.getlist("categories")

            result = find_combinations(
                _products,
                target,
                set(selected),
            )

            if result:
                flash("見つかりました！", "info")

    return render_template(
        "index.html",
        categories=_categories,
        result=result,
        target=target,
        selected=selected,
        product_count=len(_products),
        error=_load_error,
    )


if __name__ == "__main__":
    app.run(debug=True)