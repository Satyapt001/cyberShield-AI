from flask import Flask, render_template, request, jsonify

from services.spam_detector import predict_spam
from services.phishing_detector import predict_phishing

from services.keyword_analyzer import detect_keywords
from services.url_analyzer import extract_urls
from services.url_risk_analyzer import analyze_url

from services.risk_scorer import calculate_risk_score

from services.dashboard_service import (
    get_dashboard_stats,
    save_scan,
    get_model_metrics,
    get_best_model
)

from services.explainability import (
    generate_explanation
)

app = Flask(__name__)


# ==========================================
# Pages
# ==========================================

@app.route("/")
def home():

    return render_template(
        "scan.html"
    )


@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    metrics = get_model_metrics()

    best_model = get_best_model()

    return render_template(

        "dashboard.html",

        stats=stats,

        metrics=metrics,

        best_model=best_model
    )


# ==========================================
# Dashboard API
# ==========================================

@app.route("/dashboard-data")
def dashboard_data():

    stats = get_dashboard_stats()

    metrics = get_model_metrics()

    best_model = get_best_model()

    return jsonify({

        "stats": stats,

        "metrics": metrics,

        "best_model": best_model

    })


# ==========================================
# Health Check
# ==========================================

@app.route("/healthz")
def health_check():

    return jsonify({
        "status": "healthy"
    }), 200


# ==========================================
# Threat Analysis API
# ==========================================

@app.route("/scan", methods=["POST"])
def scan():

    try:

        data = request.get_json()

        text = data.get(
            "message",
            ""
        ).strip()

        if not text:

            return jsonify({

                "error":
                    "Message cannot be empty"

            }), 400

        # ==================================
        # Spam Detection
        # ==================================

        spam_result = predict_spam(
            text
        )

        # ==================================
        # Phishing Detection
        # ==================================

        phishing_result = predict_phishing(
            text
        )

        # ==================================
        # Keyword Analysis
        # ==================================

        keywords = detect_keywords(
            text
        )

        # ==================================
        # URL Extraction
        # ==================================

        urls = extract_urls(
            text
        )

        # ==================================
        # URL Risk Analysis
        # ==================================

        url_analysis = [

            analyze_url(url)

            for url in urls

        ]

        # ==================================
        # Risk Score
        # ==================================

        highest_confidence = max(

            spam_result["confidence"],

            phishing_result["confidence"]

        )

        risk_score = calculate_risk_score(
            spam_result,
            phishing_result,
            len(keywords),
            len(urls)
        )

        # ==================================
        # Threat Level
        # ==================================

        if risk_score >= 80:

            threat_level = "HIGH"

        elif risk_score >= 50:

            threat_level = "MEDIUM"

        else:

            threat_level = "LOW"

        # ==================================
        # Explainable AI
        # ==================================

        explanation = generate_explanation(

            spam_result,

            phishing_result,

            keywords,

            urls,

            risk_score

        )

        # ==================================
        # Save Scan History
        # ==================================

        save_scan({

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

            "url_count":
                len(urls)
        })

        # ==================================
        # API Response
        # ==================================

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
                url_analysis,

            "explanation":
                explanation

        })

    except Exception as e:

        return jsonify({

            "error":
                str(e)

        }), 500


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )