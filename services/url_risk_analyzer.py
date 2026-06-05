# services/url_risk_analyzer.py

from urllib.parse import urlparse


SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "account",
    "bank",
    "secure",
    "update",
    "password"
]

SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".click",
    ".work",
    ".loan"
]


def analyze_url(url):

    reasons = []

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    for word in SUSPICIOUS_WORDS:

        if word in domain:

            reasons.append(
                f"Suspicious keyword: {word}"
            )

    for tld in SUSPICIOUS_TLDS:

        if domain.endswith(tld):

            reasons.append(
                f"Suspicious TLD: {tld}"
            )

    risk = "LOW"

    if len(reasons) >= 3:
        risk = "HIGH"

    elif len(reasons) > 0:
        risk = "MEDIUM"

    return {
        "url": url,
        "risk": risk,
        "reasons": reasons
    }