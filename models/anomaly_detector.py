import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

print("=" * 60)
print("TRAINING ANOMALY DETECTOR")
print("=" * 60)

# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------

df = pd.read_csv("data/processed_logs.csv")

print("Dataset Loaded Successfully")
print(df.shape)

# -------------------------------------------------
# FEATURES
# -------------------------------------------------

drop_columns = [

    "label",
    "attack_type",
    "target"

]

X = df.drop(columns=drop_columns)

y = df["target"]

# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

model = IsolationForest(

    n_estimators=150,
    contamination=0.03,
    random_state=42

)

model.fit(X)

# -------------------------------------------------
# PREDICTIONS
# -------------------------------------------------

pred = model.predict(X)

pred = [0 if i == 1 else 1 for i in pred]

# -------------------------------------------------
# METRICS
# -------------------------------------------------

print("\nAccuracy :", round(accuracy_score(y, pred),4))
print("Precision:", round(precision_score(y, pred),4))
print("Recall   :", round(recall_score(y, pred),4))
print("F1 Score :", round(f1_score(y, pred),4))

print("\nClassification Report\n")

print(classification_report(y, pred))

print("\nConfusion Matrix\n")

print(confusion_matrix(y, pred))

# -------------------------------------------------
# SAVE MODEL
# -------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/anomaly_model.pkl")

print("\nModel Saved Successfully")

print("Location : models/anomaly_model.pkl")

print("=" * 60)