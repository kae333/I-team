import random
from itertools import combinations


def find_combinations(products, target, required_categories):
    """
    高速版 solver
    - 枝刈り強化
    - 無駄なリスト操作削減
    - 早期終了
    """

    if not products:
        return []

    candidates = []

    # ローカル変数化（少し高速化）
    target_price = target
    required = required_categories

    # 商品を価格順にソート（枝刈り効率UP）
    products = sorted(products, key=lambda p: p.price)

    n = len(products)

    # 1〜3個固定探索
    for r in (1, 2, 3):

        # rが商品の数より大きいならスキップ
        if r > n:
            continue

        for combo in combinations(products, r):

            total = 0
            names = set()
            cats = set()

            # ループ内で即判定（高速化の核心）
            for p in combo:
                total += p.price

                # 早期打ち切り（最重要）
                if total > target_price:
                    break

                names.add(p.name)
                cats.add(p.category)

            else:
                # 同名チェック
                if len(names) != r:
                    continue

                # 金額一致チェック
                if total != target_price:
                    continue

                # カテゴリ条件
                if not required.issubset(cats):
                    continue

                candidates.append(combo)

    if not candidates:
        return []

    return random.choice(candidates)