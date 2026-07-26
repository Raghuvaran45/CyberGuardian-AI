import streamlit as st
import pandas as pd

from monitoring.drift_detector import (
    calculate_data_drift,
    drift_status
)



st.set_page_config(

    page_title="Model Health",

    page_icon="🧠",

    layout="wide"

)



st.title(
    "🧠 CyberGuardian AI"
)

st.subheader(
    "🧠 Model Health Monitoring"
)


st.info(
"""
Concept drift monitoring compares current behavior patterns
against historical training data to identify when model
retraining may be required.
"""
)



training_data = pd.read_csv(

    "data/processed_logs.csv"

)


live_data = pd.read_csv(

    "data/live_event.csv"

)



drift = calculate_data_drift(

    training_data,

    live_data

)



status = drift_status(

    drift

)



# ------------------------------
# KPI
# ------------------------------

c1,c2,c3 = st.columns(3)



c1.metric(

    "Features Checked",

    len(drift)

)



c2.metric(

    "Average Drift",

    f"{sum(drift.values())/len(drift):.2f}%"

)



c3.metric(

    "Model Status",

    status

)



st.divider()



st.subheader(
    "📊 Feature Drift Analysis"
)



drift_df = pd.DataFrame(

    drift.items(),

    columns=[

        "Feature",

        "Drift %"

    ]

)



st.bar_chart(

    drift_df.set_index(

        "Feature"

    )

)



st.success(

    "✅ Model Health Monitoring Active"

)