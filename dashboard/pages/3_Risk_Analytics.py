import os
import sys
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Risk Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CyberGuardian AI")
st.subheader("Risk Analytics")

st.markdown(
"""
Analyze cyber risk trends, attack severity and overall security posture.
"""
)

st.divider()

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------

try:

    conn = sqlite3.connect("database/incidents.db")

    df = pd.read_sql(
        """
        SELECT *
        FROM incidents
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

except Exception as e:

    st.error(f"Database Error : {e}")
    st.stop()

if df.empty:

    st.warning("No incident data available.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total = len(df)

average_risk = round(df["risk_score"].mean(), 2)

maximum_risk = round(df["risk_score"].max(), 2)

minimum_risk = round(df["risk_score"].min(), 2)

high_risk = len(df[df["risk_score"] >= 70])

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Incidents", total)

c2.metric("Average Risk", average_risk)

c3.metric("Maximum Risk", maximum_risk)

c4.metric("Minimum Risk", minimum_risk)

c5.metric("High Risk", high_risk)

st.divider()

# --------------------------------------------------
# RISK SCORE DISTRIBUTION
# --------------------------------------------------

st.subheader("📈 Risk Score Distribution")

fig = px.histogram(
    df,
    x="risk_score",
    nbins=20,
    color_discrete_sequence=["crimson"]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# RISK TREND
# --------------------------------------------------

st.subheader("📉 Risk Trend Over Time")

df["timestamp"] = pd.to_datetime(df["timestamp"])

trend = df.sort_values("timestamp")

fig = px.line(
    trend,
    x="timestamp",
    y="risk_score",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# ATTACK RISK ANALYSIS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🎯 Average Risk by Attack")

    attack = (
        df.groupby("attack_type")["risk_score"]
        .mean()
        .reset_index()
        .sort_values("risk_score", ascending=False)
    )

    fig = px.bar(
        attack,
        x="attack_type",
        y="risk_score",
        color="attack_type",
        text="risk_score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("⚠ Threat Level Distribution")

    threat = (
        df["threat_level"]
        .value_counts()
        .reset_index()
    )

    threat.columns = [
        "Threat",
        "Count"
    ]

    fig = px.pie(
        threat,
        names="Threat",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# TOP DANGEROUS ATTACKS
# --------------------------------------------------

st.subheader("🔥 Top Dangerous Attack Types")

danger = (
    df.groupby("attack_type")["risk_score"]
    .mean()
    .reset_index()
    .sort_values("risk_score", ascending=False)
)

st.dataframe(
    danger,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# RISK HEATMAP
# --------------------------------------------------

st.subheader("🌡 Risk Heatmap")

heat = (
    df.pivot_table(
        values="risk_score",
        index="attack_type",
        columns="threat_level",
        aggfunc="mean",
        fill_value=0
    )
)

fig = px.imshow(
    heat,
    text_auto=".1f",
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# AI RISK INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Risk Insights")

highest_attack = danger.iloc[0]["attack_type"]
highest_score = round(danger.iloc[0]["risk_score"], 2)

st.success(f"Highest Risk Attack : {highest_attack}")

st.info(f"Average Risk Score : {average_risk}")

st.warning(f"High Risk Incidents : {high_risk}")

if average_risk >= 70:

    overall = "🔴 HIGH"

elif average_risk >= 40:

    overall = "🟡 MEDIUM"

else:

    overall = "🟢 LOW"

st.metric(
    "Overall Security Risk",
    overall
)

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Risk Analytics",
    csv,
    "risk_analytics.csv",
    "text/csv"
)

st.success("✅ Risk Analytics Module Running Successfully")