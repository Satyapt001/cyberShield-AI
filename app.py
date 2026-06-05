from flask import Flask, render_template, request, jsonify

from services.spam_detector import predict_spam
from services.phishing_detector import predict_phishing

from services.keyword_analyzer import detect_keywords
from services.url_analyzer import extract_urls

from services.url_risk_analyzer import analyze_url
from services.risk_scorer import calculate_risk_score

app = Flask(__name__)


# =========================
# Pages
# =========================
@app.route("/healthz")
def health_check():
    return {
        "status": "healthy"
    }, 200
    
@app.route("/")
def home():
    return render_template("scan.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# Threat Analysis API
# =========================

@app.route("/scan", methods=["POST"])
def scan():

    try:

        data = request.get_json()

        text = data.get("message", "").strip()

        if not text:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400

        # Spam Detection

        spam_result = predict_spam(text)

        # Phishing Detection

        phishing_result = predict_phishing(text)

        # Keywords

        keywords = detect_keywords(text)

        # URLs

        urls = extract_urls(text)

        # URL Risk Analysis

        url_analysis = [
            analyze_url(url)
            for url in urls
        ]

        # Risk Score

        highest_confidence = max(
            spam_result["confidence"],
            phishing_result["confidence"]
        )

        risk_score = calculate_risk_score(
            highest_confidence,
            len(keywords),
            len(urls)
        )

        # Threat Level

        if risk_score >= 80:
            threat_level = "HIGH"

        elif risk_score >= 50:
            threat_level = "MEDIUM"

        else:
            threat_level = "LOW"

        return jsonify({

            "spam_prediction":
                spam_result["prediction"],

            "spam_confidence":
                spam_result["confidence"],

            "phishing_prediction":
                phishing_result["prediction"],

            "phishing_confidence":
                phishing_result["confidence"],

            "risk_score":
                risk_score,

            "threat_level":
                threat_level,

            "keywords":
                keywords,

            "urls":
                urls,

            "url_analysis":
                url_analysis

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
