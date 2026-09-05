import os
import io
import joblib
import torch
import pandas as pd
from ml_model.feature_engineering import extract_features
from ml_model.autoencoder import train_autoencoder

def train_and_save_model(transactions_csv, out_model_path='ae_model.pth', out_scaler_path='ae_scaler.pkl', random_state=42):
    torch.manual_seed(random_state)
    
    df = pd.read_csv(transactions_csv)
    
    # If the dataset is massive (like PaySim's 6 million rows), take a representative sample
    # to keep training time reasonable on a CPU.
    if len(df) > 100000:
        print(f"Large dataset detected ({len(df)} rows). Sampling 100,000 rows for efficient training...")
        df = df.sample(n=100000, random_state=random_state)
        
    features = extract_features(df)
    X = features.drop(columns=['account']).values
    
    # Adjust hyperparameters based on size
    epochs = 15 if len(X) > 5000 else 100
    batch_size = 256 if len(X) > 5000 else 16
    
    # Train Autoencoder
    print(f"Training PyTorch Autoencoder (Accounts={len(X)}, Epochs={epochs}, BatchSize={batch_size})...")
    model, scaler = train_autoencoder(X, epochs=epochs, batch_size=batch_size)
    
    # Save the PyTorch model state_dict and scaler
    import tempfile
    import shutil
    temp_dir = tempfile.gettempdir()
    temp_m = os.path.join(temp_dir, 'ae_weights.pth')
    temp_s = os.path.join(temp_dir, 'ae_transformers.pkl')
    
    torch.save(model.state_dict(), temp_m)
    joblib.dump(scaler, temp_s)
    
    shutil.copy2(temp_m, out_model_path)
    shutil.copy2(temp_s, out_scaler_path)
    
    print(f"Saved model to {out_model_path}")
    print(f"Saved scaler to {out_scaler_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Default to sample, but if paysim dataset.csv exists, use it!
    csv_path = os.path.join(BASE_DIR, 'sample_transactions.csv')
    paysim_path = os.path.join(BASE_DIR, 'paysim dataset.csv')
    if os.path.exists(paysim_path):
        csv_path = paysim_path
        print("Found PaySim dataset! Using it for training...")
    elif not os.path.exists(csv_path):
        raise FileNotFoundError(f"No datasets found!")
        
    model_path = os.path.join(BASE_DIR, 'ae_model_v2.pth')
    scaler_path = os.path.join(BASE_DIR, 'ae_scaler_v2.pkl')
    
    train_and_save_model(csv_path, model_path, scaler_path)