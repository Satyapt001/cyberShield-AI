def generate_explanation(

    spam_result,
    phishing_result,
    keywords,
    urls,
    risk_score

):

    reasons = []

    if spam_result["prediction"] == "Spam":

        reasons.append(
            f"Spam confidence is {spam_result['confidence']}%"
        )

    if phishing_result["prediction"] == "Phishing":

        reasons.append(
            f"Phishing confidence is {phishing_result['confidence']}%"
        )

    if keywords:

        reasons.append(
            "Suspicious keywords detected: "
            + ", ".join(keywords)
        )

    if urls:

        reasons.append(
            f"{len(urls)} URL(s) detected"
        )

    if risk_score >= 80:

        reasons.append(
            "Overall threat score is very high"
        )

    return reasons