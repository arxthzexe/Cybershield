import joblib
import pandas as pd
from url_scanner.url_features import extract_url_features
from url_scanner.url_rules import rule_score

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "url_phishing_model.pkl")

def analyze_url(url):
    features = extract_url_features(url)
    rule = rule_score(features)

    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame([features])
    ml_prob = model.predict_proba(X)[0][1] * 100

    hybrid_score = 0.6 * rule + 0.4 * ml_prob

    if hybrid_score > 70:
        verdict = "PHISHING"
    elif hybrid_score > 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return {
        "url": url,
        "rule_score": rule,
        "ml_score": round(ml_prob, 2),
        "hybrid_score": round(hybrid_score, 2),
        "verdict": verdict
    }
