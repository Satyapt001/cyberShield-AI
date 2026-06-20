def calculate_risk_score(
    spam_result,
    phishing_result,
    keyword_count,
    url_count
):
    """
    Intelligently calculates a uniform risk score from 0 to 100.
    Safely handles high-confidence 'Safe' classifications.
    """
    base_score = 0
    
    # 1. Extract confidence values
    spam_conf = spam_result.get("confidence", 0)
    phishing_conf = phishing_result.get("confidence", 0)
    
    # 2. Only factor in ML confidence if the prediction points to an active threat
    if spam_result.get("prediction") == "Spam":
        base_score = max(base_score, spam_conf)
        
    if phishing_result.get("prediction") == "Phishing":
        # Give phishing a slightly higher base weight if matched
        base_score = max(base_score, phishing_conf)
        
    # 3. Apply multipliers for environmental risk indicators
    keyword_weight = keyword_count * 4   # High-contrast keyword impact
    url_weight = url_count * 12         # High-contrast URL danger impact
    
    # 4. Consolidate absolute risk metrics
    total_score = base_score + keyword_weight + url_weight
    
    # 5. Cap at 100 max and round cleanly
    return round(min(total_score, 100))