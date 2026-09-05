import pandas as pd
from datetime import datetime
from hybrid_risk import calculate_hybrid_risk

def evaluate_accounts(df):
    return calculate_hybrid_risk(df)

if __name__ == "__main__":
    df = pd.read_csv("sample_transactions.csv")
    result = evaluate_accounts(df)
    print(result)
