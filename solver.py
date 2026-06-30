from itertools import combinations
import random

# 最大商品数（3がおすすめ）
MAX_ITEMS = 3


def find_combinations(products, target, required_categories):
    """
    target: 予算
    required_categories: チェックされたカテゴリ(set)
    """

    # 予算より高い商品は最初から除外
    candidates = [p for p in products if p.price <= target]

    # ランダムに並び替える
    random.shuffle(candidates)

    # 1～3商品で探索
    for r in range(1, MAX_ITEMS + 1):

        for combo in combinations(candidates, r):

            # 合計金額
            total = sum(item.price for item in combo)

            # ぴったりだけ
            if total != target:
                continue

            # 同じ商品名は禁止
            names = [item.name for item in combo]

            if len(names) != len(set(names)):
                continue

            # 必須カテゴリ
            combo_categories = {item.category for item in combo}

            if not required_categories.issubset(combo_categories):
                continue

            # 見つかったら即返す（高速！）
            return list(combo)

    # 見つからない
    return []