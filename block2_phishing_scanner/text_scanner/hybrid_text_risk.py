import pandas as pd
import joblib
from text_scanner.message_model import extract_text_features
from text_scanner.nlp_rules import rule_score

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "sms_scam_model.pkl")

def analyze_text(text):
    features = extract_text_features(text)
    rule = rule_score(features)

    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame([features])
    ml_prob = model.predict_proba(X)[0][1] * 100

    hybrid_score = 0.7 * rule + 0.3 * ml_prob

    if hybrid_score > 70:
        verdict = "SCAM"
    elif hybrid_score > 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return {
        "message": text,
        "rule_score": rule,
        "ml_probability": round(ml_prob, 2),
        "hybrid_score": round(hybrid_score, 2),
        "verdict": verdict
    }
