def calculate_risk_score(

    confidence,

    keyword_count,

    url_count

):

    score = confidence

    score += keyword_count * 3

    score += url_count * 10

    score = min(score, 100)

    return round(score)