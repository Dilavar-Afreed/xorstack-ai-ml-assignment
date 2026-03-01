import pandas as pd
import snowflake.connector
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

# ========== SNOWFLAKE CONNECTION ==========
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database="FRAUD_DB",
    schema="FRAUD_SCHEMA"
)

print("Connected to Snowflake")

# ===============================
# LOAD FEATURE DATA
# ===============================

query = "SELECT * FROM FRAUD_FEATURES"
df = pd.read_sql(query, conn)

print("Loaded data:", df.shape)

# ===============================
# LOAD TRAINED MODEL
# ===============================

model = joblib.load("fraud_model.pkl")
print("Model loaded successfully")

# ===============================
# PREPARE FEATURES
# ===============================

X = df.drop(columns=["IS_FRAUD"])

# ===============================
# GENERATE PREDICTIONS
# ===============================

df["FRAUD_PROBABILITY"] = model.predict_proba(X)[:, 1]

def risk_label(prob):
    if prob > 0.8:
        return "HIGH"
    elif prob > 0.4:
        return "MEDIUM"
    else:
        return "LOW"

df["RISK_LEVEL"] = df["FRAUD_PROBABILITY"].apply(risk_label)

print("Predictions generated")

# ===============================
# KEEP ONLY REQUIRED COLUMNS
# ===============================

predictions_df = df[["TRANSACTION_ID", "FRAUD_PROBABILITY", "RISK_LEVEL"]]

# ===============================
# CREATE TABLE IN SNOWFLAKE
# ===============================

cursor = conn.cursor()

cursor.execute("""
CREATE OR REPLACE TABLE FRAUD_PREDICTIONS (
    TRANSACTION_ID INT,
    FRAUD_PROBABILITY FLOAT,
    RISK_LEVEL STRING
)
""")

print("Prediction table created")

# ===============================
# BULK INSERT USING executemany
# ===============================

insert_query = """
INSERT INTO FRAUD_PREDICTIONS 
(TRANSACTION_ID, FRAUD_PROBABILITY, RISK_LEVEL)
VALUES (%s, %s, %s)
"""

data_to_insert = list(predictions_df.itertuples(index=False, name=None))

cursor.executemany(insert_query, data_to_insert)

print(f"Inserted {len(data_to_insert)} rows into FRAUD_PREDICTIONS")

cursor.close()
conn.close()

print("Process completed successfully")