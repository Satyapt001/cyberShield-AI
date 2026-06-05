SUSPICIOUS_KEYWORDS = [

    "free",
    "winner",
    "urgent",
    "verify",
    "password",
    "account",

    "bank",

    "claim",

    "reward",

    "bonus",

    "limited",

    "click",

    "offer",

    "money",

    "login"
]


def detect_keywords(text):

    text = text.lower()

    found_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in text:

            found_keywords.append(
                keyword
            )

    return found_keywords