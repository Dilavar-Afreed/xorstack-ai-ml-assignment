import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import snowflake.connector
import os
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

# ========== LOAD FEATURE DATA ==========
query = "SELECT * FROM FRAUD_FEATURES"
df = pd.read_sql(query, conn)
print("Data loaded:", df.shape)
print("Columns:", df.columns)

print("Data loaded:", df.shape)

# ========== PREPARE DATA ==========
X = df.drop(columns=["IS_FRAUD"])
y = df["IS_FRAUD"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("Training size:", X_train.shape)
print("Test size:", X_test.shape)

# ========== HANDLE IMBALANCE ==========
scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

# ========== TRAIN MODEL ==========
model = xgb.XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    use_label_encoder=False
)

model.fit(X_train, y_train)

# ========== EVALUATION ==========
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)

print("\nROC-AUC Score:", auc)
print("\nClassification Report:")
print(classification_report(y_test, model.predict(X_test)))



joblib.dump(model, "fraud_model.pkl")
print("Model saved successfully!")

