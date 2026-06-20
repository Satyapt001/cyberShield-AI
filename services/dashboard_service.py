import json
import os
from datetime import datetime

SCAN_LOG_FILE = "data/scan_logs.json"
MODEL_METRICS_FILE = "data/model_metrics.json"

# ==========================================================================
# Scan Logs Data Operations
# ==========================================================================

def load_scan_logs():
    if not os.path.exists(SCAN_LOG_FILE):
        return []
    try:
        with open(SCAN_LOG_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return []

def save_scan(scan_data):
    scans = load_scan_logs()
    
    # Inject formatted operational timestamp
    scan_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scans.append(scan_data)
    
    with open(SCAN_LOG_FILE, "w") as file:
        json.dump(scans, file, indent=4)

# ==========================================================================
# Real-Time Dashboard Statistics Engine
# ==========================================================================

def get_dashboard_stats():
    scans = load_scan_logs()
    total_scans = len(scans)

    spam_detected = sum(1 for scan in scans if scan.get("spam_prediction") == "Spam")
    phishing_detected = sum(1 for scan in scans if scan.get("phishing_prediction") == "Phishing")
    
    high_threats = sum(1 for scan in scans if scan.get("threat_level") == "HIGH")
    medium_threats = sum(1 for scan in scans if scan.get("threat_level") == "MEDIUM")
    low_threats = sum(1 for scan in scans if scan.get("threat_level") == "LOW")
    
    safe_emails = sum(
        1 for scan in scans 
        if scan.get("spam_prediction") == "Safe" and scan.get("phishing_prediction") == "Safe"
    )

    return {
        "total_scans": total_scans,
        "spam_detected": spam_detected,
        "phishing_detected": phishing_detected,
        "safe_emails": safe_emails,
        "high_threats": high_threats,
        "medium_threats": medium_threats,
        "low_threats": low_threats,
        # Safely tracks up to 50 logs for front-end reversing inside the scroll container
        "recent_scans": scans[-50:] 
    }

# ==========================================================================
# Model Metrics Extraction
# ==========================================================================

def get_model_metrics():
    if not os.path.exists(MODEL_METRICS_FILE):
        return []
    try:
        with open(MODEL_METRICS_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return []

# ==========================================================================
# Locked Selection Profile (Configured for Logistic Regression)
# ==========================================================================

def get_best_model():
    metrics = get_model_metrics()
    if not metrics:
        return None

    # Pull metrics explicitly calculated for the active Logistic Regression pipeline
    lr_metrics = next((m for m in metrics if m["Model"] == "Logistic Regression"), None)
    
    # Fallback to absolute top accuracy value if target file is empty/missing
    if not lr_metrics:
        best_model = max(metrics, key=lambda model: model["Accuracy"])
        return {
            "name": best_model["Model"],
            "accuracy": best_model["Accuracy"],
            "precision": best_model["Precision"],
            "recall": best_model["Recall"],
            "f1": best_model["F1 Score"],
            "reason": [
                "Stable Classification Probabilities on Variable Datasets",
                "Highly Linear Convergence via Softmax Vector Regularization",
                "Fast Prediction Execution Over Complex NLP Feature Extraction Arrays"
            ]
        }

    return {
        "name": "Logistic Regression",
        "accuracy": lr_metrics["Accuracy"],
        "precision": lr_metrics["Precision"],
        "recall": lr_metrics["Recall"],
        "f1": lr_metrics["F1 Score"],
        "reason": [
            "Stable Classification Probabilities on Variable Datasets",
            "Highly Linear Convergence via Softmax Vector Regularization",
            "Fast Prediction Execution Over Complex NLP Feature Extraction Arrays"
        ]
    }