import joblib

# Load once when application starts

spam_model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def predict_spam(text):

    transformed_text = vectorizer.transform([text])

    prediction = spam_model.predict(
        transformed_text
    )[0]

    confidence = max(
        spam_model.predict_proba(
            transformed_text
        )[0]
    ) * 100

    return {
    "prediction": "Spam" if prediction == 1 else "Safe",
    "confidence": float(round(confidence, 2))
}