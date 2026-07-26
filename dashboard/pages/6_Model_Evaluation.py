import streamlit as st
import os
import sys
import pandas as pd
import joblib
import plotly.express as px

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# PATH SETUP
# ==================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Model Evaluation",
    page_icon="📊",
    layout="wide"
)


st.title("📊 CyberGuardian AI")
st.subheader("Machine Learning Model Evaluation")


st.write(
"""
Performance analysis of anomaly detection and attack classification models.
"""
)


st.divider()



# ==================================================
# LOAD DATA
# ==================================================

try:

    df = pd.read_csv(
        "data/processed_logs.csv"
    )

except Exception as e:

    st.error(
        f"Dataset Loading Error: {e}"
    )

    st.stop()



# ==================================================
# DATA DISTRIBUTION
# ==================================================

st.header(
    "📌 Dataset Attack Distribution"
)


attack_distribution = (

    df["attack_type"]
    .value_counts()
    .reset_index()

)


attack_distribution.columns = [

    "Attack Type",

    "Count"

]


pie_chart = px.pie(

    attack_distribution,

    names="Attack Type",

    values="Count",

    hole=0.4,

    title="Cybersecurity Dataset Distribution"

)


st.plotly_chart(
    pie_chart,
    use_container_width=True
)



st.divider()



# ==================================================
# LOAD MODELS
# ==================================================

try:

    anomaly_model = joblib.load(
        "models/anomaly_model.pkl"
    )


    attack_model = joblib.load(
        "models/attack_classifier.pkl"
    )


    encoder = joblib.load(
        "models/attack_label_encoder.pkl"
    )


except Exception as e:

    st.error(
        f"Model Loading Error: {e}"
    )

    st.stop()



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



features = anomaly_model.feature_names_in_



for feature in features:

    if feature not in X.columns:

        X[feature] = 0



X = X[features]



# ==================================================
# ANOMALY DETECTION
# ==================================================

st.header(
    "🚨 Anomaly Detection Model"
)



anomaly_prediction = anomaly_model.predict(
    X
)



anomaly_prediction = [

    "Attack"
    if value == -1
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



c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Accuracy",
    f"{accuracy*100:.2f}%"
)


c2.metric(
    "Precision",
    f"{precision*100:.2f}%"
)


c3.metric(
    "Recall",
    f"{recall*100:.2f}%"
)


c4.metric(
    "F1 Score",
    f"{f1*100:.2f}%"
)



# -------- Anomaly Bar Chart --------


metrics_df = pd.DataFrame({

    "Metric":[

        "Accuracy",

        "Precision",

        "Recall",

        "F1 Score"

    ],

    "Score":[

        accuracy,

        precision,

        recall,

        f1

    ]

})


fig = px.bar(

    metrics_df,

    x="Metric",

    y="Score",

    text_auto=".2%",

    title="Anomaly Detection Performance"

)


st.plotly_chart(

    fig,

    use_container_width=True

)



# -------- Confusion Matrix --------


st.subheader(
    "🔥 Confusion Matrix"
)



cm = confusion_matrix(

    actual_labels,

    anomaly_prediction

)



cm_df = pd.DataFrame(

    cm,

    columns=[

        "Predicted Attack",

        "Predicted Normal"

    ],

    index=[

        "Actual Attack",

        "Actual Normal"

    ]

)



fig = px.imshow(

    cm_df,

    text_auto=True,

    title="Anomaly Detection Confusion Matrix"

)


st.plotly_chart(

    fig,

    use_container_width=True

)



st.divider()



# ==================================================
# ATTACK CLASSIFICATION
# ==================================================

st.header(
    "🎯 Attack Classification Model"
)



# Remove normal events

attack_df = df[

    df["attack_type"] != "Unknown"

]



X_attack = attack_df.drop(

    columns=[

        "attack_type",

        "label",

        "target"

    ],

    errors="ignore"

)



for feature in features:

    if feature not in X_attack.columns:

        X_attack[feature] = 0



X_attack = X_attack[features]



y_attack = attack_df[

    "attack_type"

]



prediction = attack_model.predict(

    X_attack

)



prediction_labels = encoder.inverse_transform(

    prediction

)



accuracy2 = accuracy_score(

    y_attack,

    prediction_labels

)


precision2 = precision_score(

    y_attack,

    prediction_labels,

    average="weighted",

    zero_division=0

)


recall2 = recall_score(

    y_attack,

    prediction_labels,

    average="weighted",

    zero_division=0

)


f12 = f1_score(

    y_attack,

    prediction_labels,

    average="weighted",

    zero_division=0

)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

    "Accuracy",

    f"{accuracy2*100:.2f}%"

)


c2.metric(

    "Precision",

    f"{precision2*100:.2f}%"

)


c3.metric(

    "Recall",

    f"{recall2*100:.2f}%"

)


c4.metric(

    "F1 Score",

    f"{f12*100:.2f}%"

)



# -------- Classification Bar Chart --------


classification_metrics = pd.DataFrame({

    "Metric":[

        "Accuracy",

        "Precision",

        "Recall",

        "F1 Score"

    ],

    "Score":[

        accuracy2,

        precision2,

        recall2,

        f12

    ]

})



fig = px.bar(

    classification_metrics,

    x="Metric",

    y="Score",

    text_auto=".2%",

    title="Attack Classification Performance"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



st.divider()



# ==================================================
# CLASSIFICATION REPORT
# ==================================================

st.header(
    "📄 Detailed Classification Report"
)



report = classification_report(

    y_attack,

    prediction_labels,

    output_dict=True,

    zero_division=0

)



report_df = pd.DataFrame(

    report

).transpose()



st.dataframe(

    report_df,

    use_container_width=True

)



# Heatmap

heatmap_df = report_df.drop(

    index=[

        "accuracy",

        "macro avg",

        "weighted avg"

    ],

    errors="ignore"

)



fig = px.imshow(

    heatmap_df[

        [

            "precision",

            "recall",

            "f1-score"

        ]

    ],

    text_auto=".2f",

    title="Attack Class Performance Heatmap"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



st.success(
    "✅ Model Evaluation Completed Successfully"
)