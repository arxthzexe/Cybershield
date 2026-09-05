import os
import io
import logging
import numpy as np
import pandas as pd
import torch
import joblib
from rules import RuleEngine
from ml_model.feature_engineering import extract_features
from ml_model.autoencoder import TransactionAutoencoder, train_autoencoder, predict_anomaly_scores, get_feature_contributions
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import rankdata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scale_to_0_100(values):
    arr = np.asarray(values).astype(float).ravel()
    finite_mask = np.isfinite(arr)
    safe_arr = arr.copy()
    safe_arr[~finite_mask] = 0.0
    if safe_arr.size == 0:
        return np.array([])
    safe_arr = safe_arr.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 100))
    try:
        scaled = scaler.fit_transform(safe_arr).flatten()
    except Exception:
        scaled = np.zeros_like(arr)
    scaled[~finite_mask] = 0.0
    return scaled

def load_or_train_model(model_path, scaler_path, feature_X, feature_df=None, sample_csv=None):
    need_train = False
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        need_train = True
    elif os.path.getsize(model_path) == 0 or os.path.getsize(scaler_path) == 0:
        logger.warning("Model or scaler file is empty; it will be overwritten.")
        need_train = True

    input_dim = feature_X.shape[1] if feature_X is not None else (feature_df.shape[1] - 1 if feature_df is not None else 10)
    
    if need_train:
        logger.info("Training new Autoencoder model...")
        if feature_X is not None and len(feature_X) > 0:
            model, scaler = train_autoencoder(feature_X, epochs=50)
            input_dim = feature_X.shape[1]
        elif sample_csv is not None and os.path.exists(sample_csv):
            df = pd.read_csv(sample_csv)
            if len(df) > 100000:
                logger.info(f"Large dataset detected ({len(df)} rows). Sampling 100,000 rows for efficient fallback training...")
                df = df.sample(n=100000, random_state=42)
            features = extract_features(df)
            X = features.drop(columns=['account']).values
            epochs = 15 if len(X) > 5000 else 50
            batch_size = 256 if len(X) > 5000 else 32
            model, scaler = train_autoencoder(X, epochs=epochs, batch_size=batch_size)
            input_dim = X.shape[1]
        else:
            raise FileNotFoundError("No valid model and insufficient data to train a fallback model.")
        
        import tempfile
        import shutil
        temp_dir = tempfile.gettempdir()
        temp_m = os.path.join(temp_dir, 'ae_model_v2.pth')
        temp_s = os.path.join(temp_dir, 'ae_scaler_v2.pkl')
        
        torch.save(model.state_dict(), temp_m)
        joblib.dump(scaler, temp_s)
        
        try:
            shutil.copy2(temp_m, model_path)
            shutil.copy2(temp_s, scaler_path)
        except Exception as e:
            logger.warning(f"Could not copy to final path: {e}")
    else:
        scaler = joblib.load(scaler_path)
        model = TransactionAutoencoder(input_dim)
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        
    return model, scaler

def calculate_hybrid_risk(df, model_path=None, scaler_path=None, ml_weight=0.4, rule_weight=0.6):
    if not np.isclose(ml_weight + rule_weight, 1.0):
        raise ValueError("ml_weight + rule_weight must equal 1.0")

    feature_df = extract_features(df)
    if 'account' not in feature_df.columns:
        raise KeyError("extract_features must return a DataFrame with an 'account' column")

    accounts = feature_df['account'].astype(str).values
    rule_engine = RuleEngine(df)
    rule_scores = [rule_engine.score_account(acc) for acc in accounts]

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if model_path is None:
        model_path = os.path.join(BASE_DIR, 'ae_model_v2.pth')
    if scaler_path is None:
        scaler_path = os.path.join(BASE_DIR, 'ae_scaler_v2.pkl')

    paysim_path = os.path.join(BASE_DIR, 'paysim dataset.csv')
    sample_csv = paysim_path if os.path.exists(paysim_path) else os.path.join(BASE_DIR, 'sample_transactions.csv')

    feature_cols = [c for c in feature_df.columns if c != 'account']
    X = feature_df[feature_cols].values

    # Load or train the Autoencoder
    model, scaler = load_or_train_model(model_path, scaler_path, feature_X=X, feature_df=feature_df, sample_csv=sample_csv)

    # Get ML anomaly scores and explanations
    ml_raw = predict_anomaly_scores(model, scaler, X)
    explanations = get_feature_contributions(model, scaler, X, feature_cols)

    if len(accounts) != len(ml_raw):
        raise ValueError(f"Length mismatch: {len(accounts)} accounts vs {len(ml_raw)} ML scores.")

    # Rank data to normalize the heavily skewed MSE scores into a smooth 0-100 curve
    ranks = rankdata(ml_raw, method='average') - 1
    ml_scaled = scale_to_0_100(ranks)
    hybrid_scores = (rule_weight * np.array(rule_scores)) + (ml_weight * ml_scaled)

    final_results = pd.DataFrame({
        'account': accounts,
        'rule_score': rule_scores,
        'ml_score': ml_scaled,
        'hybrid_score': hybrid_scores,
        'anomaly_reason': explanations
    })

    final_results['risk_level'] = final_results['hybrid_score'].apply(
        lambda x: 'HIGH' if x > 60 else ('MEDIUM' if x > 30 else 'LOW')
    )

    return final_results

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, 'sample_transactions.csv')
    paysim_path = os.path.join(BASE_DIR, 'paysim dataset.csv')
    
    if os.path.exists(paysim_path):
        print("Running hybrid risk on a sample of PaySim...")
        df = pd.read_csv(paysim_path).sample(10) # Just test on 10 rows
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"No datasets found!")

    results = calculate_hybrid_risk(df)
    print(results)