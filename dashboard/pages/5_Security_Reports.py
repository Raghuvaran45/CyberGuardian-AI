import os
import sys
import sqlite3
import json
import pandas as pd
import streamlit as st


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
    page_title="Security Reports",
    page_icon="📄",
    layout="wide"
)


st.title("📄 CyberGuardian AI")
st.subheader("Advanced SOC Security Reports")


st.markdown(
"""
Professional incident reports generated from
AI-powered behavioral anomaly detection.
"""
)


st.divider()



# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------

try:

    conn = sqlite3.connect(
        "database/incidents.db"
    )


    reports = pd.read_sql(

        """
        SELECT *
        FROM incidents
        WHERE status='ANOMALY DETECTED'
        ORDER BY id DESC
        """,

        conn

    )


    conn.close()


except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    st.stop()



if reports.empty:

    st.warning(
        "No security incidents detected yet."
    )

    st.stop()



# --------------------------------------------------
# HANDLE MISSING COLUMNS
# --------------------------------------------------

default_values = {


    "incident_id":
    "Not Generated",


    "affected_entity":
    "Unknown",


    "source_ip":
    "Unknown",


    "device_information":
    "Unknown",


    "attack_summary":
    "Security anomaly detected.",


    "analyst_action":
    json.dumps(

        [

            "Verify affected user",

            "Review authentication logs",

            "Investigate source IP",

            "Monitor future activity"

        ]

    )

}



for column,value in default_values.items():

    if column not in reports.columns:

        reports[column] = value



# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

total = len(reports)


critical = len(

    reports[
        reports["risk_score"] >= 80
    ]

)


high = len(

    reports[
        reports["threat_level"] == "HIGH"
    ]

)


medium = len(

    reports[
        reports["threat_level"] == "MEDIUM"
    ]

)


low = len(

    reports[
        reports["threat_level"] == "LOW"
    ]

)



c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(
    "Incidents",
    total
)


c2.metric(
    "Critical",
    critical
)


c3.metric(
    "High",
    high
)


c4.metric(
    "Medium",
    medium
)


c5.metric(
    "Low",
    low
)



st.divider()



# --------------------------------------------------
# FILTERS
# --------------------------------------------------

left,right = st.columns(2)



with left:

    attack_filter = st.selectbox(

        "Attack Type",

        ["All"]

        +

        sorted(

            reports["attack_type"]
            .unique()
            .tolist()

        )

    )



with right:

    threat_filter = st.selectbox(

        "Threat Level",

        ["All"]

        +

        sorted(

            reports["threat_level"]
            .unique()
            .tolist()

        )

    )



filtered = reports.copy()



if attack_filter != "All":

    filtered = filtered[

        filtered["attack_type"]

        ==

        attack_filter

    ]



if threat_filter != "All":

    filtered = filtered[

        filtered["threat_level"]

        ==

        threat_filter

    ]



# --------------------------------------------------
# INCIDENT TABLE
# --------------------------------------------------

st.subheader(
    "📚 Security Incident History"
)



st.dataframe(

    filtered[

        [

            "id",

            "timestamp",

            "attack_type",

            "risk_score",

            "threat_level"

        ]

    ],

    use_container_width=True

)



st.divider()



# --------------------------------------------------
# SELECT INCIDENT
# --------------------------------------------------

st.subheader(
    "🔍 Detailed Incident Report"
)



selected = st.selectbox(

    "Select Incident ID",

    filtered["id"]

)



report = filtered[

    filtered["id"]

    ==

    selected

].iloc[0]



# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.header(
    "🚨 Executive Security Summary"
)



st.info(

    report["attack_summary"]

)



# --------------------------------------------------
# INCIDENT DETAILS
# --------------------------------------------------

left,right = st.columns(2)



with left:

    st.subheader(
        "Incident Information"
    )


    st.write(
        "**Incident ID:**",
        report["incident_id"]
    )


    st.write(
        "**Timestamp:**",
        report["timestamp"]
    )


    st.write(
        "**Status:**",
        report["status"]
    )


    st.write(
        "**Attack Type:**",
        report["attack_type"]
    )


    st.write(
        "**Risk Score:**",
        report["risk_score"]
    )


    st.write(
        "**Threat Level:**",
        report["threat_level"]
    )



with right:

    st.subheader(
        "Affected Entity"
    )


    st.write(
        "**Entity:**",
        report["affected_entity"]
    )


    st.write(
        "**Source IP:**",
        report["source_ip"]
    )


    st.write(
        "**Device:**",
        report["device_information"]
    )



st.divider()



# --------------------------------------------------
# ROOT CAUSE
# --------------------------------------------------

st.subheader(
    "🧠 Detection Reasons"
)



try:

    causes = json.loads(

        report["root_causes"]

    )

except:

    causes = []



if causes:

    for cause in causes:

        st.warning(cause)

else:

    st.info(
        "No root cause information available."
    )



st.divider()



# --------------------------------------------------
# MITRE ATT&CK
# --------------------------------------------------

st.subheader(
    "🎯 MITRE ATT&CK Mapping"
)



m1,m2,m3 = st.columns(3)



m1.metric(

    "Technique ID",

    report.get(
        "mitre_id",
        "Unknown"
    )

)


m2.metric(

    "Technique",

    report.get(
        "technique",
        "Unknown"
    )

)


m3.metric(

    "Tactic",

    report.get(
        "tactic",
        "Unknown"
    )

)



st.divider()



# --------------------------------------------------
# THREAT INTELLIGENCE
# --------------------------------------------------

st.subheader(
    "🌐 Threat Intelligence"
)



try:

    threat = json.loads(

        report["threat_intelligence"]

    )


    st.info(

        "Severity : "

        +

        threat["severity"]

    )


    st.write(

        "**Description:**",

        threat["description"]

    )


    st.write(

        "**Impact:**",

        threat["impact"]

    )


    st.write(
        "### Indicators of Compromise"
    )


    for ioc in threat["ioc"]:

        st.error(ioc)


except:

    st.info(
        "Threat intelligence unavailable."
    )



st.divider()



# --------------------------------------------------
# ANALYST ACTIONS
# --------------------------------------------------

st.subheader(
    "🛡 Analyst Recommended Actions"
)



try:

    actions = json.loads(

        report["analyst_action"]

    )

except:

    actions = []



for action in actions:

    st.success(action)



st.divider()



# --------------------------------------------------
# EXPORT
# --------------------------------------------------

st.subheader(
    "⬇ Export Report"
)



json_report = json.dumps(

    report.to_dict(),

    indent=4,

    default=str

)



st.download_button(

    "Download JSON Report",

    json_report,

    file_name=f"incident_{selected}.json",

    mime="application/json"

)



csv = filtered.to_csv(

    index=False

).encode()



st.download_button(

    "Download CSV Report",

    csv,

    file_name="security_reports.csv",

    mime="text/csv"

)



st.success(
"✅ Advanced SOC Security Reports Running Successfully"
)