import os
import re
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# ---------- FEATURE EXTRACTION ----------
def extract_text_features(text):
    text = text.lower()
    tokens = text.split()

    scam_keywords = [
        "otp", "verify", "urgent", "blocked", "suspend",
        "click", "link", "upi", "refund", "reward", "prize"
    ]

    return {
        "text_length": len(text),
        "word_count": len(tokens),
        "digit_count": sum(char.isdigit() for char in text),

        "has_url": int("http" in text or "www" in text),
        "has_otp_word": int("otp" in text),
        "keyword_count": sum(1 for w in scam_keywords if w in text),
        "urgent_words": int(any(w in text for w in ["urgent", "now", "immediately"])),
        "has_bank_word": int(any(w in text for w in ["bank", "upi", "account"]))
    }

# ---------- MODEL TRAINING ----------
def train_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, "sample_sms.csv")
    df = pd.read_csv(csv_path)

    X = df.drop(columns=["text", "label"])
    y = df["label"]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X, y)
    out_model_path = os.path.join(BASE_DIR, "sms_scam_model.pkl")
    joblib.dump(model, out_model_path)
    print(f"SMS scam model trained successfully and saved to {out_model_path}")

if __name__ == "__main__":
    train_model()

