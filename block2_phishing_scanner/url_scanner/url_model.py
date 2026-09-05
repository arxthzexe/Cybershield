import os
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib

def train_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, "sample_urls.csv")
    df = pd.read_csv(csv_path)

    X = df.drop(columns=["url", "label"])
    y = df["label"]

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X, y)
    out_model_path = os.path.join(BASE_DIR, "url_phishing_model.pkl")
    joblib.dump(model, out_model_path)
    print(f"Improved phishing model trained and saved to {out_model_path}")

if __name__ == "__main__":
    train_model()

