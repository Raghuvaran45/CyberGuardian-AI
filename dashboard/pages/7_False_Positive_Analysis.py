import os
import sys
import pandas as pd
import streamlit as st
import joblib

import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

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


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="False Positive Analysis",
    page_icon="📉",
    layout="wide"
)


st.title("📉 CyberGuardian AI")
st.subheader("False Positive Rate Analysis")


st.markdown(
"""
SOC analyst alert-budget evaluation.
Measures false positives and detection efficiency.
"""
)


st.divider()



# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    df = pd.read_csv(
        "data/processed_logs.csv"
    )

except Exception as e:

    st.error(
        f"Dataset Loading Error: {e}"
    )

    st.stop()



# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

try:

    anomaly_model = joblib.load(
        "models/anomaly_model.pkl"
    )

except Exception as e:

    st.error(
        f"Model Loading Error: {e}"
    )

    st.stop()



# --------------------------------------------------
# PREPARE FEATURES
# --------------------------------------------------

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



# --------------------------------------------------
# MODEL PREDICTION
# --------------------------------------------------

prediction = anomaly_model.predict(X)



scores = anomaly_model.decision_function(X)



df["prediction"] = [

    "Attack Alert"

    if value == -1

    else

    "Normal"

    for value in prediction

]



# --------------------------------------------------
# CORRECT RISK SCORE CALCULATION
# --------------------------------------------------

df["risk_score"] = (

    (scores.max() - scores)

    /

    (scores.max() - scores.min())

) * 100



# --------------------------------------------------
# TOP 1% ALERT BUDGET
# --------------------------------------------------

alert_budget = int(
    len(df) * 0.01
)



alerts = df.sort_values(

    by="risk_score",

    ascending=False

).head(

    alert_budget

)



# Debug information
with st.expander("Debug Information"):

    st.write(
        "Top Alert Target Distribution"
    )

    st.write(
        alerts["target"].value_counts()
    )



# --------------------------------------------------
# METRICS
# --------------------------------------------------

true_attacks = alerts[

    alerts["target"].astype(int) == 1

].shape[0]



false_positive = alerts[

    alerts["target"].astype(int) == 0

].shape[0]



false_positive_rate = (

    false_positive /

    alert_budget

) * 100



precision = (

    true_attacks /

    alert_budget

) * 100




# ==================================================
# KPI CARDS
# ==================================================

st.subheader(
    "📊 SOC Performance Metrics"
)



c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(
    "Total Events",
    len(df)
)


c2.metric(
    "Alert Budget (1%)",
    alert_budget
)


c3.metric(
    "True Attacks",
    true_attacks
)


c4.metric(
    "False Positives",
    false_positive
)


c5.metric(
    "False Positive Rate",
    f"{false_positive_rate:.2f}%"
)



st.divider()



# ==================================================
# TEXT REPORT
# ==================================================

st.subheader(
    "📋 Detailed SOC Analysis"
)



analysis_df = pd.DataFrame({

    "Metric":[

        "Total Security Events",

        "Alert Budget",

        "Generated Alerts",

        "True Attacks Detected",

        "False Positives",

        "False Positive Rate",

        "Alert Precision"

    ],


    "Value":[

        len(df),

        alert_budget,

        len(alerts),

        true_attacks,

        false_positive,

        f"{false_positive_rate:.2f}%",

        f"{precision:.2f}%"

    ]

})



st.table(
    analysis_df
)



st.divider()



# ==================================================
# GRAPH 1 ALERT BUDGET
# ==================================================

st.subheader(
    "📈 Alert Budget Comparison"
)



budget_df = pd.DataFrame({

    "Category":[

        "Allowed Alerts",

        "Generated Alerts"

    ],

    "Count":[

        alert_budget,

        len(alerts)

    ]

})



fig1 = px.bar(

    budget_df,

    x="Category",

    y="Count",

    text="Count",

    title="SOC Alert Budget"

)



st.plotly_chart(

    fig1,

    use_container_width=True

)



# ==================================================
# GRAPH 2 TRUE VS FALSE
# ==================================================

st.subheader(
    "🎯 True Attacks vs False Positives"
)



fp_df = pd.DataFrame({

    "Category":[

        "True Attacks",

        "False Positives"

    ],

    "Count":[

        true_attacks,

        false_positive

    ]

})



fig2 = px.pie(

    fp_df,

    names="Category",

    values="Count",

    hole=0.45

)



st.plotly_chart(

    fig2,

    use_container_width=True

)



# ==================================================
# GRAPH 3 - DETECTION EFFECTIVENESS
# ==================================================

st.subheader(
    "🎯 Detection Effectiveness"
)


effectiveness_df = pd.DataFrame({

    "Category":[

        "Detected Attacks",

        "False Positives"

    ],

    "Count":[

        true_attacks,

        false_positive

    ]

})



fig_effectiveness = px.bar(

    effectiveness_df,

    x="Category",

    y="Count",

    text="Count",

    title="SOC Detection Effectiveness"

)



st.plotly_chart(

    fig_effectiveness,

    use_container_width=True

)



st.divider()



# ==================================================
# GRAPH 4 - FALSE POSITIVE GAUGE
# ==================================================
st.subheader(
    "⚠ False Positive Rate"
)



gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=false_positive_rate,

        title={

            "text":

            "False Positive %"

        },

        gauge={

            "axis":{

                "range":[0,100]

            }

        }

    )

)



st.plotly_chart(

    gauge,

    use_container_width=True

)



# ==================================================
# GRAPH 4 RISK SCORE
# ==================================================

st.subheader(
    "📊 Risk Score Distribution"
)



fig4 = px.histogram(

    alerts,

    x="risk_score",

    nbins=40,

    title="Risk Score Distribution of Top Alerts"

)



st.plotly_chart(

    fig4,

    use_container_width=True

)



# ==================================================
# GRAPH 5 ATTACK TYPES
# ==================================================

st.subheader(
    "🔥 Attack Types in Alert Set"
)



attack_df = (

    alerts["attack_type"]

    .value_counts()

    .reset_index()

)



attack_df.columns = [

    "Attack Type",

    "Count"

]



fig5 = px.bar(

    attack_df,

    x="Attack Type",

    y="Count",

    text="Count",

    title="Detected Attack Categories"

)



st.plotly_chart(

    fig5,

    use_container_width=True

)



# ==================================================
# TOP RISK EVENTS
# ==================================================

st.subheader(
    "🚨 Highest Risk Security Events"
)



st.dataframe(

    alerts[

        [

            "attack_type",

            "risk_score",

            "target",

            "prediction"

        ]

    ],

    use_container_width=True

)



st.success(
"✅ False Positive Analysis Completed Successfully"
)