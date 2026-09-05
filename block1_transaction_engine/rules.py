# rules.py
import pandas as pd

class RuleEngine:

    def __init__(self, df):
        self.df = df.copy()
        if 'nameOrig' in self.df.columns and 'sender_account' not in self.df.columns:
            self.df = self.df.rename(columns={
                'nameOrig': 'sender_account',
                'nameDest': 'receiver_account'
            })
        if 'step' in self.df.columns and 'timestamp' not in self.df.columns:
            start_date = pd.to_datetime('2025-01-01')
            self.df['timestamp'] = start_date + pd.to_timedelta(self.df['step'], unit='h')
        if 'device_id' not in self.df.columns:
            self.df['device_id'] = 'D1'
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        else:
            self.df['timestamp'] = pd.Timestamp.now()

    def sudden_spike(self, account):
        """Rule-1: Detect sudden spike in transactions"""
        tx_count = len(self.df[self.df['sender_account'] == account])
        return 30 if tx_count > 5 else 0

    def quick_in_out(self, account):
        """Rule-2: Deposit → withdraw shortly"""
        tx = self.df[self.df['sender_account'] == account]
        tx = tx.sort_values('timestamp')
        score = 0

        # use total_seconds() to correctly handle multi-day diffs
        for i in range(len(tx) - 1):
            t1 = tx.iloc[i]['timestamp']
            t2 = tx.iloc[i + 1]['timestamp']
            time_diff_seconds = (t2 - t1).total_seconds()

            if time_diff_seconds < 1800:  # 30 min
                score += 10

        return min(score, 25)

    def many_recipients(self, account):
        """Rule-3: Many unique receivers"""
        receivers = self.df[self.df['sender_account'] == account]['receiver_account']
        return 20 if receivers.nunique() > 3 else 0

    def multiple_devices(self, account):
        """Rule-4: Device switching"""
        devices = self.df[self.df['sender_account'] == account]['device_id']
        return 15 if devices.nunique() > 1 else 0

    def score_account(self, account):
        total = 0
        total += self.sudden_spike(account)
        total += self.quick_in_out(account)
        total += self.many_recipients(account)
        total += self.multiple_devices(account)

        return total