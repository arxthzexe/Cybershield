import pandas as pd
import numpy as np

def extract_features(df):
    """Aggregate transaction-level dataframe into one row per sender_account with useful features.

    Returns DataFrame with an 'account' column followed by numeric features suitable for ML models.
    """
    df = df.copy()
    
    # Auto-adapt PaySim dataset format if detected
    if 'nameOrig' in df.columns and 'sender_account' not in df.columns:
        df = df.rename(columns={
            'nameOrig': 'sender_account',
            'nameDest': 'receiver_account'
        })
        if 'step' in df.columns and 'timestamp' not in df.columns:
            start_date = pd.to_datetime('2025-01-01')
            df['timestamp'] = start_date + pd.to_timedelta(df['step'], unit='h')
        if 'transaction_id' not in df.columns:
            df['transaction_id'] = df.index
        if 'device_id' not in df.columns:
            df['device_id'] = 'D1' # Dummy device for PaySim
            
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    
    # Feature: is_night_tx (e.g., between 12 AM and 5 AM)
    df['is_night_tx'] = df['hour'].apply(lambda x: 1 if 0 <= x <= 5 else 0)

    # Basic aggregations that pandas can optimize
    agg = df.groupby('sender_account').agg(
        tx_count=('transaction_id', 'count'),
        total_amount=('amount', 'sum'),
        mean_amount=('amount', 'mean'),
        std_amount=('amount', lambda x: x.astype(float).std(ddof=0)),
        unique_receivers=('receiver_account', pd.Series.nunique),
        unique_devices=('device_id', pd.Series.nunique),
        night_tx_count=('is_night_tx', 'sum'),
        first_ts=('timestamp', 'min'),
        last_ts=('timestamp', 'max')
    ).reset_index()

    # Compute median inter-transaction seconds per account
    def median_inter_tx_seconds(group):
        times = group.sort_values('timestamp')['timestamp'].values
        if len(times) > 1:
            diffs = np.diff(times).astype('timedelta64[s]').astype(float)
            return float(np.median(diffs))
        return 0.0

    try:
        medians = df.groupby('sender_account').apply(median_inter_tx_seconds, include_groups=False).rename('median_inter_tx_seconds').reset_index()
    except TypeError:
        # Fallback for older pandas versions
        medians = df.groupby('sender_account').apply(median_inter_tx_seconds).rename('median_inter_tx_seconds').reset_index()

    # Merge and finalize
    grouped = agg.merge(medians, on='sender_account', how='left')
    
    # Temporal & Behavioral Features
    grouped['hours_active_span'] = ((grouped['last_ts'] - grouped['first_ts']).dt.total_seconds() / 3600.0).fillna(0.0)
    grouped['tx_count'] = grouped['tx_count'].fillna(0).astype(int)
    grouped['tx_per_hour'] = grouped.apply(
        lambda r: (r['tx_count'] / r['hours_active_span']) if r['hours_active_span'] > 0 else float(r['tx_count']),
        axis=1
    )
    
    grouped['proportion_night_tx'] = grouped['night_tx_count'] / grouped['tx_count'].replace(0, 1)
    
    # Velocity Score: combination of tx frequency and mean amount
    grouped['velocity_score'] = grouped['tx_per_hour'] * np.log1p(grouped['mean_amount'])

    # cleanup columns and rename
    grouped = grouped.rename(columns={'sender_account': 'account'})
    grouped = grouped.drop(columns=['first_ts', 'last_ts', 'night_tx_count'])
    grouped['account'] = grouped['account'].astype(str)
    
    # fill NaNs that may remain
    grouped = grouped.fillna(0.0)
    
    return grouped