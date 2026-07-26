import os
import sys
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

from streamlit_autorefresh import st_autorefresh
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Incident Dashboard",
    page_icon="📋",
    layout="wide"
)
st_autorefresh(
    interval=10000,
    key="incident_dashboard"
)
st.title("📋 CyberGuardian AI")
st.subheader("Incident Dashboard")

st.markdown(
"""
View, search and analyze detected security incidents.
"""
)

st.divider()

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------

try:

    conn = sqlite3.connect("database/incidents.db")

    history_df = pd.read_sql(
        """
        SELECT
            id,
            timestamp,
            status,
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

    st.error(f"Database Error: {e}")
    st.stop()

# --------------------------------------------------
# NO INCIDENTS
# --------------------------------------------------

if history_df.empty:

    st.warning("No incidents found in database.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total = len(history_df)

critical = len(
    history_df[
        history_df["risk_score"] >= 80
    ]
)

high = len(
    history_df[
        history_df["threat_level"] == "HIGH"
    ]
)

medium = len(
    history_df[
        history_df["threat_level"] == "MEDIUM"
    ]
)

low = len(
    history_df[
        history_df["threat_level"] == "LOW"
    ]
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Incidents", total)

c2.metric("Critical", critical)

c3.metric("High", high)

c4.metric("Medium", medium)

c5.metric("Low", low)

st.divider()

st.divider()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    attack_filter = st.selectbox(
        "Filter by Attack Type",
        ["All"] + sorted(history_df["attack_type"].unique().tolist())
    )

with right:

    threat_filter = st.selectbox(
        "Filter by Threat Level",
        ["All"] + sorted(history_df["threat_level"].unique().tolist())
    )

filtered = history_df.copy()

if attack_filter != "All":

    filtered = filtered[
        filtered["attack_type"] == attack_filter
    ]

if threat_filter != "All":

    filtered = filtered[
        filtered["threat_level"] == threat_filter
    ]

st.subheader("🔍 Search Incident")

search = st.text_input(
    "Search by Attack Type"
)

if search:

    filtered = filtered[
        filtered["attack_type"]
        .str.contains(search, case=False)
    ]

# --------------------------------------------------
# INCIDENT TABLE
# --------------------------------------------------

st.subheader("📚 Incident History")

st.dataframe(
    filtered.set_index("id"),
    use_container_width=True
)

st.divider()

import plotly.express as px

st.divider()

st.subheader("📊 Threat Level Distribution")

fig = px.pie(

    filtered,

    names="threat_level",

    hole=0.45,

    title="Threat Levels"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# INCIDENT DETAILS
# --------------------------------------------------

st.subheader("🔍 Incident Details")

incident_ids = filtered["id"].tolist()

selected = st.selectbox(
    "Select Incident ID",
    incident_ids
)

incident = filtered[
    filtered["id"] == selected
].iloc[0]

left, right = st.columns(2)

with left:

    st.write("### General Information")

    st.write("**Timestamp:**", incident["timestamp"])
    st.write("**Status:**", incident["status"])
    st.write("**Attack Type:**", incident["attack_type"])
    risk = incident["risk_score"]

    if risk >= 80:

        st.error(f"Risk Score : {risk}")

    elif risk >= 60:

        st.warning(f"Risk Score : {risk}")

    else:

        st.success(f"Risk Score : {risk}")

with right:

    st.write("### Threat Information")

    level = incident["threat_level"]

    if level == "LOW":
        st.success(level)

    elif level == "MEDIUM":
        st.warning(level)

    elif level == "HIGH":
        st.error(level)

    else:
        st.info(level)

    st.write("**MITRE ID:**", incident["mitre_id"])
    st.write("**Technique:**", incident["technique"])
    st.write("**Tactic:**", incident["tactic"])

st.divider()

# --------------------------------------------------
# RECENT INCIDENTS
# --------------------------------------------------

st.subheader("🚨 Latest 10 Incidents")

recent = history_df.head(10)

st.dataframe(
    recent.set_index("id"),
    use_container_width=True
)

st.divider()

st.subheader("🚨 Attack Distribution")

attack_counts = (

    filtered["attack_type"]

    .value_counts()

    .reset_index()

)

attack_counts.columns = [

    "Attack",

    "Count"

]

fig = px.bar(

    attack_counts,

    x="Attack",

    y="Count",

    color="Attack",

    text="Count"

)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

st.subheader("📈 Incident Timeline")

timeline = filtered.copy()

timeline["timestamp"] = pd.to_datetime(
    timeline["timestamp"]
)

timeline = (

    timeline

    .groupby(

        timeline["timestamp"].dt.date

    )

    .size()

    .reset_index(name="Incidents")

)

fig = px.line(

    timeline,

    x="timestamp",

    y="Incidents",

    markers=True

)

st.plotly_chart(
    fig,
    use_container_width=True
)
# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Incident History",
    csv,
    "incident_history.csv",
    "text/csv"
)


# --------------------------------------------------
# THREAT SEVERITY DISTRIBUTION
# --------------------------------------------------



st.divider()

st.subheader(
    "📈 Threat Severity Distribution"
)


severity_count = history_df[
    "threat_level"
].value_counts().reset_index()


severity_count.columns = [
    "Threat Level",
    "Count"
]


fig = px.pie(
    severity_count,
    names="Threat Level",
    values="Count",
    hole=0.4
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.success("✅ Incident Dashboard Running Successfully")