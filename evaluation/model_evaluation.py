import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


import pandas as pd
import joblib


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)



# ==================================================
# LOAD DATA
# ==================================================

print("=" * 60)
print("CyberGuardian AI Model Evaluation")
print("=" * 60)


df = pd.read_csv(
    "data/processed_logs.csv"
)


print("\nDataset Shape:")
print(df.shape)



print("\nAttack Distribution:")
print(
    df["attack_type"].value_counts()
)



# ==================================================
# LOAD MODELS
# ==================================================

anomaly_model = joblib.load(
    "models/anomaly_model.pkl"
)


attack_model = joblib.load(
    "models/attack_classifier.pkl"
)


encoder = joblib.load(
    "models/attack_label_encoder.pkl"
)



# ==================================================
# FEATURE PREPARATION
# ==================================================

X = df.drop(
    columns=[
        "attack_type",
        "label",
        "target"
    ],
    errors="ignore"
)



# Match model features

features = anomaly_model.feature_names_in_


for feature in features:

    if feature not in X.columns:

        X[feature] = 0



X = X[features]



# ==================================================
# PART 1
# ANOMALY DETECTION EVALUATION
# ==================================================

print("\n")
print("=" * 60)
print("ANOMALY DETECTION MODEL")
print("=" * 60)



# Isolation Forest prediction

anomaly_prediction = anomaly_model.predict(
    X
)



# Convert output

anomaly_prediction = [

    "Attack" if value == -1
    else "Normal"

    for value in anomaly_prediction

]



actual_labels = df["label"]



accuracy = accuracy_score(
    actual_labels,
    anomaly_prediction
)


precision = precision_score(
    actual_labels,
    anomaly_prediction,
    pos_label="Attack",
    zero_division=0
)


recall = recall_score(
    actual_labels,
    anomaly_prediction,
    pos_label="Attack",
    zero_division=0
)


f1 = f1_score(
    actual_labels,
    anomaly_prediction,
    pos_label="Attack",
    zero_division=0
)



print(
    f"Accuracy  : {accuracy:.2f}"
)

print(
    f"Precision : {precision:.2f}"
)

print(
    f"Recall    : {recall:.2f}"
)

print(
    f"F1 Score  : {f1:.2f}"
)



print("\nConfusion Matrix:")

print(
    confusion_matrix(
        actual_labels,
        anomaly_prediction
    )
)



# ==================================================
# PART 2
# ATTACK CLASSIFICATION EVALUATION
# ==================================================

print("\n")
print("=" * 60)
print("ATTACK CLASSIFICATION MODEL")
print("=" * 60)



# Remove normal events

attack_df = df[
    df["attack_type"] != "Unknown"
]



print("\nAttack Evaluation Dataset:")
print(
    attack_df.shape
)



# Prepare attack features only

X_attack = attack_df.drop(
    columns=[
        "attack_type",
        "label",
        "target"
    ],
    errors="ignore"
)



# Align features

for feature in features:

    if feature not in X_attack.columns:

        X_attack[feature] = 0



X_attack = X_attack[features]



y_attack = attack_df[
    "attack_type"
]



# Predict attacks

prediction = attack_model.predict(
    X_attack
)



prediction_labels = encoder.inverse_transform(
    prediction
)



accuracy = accuracy_score(
    y_attack,
    prediction_labels
)


precision = precision_score(
    y_attack,
    prediction_labels,
    average="weighted",
    zero_division=0
)


recall = recall_score(
    y_attack,
    prediction_labels,
    average="weighted",
    zero_division=0
)


f1 = f1_score(
    y_attack,
    prediction_labels,
    average="weighted",
    zero_division=0
)



print(
    f"Accuracy  : {accuracy:.2f}"
)


print(
    f"Precision : {precision:.2f}"
)


print(
    f"Recall    : {recall:.2f}"
)


print(
    f"F1 Score  : {f1:.2f}"
)



print("\nClassification Report:")


print(
    classification_report(
        y_attack,
        prediction_labels,
        zero_division=0
    )
)



print("\n")
print("=" * 60)
print("Evaluation Completed Successfully")
print("=" * 60)