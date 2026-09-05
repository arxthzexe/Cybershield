def rule_score(features):
    score = 0

    if features["has_ip"]:
        score += 30
    if not features["has_https"]:
        score += 20
    if features["has_at"]:
        score += 15
    if features["num_dots"] >= 4:
        score += 15
    if features["url_length"] > 60:
        score += 10
    if features["keyword_count"] >= 2:
        score += 25
    if not features["is_valid_url"]:
        score += 20

    return min(score, 100)
