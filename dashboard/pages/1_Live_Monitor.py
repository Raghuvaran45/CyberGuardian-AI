import os
import sys
import sqlite3
import json

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Live Threat Monitor",
    page_icon="🛡️",
    layout="wide"
)
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10000, key="live_monitor")
st.title("🛡️ CyberGuardian AI SOC")

st.markdown(
"""
## 🟢 Live Threat Monitoring System

Real-time AI-powered cybersecurity monitoring platform
for detecting behavioral anomalies and suspicious activities.
"""
)

st.markdown(
"""
Real-time behavioral anomaly detection powered by Machine Learning.
"""
)

st.divider()

# --------------------------------------------------
# LOAD LATEST INCIDENT FROM DATABASE
# --------------------------------------------------

try:

    conn = sqlite3.connect("database/incidents.db")

    query = """
    SELECT *
    FROM incidents
    WHERE status='ANOMALY DETECTED'
    ORDER BY id DESC
    LIMIT 1
    """

    history = pd.read_sql(query, conn)

    conn.close()

except Exception as e:

    st.error(f"Database Error : {e}")
    st.stop()

if history.empty:

    st.info("No attacks detected yet.")
    st.stop()

latest = history.iloc[0]

result = {}
# --------------------------------------------------
# SOC STATUS BANNER
# --------------------------------------------------

result = {}

result["status"] = latest.get("status", "UNKNOWN")

result["attack_type"] = latest.get(
    "attack_type",
    "Unknown"
)

result["risk_score"] = latest.get(
    "risk_score",
    0
)

result["threat_level"] = latest.get(
    "threat_level",
    "LOW"
)


try:
    result["root_causes"] = json.loads(latest["root_causes"])
except:
    result["root_causes"] = []

try:
    result["recommendations"] = json.loads(latest["recommendations"])
except:
    result["recommendations"] = []

try:
    result["threat_intelligence"] = json.loads(latest["threat_intelligence"])
except:
    result["threat_intelligence"] = {
        "severity": "Unknown",
        "description": "Unavailable",
        "impact": "Unavailable",
        "ioc": []
    }

result["mitre_attack"] = {
    "technique_id": latest["mitre_id"],
    "technique": latest["technique"],
    "tactic": latest["tactic"]
}

result["incident_report"] = {
    "timestamp": latest["timestamp"],
    "status": latest["status"],
    "attack_type": latest["attack_type"],
    "risk_score": latest["risk_score"],
    "threat_level": latest["threat_level"]
}
# --------------------------------------------------
# SOC STATUS BANNER
# --------------------------------------------------

level = result.get(
    "threat_level",
    "LOW"
)


if level == "LOW":

    st.success(
        "🟢 SOC STATUS: SYSTEM SECURE"
    )


elif level == "MEDIUM":

    st.warning(
        "🟡 SOC STATUS: INVESTIGATION REQUIRED"
    )


elif level == "HIGH":

    st.error(
        "🔴 SOC STATUS: ACTIVE SECURITY INCIDENT"
    )


elif level == "CRITICAL":

    st.error(
        "🚨 SOC STATUS: CRITICAL INCIDENT"
    )
# --------------------------------------------------
# LIVE STATUS
# --------------------------------------------------

st.subheader("🚨 Current Security Status")

c1, c2, c3, c4 = st.columns(4)
st.divider()

st.subheader("📊 Security Overview")

a,b,c,d = st.columns(4)


a.metric(
    "Detection Engine",
    "Online 🟢"
)


b.metric(
    "ML Model",
    "Active"
)


c.metric(
    "Database",
    "Connected"
)


d.metric(
    "Monitoring",
    "Live"
)

with c1:

    if result["status"] == "NORMAL":
        st.success(result["status"])
    else:
        st.error(result["status"])

with c2:

    st.metric(
        "Attack Type",
        result["attack_type"]
    )

with c3:

    st.metric(
        "Risk Score",
        f"{float(result['risk_score']):.2f}"
    )

with c4:

    level = result["threat_level"]

    if level == "LOW":
    
        st.success(
        "🟢 LOW"
        )


    elif level == "MEDIUM":

        st.warning(
        "🟡 MEDIUM"
        )


    elif level == "HIGH":

        st.error(
        "🔴 HIGH"
        )


    elif level == "CRITICAL":

        st.error(
        "🚨 CRITICAL"
        )

st.divider()

# --------------------------------------------------
# RISK GAUGE
# --------------------------------------------------

st.subheader("📊 Live Risk Score")

risk_score = float(result["risk_score"])

gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=risk_score,

        title={
            "text": "Current Risk Score"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "red"
            },

            "steps": [

                {
                    "range": [0, 30],
                    "color": "#2ECC71"
                },

                {
                    "range": [30, 60],
                    "color": "#F1C40F"
                },

                {
                    "range": [60, 80],
                    "color": "#E67E22"
                },

                {
                    "range": [80, 100],
                    "color": "#E74C3C"
                }

            ]

        }

    )

)

st.plotly_chart(
    gauge,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# ROOT CAUSE
# --------------------------------------------------

st.subheader("🛡️ AI Security Recommendations")

if result["recommendations"]:
    for recommendation in result["recommendations"]:
        st.success(recommendation)
else:
    st.info("No recommendations available.")

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

st.subheader("🛡️ AI Security Recommendations")

if result["recommendations"]:
    for recommendation in result["recommendations"]:
        st.success(recommendation)
else:
    st.info("No recommendations available.")

# --------------------------------------------------
# MITRE ATT&CK
# --------------------------------------------------

st.subheader("🎯 MITRE ATT&CK Mapping")

mitre = result["mitre_attack"]

m1, m2, m3 = st.columns(3)

m1.metric(
    "Technique ID",
    mitre["technique_id"]
)

m2.metric(
    "Technique",
    mitre["technique"]
)

m3.metric(
    "Tactic",
    mitre["tactic"]
)

st.divider()

# --------------------------------------------------
# THREAT INTELLIGENCE
# --------------------------------------------------

st.subheader("🌐 Threat Intelligence")

threat = result["threat_intelligence"]

left, right = st.columns(2)

with left:

    st.metric("Severity", threat.get("severity", "Unknown"))

    st.write("### Description")
    st.write(threat.get("description", "Unavailable"))

    st.write("### Impact")
    st.write(threat.get("impact", "Unavailable"))

with right:

    st.write("### Indicators of Compromise")

    iocs = threat.get("ioc", [])

    if iocs:
        for ioc in iocs:
            st.error(ioc)
    else:
        st.success("No Indicators of Compromise found.")

# --------------------------------------------------
# INCIDENT SUMMARY
# --------------------------------------------------

st.subheader("📄 Latest Incident Report")

report = result["incident_report"]

c1, c2 = st.columns(2)

with c1:
    st.metric("Timestamp", report["timestamp"])
    st.metric("Status", report["status"])
    st.metric("Attack Type", report["attack_type"])

with c2:
    st.metric("Risk Score", report["risk_score"])
    st.metric("Threat Level", report["threat_level"])

st.divider()

st.subheader("📚 Recent Incident History")

try:

    conn = sqlite3.connect("database/incidents.db")

    history = pd.read_sql(
        """
        SELECT
            timestamp,
            attack_type,
            risk_score,
            threat_level,
            mitre_id
        FROM incidents
        ORDER BY id DESC
        LIMIT 10
        """,
        conn
    )

    conn.close()

    st.dataframe(
        history,
        use_container_width=True
    )

except Exception as e:

    st.error(f"Unable to load incident history: {e}")

# --------------------------------------------------
# DOWNLOAD SECURITY REPORT
# --------------------------------------------------

import json


report_json = json.dumps(
    report,
    indent=4
)


st.download_button(
    label="⬇ Download Incident Report",
    data=report_json,
    file_name="CyberGuardian_Incident_Report.json",
    mime="application/json"
)

st.success("✅ Live Threat Monitor Running Successfully")
