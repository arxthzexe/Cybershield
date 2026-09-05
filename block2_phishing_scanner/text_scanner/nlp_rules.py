def rule_score(f):
    score = 0

    if f["urgent_words"]:
        score += 30
    if f["keyword_count"] >= 2:
        score += 30
    if f["has_bank_word"]:
        score += 25
    if f["has_url"]:
        score += 20
    if f["digit_count"] >= 4:
        score += 15

    return min(score, 100)
