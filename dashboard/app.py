import os
import sys
import sqlite3
import json

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.graph_objects as go


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


from engine.prediction_engine import predict_event



# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="CyberGuardian AI SOC",
    page_icon="🛡️",
    layout="wide"
)
# Auto refresh dashboard every 5 seconds

st_autorefresh(
    interval=10000,
    key="cyberguardian_refresh"
)



# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(
    "data/logs.csv"
)



# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title(
    "🛡️ CyberGuardian AI SOC Dashboard"
)


st.markdown(
"""
AI-Powered Behavioral Anomaly Detection
for Cybersecurity Monitoring
"""
)


st.divider()



# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title(
    "🛡️ CyberGuardian AI"
)


attack_options = sorted(
    df["attack_type"]
    .dropna()
    .unique()
    .tolist()
)


location_options = sorted(
    df["geo_location"]
    .dropna()
    .unique()
    .tolist()
)


login_options = sorted(
    df["login_status"]
    .dropna()
    .unique()
    .tolist()
)



selected_attacks = st.sidebar.multiselect(

    "Attack Type",

    attack_options,

    default=attack_options

)


selected_locations = st.sidebar.multiselect(

    "Geo Location",

    location_options,

    default=location_options

)


selected_login = st.sidebar.multiselect(

    "Login Status",

    login_options,

    default=login_options

)



filtered_df = df[

    (df["geo_location"].isin(selected_locations))

    &

    (df["login_status"].isin(selected_login))

]



attack_df = filtered_df[

    (filtered_df["label"]=="Attack")

    &

    (filtered_df["attack_type"].isin(selected_attacks))

]



# -------------------------------------------------
# LIVE INCIDENT
# -------------------------------------------------

st.subheader(
    "🚨 Live Incident Summary"
)


result = None



if os.path.exists(
    "data/live_event.csv"
):

    try:

        result = predict_event(
            "data/live_event.csv"
        )


    except Exception as e:

        st.error(
            f"Prediction Error : {e}"
        )



if result:


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(
        "Status",
        result.get(
            "status",
            "UNKNOWN"
        )
    )


    c2.metric(
        "Attack Type",
        result.get(
            "attack_type",
            "Unknown"
        )
    )


    c3.metric(
        "Risk Score",
        f"{float(result.get('risk_score',0)):.2f}"
    )


    c4.metric(
        "Threat Level",
        result.get(
            "threat_level",
            "LOW"
        )
    )


else:

    st.info(
        "Waiting for security events..."
    )



st.divider()



# -------------------------------------------------
# ROOT CAUSE
# -------------------------------------------------

if result:


    st.subheader(
        "🧠 Root Cause Analysis"
    )


    causes = result.get(
        "root_causes",
        []
    )


    if causes:

        for cause in causes:

            st.warning(
                cause
            )

    else:

        st.info(
            "No suspicious behavior detected."
        )



    st.divider()



# -------------------------------------------------
# AI RECOMMENDATIONS
# -------------------------------------------------

if result:


    st.subheader(
        "🛡 AI Recommendations"
    )


    recommendations = result.get(
        "recommendations",
        []
    )


    if recommendations:

        for rec in recommendations:

            st.success(
                rec
            )

    else:

        st.info(
            "Continue monitoring."
        )



    st.divider()



# -------------------------------------------------
# INCIDENT REPORT
# -------------------------------------------------

if result:


    st.subheader(
        "📄 Latest Incident Report"
    )


    report = result.get(
        "incident_report",
        {}
    )


    st.markdown(
        "### Incident Summary"
    )


    c1,c2 = st.columns(2)


    with c1:

        st.write(
            "**Timestamp:**",
            report.get(
                "timestamp",
                "-"
            )
        )


        st.write(
            "**Status:**",
            report.get(
                "status",
                "-"
            )
        )


        st.write(
            "**Attack Type:**",
            report.get(
                "attack_type",
                "-"
            )
        )


    with c2:


        st.write(
            "**Risk Score:**",
            report.get(
                "risk_score",
                0
            )
        )


        st.write(
            "**Threat Level:**",
            report.get(
                "threat_level",
                "LOW"
            )
        )



    st.divider()



    st.subheader(
        "🧠 Root Causes"
    )


    for cause in report.get(
        "root_causes",
        []
    ):

        st.warning(
            cause
        )



    st.subheader(
        "🛡 Recommendations"
    )


    for rec in report.get(
        "recommendations",
        []
    ):

        st.success(
            rec
        )



    st.subheader(
        "🎯 MITRE ATT&CK Mapping"
    )


    mitre = report.get(
        "mitre_attack",
        {}
    )


    st.table(

        pd.DataFrame(

            {

            "Field":[
                "Technique ID",
                "Technique",
                "Tactic"
            ],


            "Value":[

                mitre.get(
                    "technique_id",
                    "Unknown"
                ),

                mitre.get(
                    "technique",
                    "Unknown"
                ),

                mitre.get(
                    "tactic",
                    "Unknown"
                )

            ]

            }

        )

    )
    # -------------------------------------------------
# THREAT INTELLIGENCE
# -------------------------------------------------

if result:

    st.subheader(
        "🌐 Threat Intelligence"
    )


    report = result.get(
        "incident_report",
        {}
    )


    threat = report.get(
        "threat_intelligence",
        {}
    )


    if threat:


        st.info(
            "Severity : "
            +
            str(
                threat.get(
                    "severity",
                    "Unknown"
                )
            )
        )


        st.write(
            "**Description:**",
            threat.get(
                "description",
                "Unavailable"
            )
        )


        st.write(
            "**Impact:**",
            threat.get(
                "impact",
                "Unavailable"
            )
        )


        st.write(
            "**Indicators of Compromise:**"
        )


        for ioc in threat.get(
            "ioc",
            []
        ):

            st.error(
                ioc
            )


    else:

        st.info(
            "Threat intelligence unavailable."
        )


    st.divider()



# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

st.subheader(
    "📊 SOC Overview"
)



total_logs = len(
    filtered_df
)


normal_logs = len(

    filtered_df[
        filtered_df["label"]
        ==
        "Normal"
    ]

)


attack_logs = len(

    filtered_df[
        filtered_df["label"]
        ==
        "Attack"
    ]

)


attack_rate = (

    round(
        (
            attack_logs /
            total_logs
        )
        *
        100,

        2

    )

    if total_logs > 0

    else 0

)



c1,c2,c3,c4 = st.columns(4)



c1.metric(
    "📄 Total Logs",
    total_logs
)


c2.metric(
    "✅ Normal Events",
    normal_logs
)


c3.metric(
    "🚨 Attack Events",
    attack_logs
)


c4.metric(
    "⚠ Attack Rate",
    f"{attack_rate}%"
)



st.divider()



# -------------------------------------------------
# LIVE THREAT GAUGE
# -------------------------------------------------

left,right = st.columns(2)



with left:


    st.subheader(
        "🚨 Current Risk Score"
    )


    risk_score = 0


    if result:

        risk_score = float(

            result.get(
                "risk_score",
                0
            )

        )


    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=risk_score,

            title={
                "text":
                "Threat Risk"
            },

            gauge={

                "axis":
                {
                    "range":
                    [
                        0,
                        100
                    ]
                },


                "steps":

                [

                    {
                    "range":
                    [
                        0,
                        30
                    ],

                    "color":
                    "green"

                    },


                    {
                    "range":
                    [
                        30,
                        60
                    ],

                    "color":
                    "yellow"

                    },


                    {
                    "range":
                    [
                        60,
                        80
                    ],

                    "color":
                    "orange"

                    },


                    {
                    "range":
                    [
                        80,
                        100
                    ],

                    "color":
                    "red"

                    }

                ]

            }

        )

    )


    st.plotly_chart(
        gauge,
        use_container_width=True
    )



with right:


    st.subheader(
        "🤖 AI Security Recommendation"
    )


    if result:


        attack = result.get(
            "attack_type",
            "Unknown"
        )


        if attack == "Brute Force":

            recommendation = """

🔴 Brute force attack detected.

✔ Lock affected account

✔ Enable MFA

✔ Block suspicious IP

"""


        elif attack == "Credential Stuffing":


            recommendation = """

🟠 Credential stuffing detected.

✔ Reset passwords

✔ Block source IP

✔ Review login activity

"""


        elif attack == "Lateral Movement":


            recommendation = """

🔴 Lateral movement detected.

✔ Isolate device

✔ Review network traffic

✔ Notify SOC

"""


        elif attack == "Impossible Travel":


            recommendation = """

🟡 Impossible travel detected.

✔ Verify user identity

✔ Enable MFA

"""


        else:


            recommendation = """

🟢 Continue monitoring activity.

✔ Review future events

✔ Maintain security controls

"""


        st.info(
            recommendation
        )


        st.metric(
            "Detected Attack",
            attack
        )


    else:

        st.success(
            "No active incident."
        )



st.divider()



# -------------------------------------------------
# ATTACK ANALYTICS
# -------------------------------------------------

left,right = st.columns(2)



with left:


    st.subheader(
        "🚨 Attack Distribution"
    )


    if not attack_df.empty:


        attack_counts = (

            attack_df[
                "attack_type"
            ]

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

            text="Count"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:

        st.info(
            "No attacks found."
        )



with right:


    st.subheader(
        "🔐 Login Status Distribution"
    )


    login_counts = (

        filtered_df[
            "login_status"
        ]

        .value_counts()

        .reset_index()

    )


    login_counts.columns = [

        "Status",

        "Count"

    ]


    fig = px.pie(

        login_counts,

        names="Status",

        values="Count",

        hole=0.5

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



st.divider()



# -------------------------------------------------
# GEO LOCATION ANALYSIS
# -------------------------------------------------

left,right = st.columns(2)



with left:


    st.subheader(
        "🌍 Geographic Activity"
    )


    geo = (

        filtered_df[
            "geo_location"
        ]

        .value_counts()

        .reset_index()

    )


    geo.columns=[

        "Location",

        "Count"

    ]


    fig = px.bar(

        geo,

        x="Location",

        y="Count"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



with right:


    st.subheader(
        "📂 Resource Access"
    )


    resource = (

        filtered_df[
            "resource_accessed"
        ]

        .value_counts()

        .head(10)

        .reset_index()

    )


    resource.columns=[

        "Resource",

        "Count"

    ]


    fig = px.bar(

        resource,

        x="Resource",

        y="Count"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )
    # -------------------------------------------------
# RECENT ATTACK ALERTS
# -------------------------------------------------

st.divider()

st.subheader(
    "🚨 Recent Attack Alerts"
)


if not attack_df.empty:


    if len(attack_df) > 10:

        alerts = attack_df.sample(
            10,
            random_state=42
        )

    else:

        alerts = attack_df



    alerts = alerts.reset_index(
        drop=True
    )


    alerts.index = alerts.index + 1



    st.dataframe(

        alerts[

            [

                "entity_id",

                "source_ip",

                "geo_location",

                "attack_type",

                "resource_accessed",

                "login_status"

            ]

        ],

        use_container_width=True

    )


else:

    st.info(
        "No attack alerts available."
    )



st.divider()



# -------------------------------------------------
# ATTACK TIMELINE
# -------------------------------------------------

st.subheader(
    "📈 Attack Timeline"
)



if not attack_df.empty:


    timeline = attack_df.copy()



    timeline["timestamp"] = pd.to_datetime(

        timeline["timestamp"]

    )



    timeline = (

        timeline

        .groupby(

            timeline["timestamp"].dt.date

        )

        .size()

        .reset_index(

            name="Attacks"

        )

    )



    fig = px.line(

        timeline,

        x="timestamp",

        y="Attacks",

        markers=True,

        title="Daily Attack Trend"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:

    st.info(
        "No attack timeline available."
    )



st.divider()



# -------------------------------------------------
# SYSTEM HEALTH
# -------------------------------------------------

st.subheader(
    "🖥️ System Health"
)



c1,c2,c3 = st.columns(3)



c1.metric(
    "Isolation Forest",
    "Healthy ✅"
)


c2.metric(
    "Random Forest",
    "Healthy ✅"
)


c3.metric(
    "SOC Dashboard",
    "Online 🟢"
)



st.divider()



# -------------------------------------------------
# INCIDENT HISTORY FROM DATABASE
# -------------------------------------------------

st.subheader(
    "📚 Incident History"
)



history_df = pd.DataFrame()



try:


    conn = sqlite3.connect(

        "database/incidents.db"

    )


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


    st.error(

        f"Database Error: {e}"

    )




if not history_df.empty:


    st.dataframe(

        history_df,

        use_container_width=True

    )



    st.markdown(

        "### 🔍 Incident Details"

    )



    incident_id = st.selectbox(

        "Select Incident",

        history_df["id"].tolist()

    )



    selected = history_df[

        history_df["id"]

        ==

        incident_id

    ].iloc[0]



    c1,c2 = st.columns(2)



    with c1:


        st.write(

            "**Timestamp:**",

            selected["timestamp"]

        )


        st.write(

            "**Attack Type:**",

            selected["attack_type"]

        )


        st.write(

            "**Risk Score:**",

            selected["risk_score"]

        )



    with c2:


        st.write(

            "**Status:**",

            selected["status"]

        )


        level = selected["threat_level"]



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

                "🟠 HIGH"

            )


        elif level == "CRITICAL":

            st.error(

                "🔴 CRITICAL"

            )


        else:

            st.write(level)



    st.write(

        "**MITRE ID:**",

        selected["mitre_id"]

    )


    st.write(

        "**Technique:**",

        selected["technique"]

    )


    st.write(

        "**Tactic:**",

        selected["tactic"]

    )



else:


    st.info(

        "No incidents stored yet."

    )



st.divider()



# -------------------------------------------------
# MITRE ATT&CK ANALYTICS
# -------------------------------------------------

st.subheader(
    "🎯 MITRE ATT&CK Analytics"
)



if not history_df.empty:


    mitre_df = (

        history_df

        .groupby(

            "technique"

        )

        .size()

        .reset_index(

            name="Count"

        )

    )



    fig = px.bar(

        mitre_df,

        x="technique",

        y="Count",

        text="Count",

        title="MITRE Technique Frequency"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:

    st.info(

        "No MITRE data available."

    )



st.divider()



# -------------------------------------------------
# DOWNLOAD REPORTS
# -------------------------------------------------

st.subheader(
    "⬇ Export Security Data"
)



csv = filtered_df.to_csv(

    index=False

).encode("utf-8")



st.download_button(

    label="Download Logs CSV",

    data=csv,

    file_name="cyberguardian_logs.csv",

    mime="text/csv"

)



if not history_df.empty:


    incident_csv = history_df.to_csv(

        index=False

    ).encode("utf-8")



    st.download_button(

        label="Download Incident Reports",

        data=incident_csv,

        file_name="incident_reports.csv",

        mime="text/csv"

    )



st.divider()



st.success(
    "✅ CyberGuardian AI SOC Dashboard Running Successfully"
)