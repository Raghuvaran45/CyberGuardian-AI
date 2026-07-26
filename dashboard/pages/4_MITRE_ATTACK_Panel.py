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
    page_title="MITRE ATT&CK Panel",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 CyberGuardian AI")
st.subheader("MITRE ATT&CK Panel")

st.markdown(
"""
Analyze detected attacks using the MITRE ATT&CK Framework.
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
        SELECT
            id,
            timestamp,
            attack_type,
            risk_score,
            threat_level,
            mitre_id,
            technique,
            tactic
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

    st.warning("No MITRE incidents available.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total = len(df)

unique_techniques = df["technique"].nunique()

unique_tactics = df["tactic"].nunique()

top_technique = df["technique"].mode()[0]

top_tactic = df["tactic"].mode()[0]

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Incidents", total)

c2.metric("Techniques", unique_techniques)

c3.metric("Tactics", unique_tactics)

c4.metric("Top Technique", top_technique)

c5.metric("Top Tactic", top_tactic)

st.divider()

# --------------------------------------------------
# TECHNIQUE DISTRIBUTION
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🎯 Technique Distribution")

    technique_df = (
        df.groupby(["mitre_id", "technique"])
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        technique_df,
        x="mitre_id",
        y="Count",
        color="technique",
        text="Count",
        hover_data=["technique"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🛡 Tactic Distribution")

    tactic_df = (
        df["tactic"]
        .value_counts()
        .reset_index()
    )

    tactic_df.columns = [
        "Tactic",
        "Count"
    ]

    fig = px.pie(
        tactic_df,
        names="Tactic",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# TECHNIQUE FREQUENCY
# --------------------------------------------------

st.subheader("📋 MITRE Technique Frequency")

technique_table = (
    df.groupby(
        ["mitre_id", "technique"]
    )
    .size()
    .reset_index(name="Occurrences")
    .sort_values(
        "Occurrences",
        ascending=False
    )
)

st.dataframe(
    technique_table,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# TACTIC FREQUENCY
# --------------------------------------------------

st.subheader("📋 MITRE Tactic Frequency")

tactic_table = (
    df.groupby("tactic")
    .size()
    .reset_index(name="Occurrences")
    .sort_values(
        "Occurrences",
        ascending=False
    )
)

st.dataframe(
    tactic_table,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# INCIDENT MATRIX
# --------------------------------------------------

st.subheader("🗂 MITRE Incident Matrix")

matrix = df[
    [
        "timestamp",
        "attack_type",
        "mitre_id",
        "technique",
        "tactic",
        "risk_score",
        "threat_level"
    ]
]

st.dataframe(
    matrix,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# HIGH RISK TECHNIQUES
# --------------------------------------------------

st.subheader("🚨 High Risk MITRE Techniques")

high = df[
    df["risk_score"] >= 70
]

if high.empty:

    st.success("No High Risk MITRE incidents detected.")

else:

    st.dataframe(
        high[
            [
                "timestamp",
                "attack_type",
                "mitre_id",
                "technique",
                "tactic",
                "risk_score",
                "threat_level"
            ]
        ],
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI MITRE Insights")

highest = (
    df.groupby("technique")["risk_score"]
    .mean()
    .sort_values(ascending=False)
)

highest_technique = highest.index[0]

highest_score = round(highest.iloc[0], 2)

st.success(
    f"Most Common Technique : {top_technique}"
)

st.info(
    f"Most Common Tactic : {top_tactic}"
)

st.warning(
    f"Highest Risk Technique : {highest_technique} ({highest_score})"
)

st.error(
    "SOC Recommendation : Prioritize monitoring Credential Access and Defense Evasion techniques."
)

st.divider()

# --------------------------------------------------
# MITRE ATTACK MAP
# --------------------------------------------------

st.subheader("🧩 MITRE ATT&CK Mapping")

st.markdown("""
| Technique ID | Technique | Tactic |
|--------------|-----------|--------|
| T1110 | Brute Force | Credential Access |
| T1078 | Valid Accounts | Defense Evasion |
| T1021 | Remote Services | Lateral Movement |
| T1036 | Masquerading | Defense Evasion |
| T1071 | Application Layer Protocol | Command and Control |
| T1087 | Account Discovery | Discovery |
""")

st.divider()

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download MITRE Analytics",
    csv,
    "mitre_attack_analytics.csv",
    "text/csv"
)

st.success("✅ MITRE ATT&CK Panel Running Successfully")