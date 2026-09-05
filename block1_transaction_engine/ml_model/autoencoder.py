import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

class TransactionAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(TransactionAutoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8) # Latent space
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def train_autoencoder(X_train, epochs=50, batch_size=32, learning_rate=1e-3, device='cpu'):
    """Trains the autoencoder and returns the model and fitted scaler."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)
    
    input_dim = X_scaled.shape[1]
    model = TransactionAutoencoder(input_dim).to(device)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    tensor_X = torch.FloatTensor(X_scaled).to(device)
    dataset = torch.utils.data.TensorDataset(tensor_X, tensor_X)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model.train()
    for epoch in range(epochs):
        for batch_x, _ in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_x)
            loss.backward()
            optimizer.step()
            
    return model, scaler

def predict_anomaly_scores(model, scaler, X, device='cpu'):
    """Returns the MSE reconstruction error per row."""
    model.eval()
    X_scaled = scaler.transform(X)
    tensor_X = torch.FloatTensor(X_scaled).to(device)
    
    with torch.no_grad():
        reconstructed = model(tensor_X)
        # Calculate MSE per sample (row-wise)
        mse = torch.mean((tensor_X - reconstructed) ** 2, dim=1).cpu().numpy()
        
    return mse

def get_feature_contributions(model, scaler, X, feature_names, device='cpu'):
    """
    Returns a list of strings explaining the top anomalous features per row.
    Useful for law enforcement dashboards.
    """
    model.eval()
    X_scaled = scaler.transform(X)
    tensor_X = torch.FloatTensor(X_scaled).to(device)
    
    with torch.no_grad():
        reconstructed = model(tensor_X)
        # Squared error per feature per sample
        sq_errors = ((tensor_X - reconstructed) ** 2).cpu().numpy()
    
    explanations = []
    for i in range(len(sq_errors)):
        # Get top 2 features with highest reconstruction error
        row_errors = sq_errors[i]
        top_indices = np.argsort(row_errors)[-2:][::-1] # Sort ascending, take last 2, reverse
        
        top_features = [feature_names[idx] for idx in top_indices]
        explanation = f"High anomaly in: {', '.join(top_features)}"
        explanations.append(explanation)
        
    return explanations
