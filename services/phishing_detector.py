import joblib

phishing_model = joblib.load(
    "models/phishing_model.pkl"
)

phishing_vectorizer = joblib.load(
    "models/phishing_vectorizer.pkl"
)


def predict_phishing(text):

    transformed_text = phishing_vectorizer.transform(
        [text]
    )

    prediction = phishing_model.predict(
        transformed_text
    )[0]

    confidence = max(
        phishing_model.predict_proba(
            transformed_text
        )[0]
    ) * 100

    return {
        "prediction":
            "Phishing" if prediction == 1 else "Safe",

        "confidence": float(round(confidence, 2))
    }