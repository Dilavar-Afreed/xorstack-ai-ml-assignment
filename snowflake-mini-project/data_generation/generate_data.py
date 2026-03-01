import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

NUM_ROWS = 100000
FRAUD_RATIO = 0.05  # 5% fraud

def generate_data():

    data = []

    for i in range(NUM_ROWS):

        transaction_id = i + 1
        user_id = np.random.randint(1, 5000)

        account_age_days = np.random.exponential(scale=365)
        transaction_amount = np.random.exponential(scale=100)

        failed_logins = np.random.poisson(1)

        device_change = np.random.choice([0, 1], p=[0.8, 0.2])

        country_risk_score = np.random.uniform(0, 1)

        transactions_last_1h = np.random.poisson(2)

        # Fraud logic (controlled)
        fraud_probability = (
            0.3 * (transaction_amount > 300) +
            0.2 * (account_age_days < 30) +
            0.2 * (failed_logins > 3) +
            0.1 * device_change +
            0.2 * (country_risk_score > 0.7)
        )

        is_fraud = 1 if fraud_probability > 0.5 else 0

        data.append([
            transaction_id,
            user_id,
            transaction_amount,
            account_age_days,
            failed_logins,
            device_change,
            country_risk_score,
            transactions_last_1h,
            is_fraud
        ])

    columns = [
        "transaction_id",
        "user_id",
        "transaction_amount",
        "account_age_days",
        "failed_logins",
        "device_change",
        "country_risk_score",
        "transactions_last_1h",
        "is_fraud"
    ]

    df = pd.DataFrame(data, columns=columns)

    df.to_csv("fraud_data.csv", index=False)
    print("Dataset generated successfully!")

if __name__ == "__main__":
    generate_data()