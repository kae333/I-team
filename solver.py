from itertools import combinations
import random


def find_combinations(products, target, required_categories):

    candidates = []

    # 商品は1～3個まで組み合わせ
    for r in range(1, 4):

        for combo in combinations(products, r):

            # 同じ商品名は禁止
            names = [p.name for p in combo]
            if len(names) != len(set(names)):
                continue

            # 合計金額
            total = sum(p.price for p in combo)

            # ぴったり一致だけ
            if total != target:
                continue

            # 必須カテゴリ
            cats = {p.category for p in combo}

            if not required_categories.issubset(cats):
                continue

            candidates.append(combo)

    # 見つからない
    if not candidates:
        return []

    # ランダムで1つだけ返す
    return random.choice(candidates)