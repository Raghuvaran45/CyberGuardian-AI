import os
import sys
import time
import random
import pandas as pd


# --------------------------------------------------
# Project Path Setup
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)



from engine.prediction_engine import predict_event



# --------------------------------------------------
# Simulator Start
# --------------------------------------------------

print("=" * 60)
print("CyberGuardian AI Live Simulator Started")
print("=" * 60)



# --------------------------------------------------
# Load Dataset Once
# --------------------------------------------------

df = pd.read_csv(
    "data/processed_logs.csv"
)



# --------------------------------------------------
# Live Simulation Loop
# --------------------------------------------------

while True:


    # ----------------------------------------------
    # Separate Normal and Attack Events
    # ----------------------------------------------

    # Dataset normal traffic label = Unknown

    normal_rows = df[
        df["attack_type"] == "Unknown"
    ]


    attack_rows = df[
        df["attack_type"] != "Unknown"
    ]



    # ----------------------------------------------
    # Generate Live Event
    # 70% Normal
    # 30% Attack
    # ----------------------------------------------

    if random.random() < 0.7:

        sample = normal_rows.sample(1)

    else:

        sample = attack_rows.sample(1)

        
    print("\nSelected dataset row:")
    print(sample[["attack_type"]])



    # ----------------------------------------------
    # Remove Training Labels
    # ----------------------------------------------

    live_event = sample.drop(
        columns=[
            "attack_type",
            "label",
            "target"
        ],
        errors="ignore"
    )



    # Save live event

    live_event.to_csv(
        "data/live_event.csv",
        index=False
    )



    # ----------------------------------------------
    # Run Prediction Engine
    # ----------------------------------------------

    result = predict_event(
        "data/live_event.csv"
    )



    # ----------------------------------------------
    # Display Prediction
    # ----------------------------------------------

    print("-" * 50)


    print(
        "Status      :",
        result["status"]
    )


    print(
        "Attack Type :",
        result["attack_type"]
    )


    print(
        "Risk Score  :",
        round(
            result["risk_score"],
            2
        )
    )


    print(
        "Threat      :",
        result["threat_level"]
    )



    # ----------------------------------------------
    # Display Incident Report
    # Only for Attacks
    # ----------------------------------------------

    if result["status"] == "ANOMALY DETECTED":


        report = result["incident_report"]



        print("\n========== INCIDENT REPORT ==========")



        print(
            "Timestamp :",
            report["timestamp"]
        )



        print(
            "Attack Type :",
            report["attack_type"]
        )



        print(
            "Risk Score :",
            report["risk_score"]
        )



        # -------------------------------
        # MITRE ATT&CK
        # -------------------------------

        print(
            "\nMITRE ATT&CK Mapping"
        )


        print(
            "Technique ID :",
            report["mitre_attack"]["technique_id"]
        )


        print(
            "Technique    :",
            report["mitre_attack"]["technique"]
        )


        print(
            "Tactic       :",
            report["mitre_attack"]["tactic"]
        )



        # -------------------------------
        # Root Cause Analysis
        # -------------------------------

        print(
            "\nRoot Causes:"
        )


        for cause in report["root_causes"]:

            print(
                "-",
                cause
            )



        # -------------------------------
        # Recommendations
        # -------------------------------

        print(
            "\nRecommendations:"
        )


        for recommendation in report["recommendations"]:

            print(
                "-",
                recommendation
            )



        print(
            "=" * 50
        )



    # ----------------------------------------------
    # Wait before next event
    # ----------------------------------------------

    time.sleep(10)