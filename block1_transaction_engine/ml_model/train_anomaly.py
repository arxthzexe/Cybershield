# train_anomaly.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from feature_engineering import extract_features

def train_model(df):
    feature_df = extract_features(df)

    X = feature_df.drop(columns=['account']).values

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    # anomaly scores (-1 anomaly, 1 normal)
    feature_df['anomaly_label'] = model.predict(X)
    feature_df['anomaly_score'] = model.decision_function(X)

    joblib.dump(model, "model.pkl")

    return feature_df

if __name__ == "__main__":
    df = pd.read_csv("sample_transactions.csv")
    result = train_model(df)
    print(result)
