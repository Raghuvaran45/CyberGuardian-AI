import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.preprocessing import LabelEncoder


print("=" * 70)
print("CYBERGUARDIAN AI")
print("CYBER ATTACK CLASSIFICATION MODEL TRAINING")
print("=" * 70)



# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "data/processed_logs.csv"
)


print("\nDataset Loaded Successfully")
print("Original Dataset Shape:", df.shape)



# =========================================================
# KEEP ONLY ATTACK EVENTS
# =========================================================

df = df[
    df["target"] == 1
].copy()



print(
    "\nAttack Samples:",
    len(df)
)



print(
    "\nAttack Distribution:"
)

print(
    df["attack_type"].value_counts()
)



# =========================================================
# CREATE TARGET LABEL
# =========================================================

encoder = LabelEncoder()


y = encoder.fit_transform(
    df["attack_type"]
)



# =========================================================
# CREATE FEATURES
# =========================================================

X = df.drop(

    columns=[

        "label",

        "target",

        "attack_type"

    ],

    errors="ignore"

)



print(
    "\nNumber of Features:",
    X.shape[1]
)



print(
    "\nFeature Names:"
)

print(
    X.columns.tolist()
)



# =========================================================
# TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.25,

    random_state=42,

    stratify=y,

    shuffle=True

)



print(
    "\nTraining Samples:",
    len(X_train)
)


print(
    "Testing Samples:",
    len(X_test)
)



# =========================================================
# RANDOM FOREST MODEL
# =========================================================

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=15,

    min_samples_split=5,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1

)



print(
    "\nTraining Model..."
)



model.fit(

    X_train,

    y_train

)



print(
    "Training Completed"
)



# =========================================================
# MODEL PREDICTION
# =========================================================

prediction = model.predict(

    X_test

)



# =========================================================
# MODEL EVALUATION
# =========================================================

accuracy = accuracy_score(

    y_test,

    prediction

)



balanced_accuracy = balanced_accuracy_score(

    y_test,

    prediction

)



print("\n")
print("=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)



print(

    "Accuracy:",

    round(accuracy,4)

)


print(

    "Balanced Accuracy:",

    round(balanced_accuracy,4)

)



print(
    "\nClassification Report\n"
)


print(

    classification_report(

        y_test,

        prediction,

        target_names=encoder.classes_,

        zero_division=0

    )

)



print(
    "\nConfusion Matrix\n"
)


print(

    confusion_matrix(

        y_test,

        prediction

    )

)



# =========================================================
# FEATURE IMPORTANCE
# =========================================================

importance = pd.DataFrame({

    "Feature":

    X.columns,


    "Importance":

    model.feature_importances_

})



importance = importance.sort_values(

    by="Importance",

    ascending=False

)



print(
    "\nTop 15 Important Features\n"
)


print(

    importance.head(15)

)



# =========================================================
# SAVE MODEL
# =========================================================

os.makedirs(

    "models",

    exist_ok=True

)



joblib.dump(

    model,

    "models/attack_classifier.pkl"

)



joblib.dump(

    encoder,

    "models/attack_label_encoder.pkl"

)



print("\n")
print("=" * 70)

print(
    "Model Saved Successfully"
)

print(
    "models/attack_classifier.pkl"
)


print(
    "models/attack_label_encoder.pkl"
)


print("=" * 70)