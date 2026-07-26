import joblib
import pandas as pd
from utils.email_alert import send_email_alert

from utils.risk_engine import (
    calculate_risk_score,
    get_threat_level
)


from utils.recommendation_engine import (
    generate_recommendation
)


from utils.threat_intelligence import (
    get_threat_intelligence
)


from utils.mitre_mapping import (
    get_mitre_mapping
)


from engine.root_cause import (
    analyze_root_cause
)


from engine.incident_report import (
    generate_incident_report
)


from engine.report_storage import (
    save_report
)


from database.database import (
    save_incident
)



# --------------------------------------------------
# Load Models
# --------------------------------------------------

anomaly_model = joblib.load(
    "models/anomaly_model.pkl"
)


attack_model = joblib.load(
    "models/attack_classifier.pkl"
)


encoder = joblib.load(
    "models/attack_label_encoder.pkl"
)



# --------------------------------------------------
# Prediction Function
# --------------------------------------------------

def predict_event(file_path):


    # Load event

    event = pd.read_csv(file_path)



    sample = event.drop(
        columns=[
            "attack_type",
            "label",
            "target"
        ],
        errors="ignore"
    )



    # Align features

    features = anomaly_model.feature_names_in_


    for feature in features:

        if feature not in sample.columns:

            sample[feature] = 0



    sample = sample[features]



    # Anomaly prediction

    anomaly = anomaly_model.predict(sample)


    anomaly_score = anomaly_model.decision_function(sample)[0]



    result = {}



    # ==================================================
    # ANOMALY DETECTED
    # ==================================================

    if anomaly[0] == -1:


        result["status"] = "ANOMALY DETECTED"



        attack_prediction = attack_model.predict(sample)



        attack_name = encoder.inverse_transform(
            attack_prediction
        )[0]



        # --------------------------------------
        # Convert dataset normal label
        # --------------------------------------

        if attack_name == "Unknown":

            attack_name = "Normal"



        result["attack_type"] = attack_name



        # Risk Score

        risk = calculate_risk_score(
            anomaly_score,
            event,
            attack_name
        )


        result["risk_score"] = float(risk)



        # Threat Level

        result["threat_level"] = get_threat_level(
            risk
        )



        # Recommendations

        result["recommendations"] = generate_recommendation(
            attack_name,
            result["threat_level"]
        )



        # Root Cause

        result["root_causes"] = analyze_root_cause(
            event,
            attack_name
        )



        # Threat Intelligence

        result["threat_intelligence"] = get_threat_intelligence(
            attack_name
        )



        # MITRE ATT&CK

        result["mitre_attack"] = get_mitre_mapping(
            attack_name
        )
        # Send Email Alert for High Risk Threats

        send_email_alert(
            attack_name,
            result["risk_score"],
            result["threat_level"],
            result["mitre_attack"]
        )



    # ==================================================
    # NORMAL EVENT
    # ==================================================

    else:


        result["status"] = "NORMAL"


        result["attack_type"] = "Normal"



        risk = calculate_risk_score(
            anomaly_score,
            event
        )


        result["risk_score"] = float(risk)



        result["threat_level"] = "LOW"



        result["recommendations"] = [
            "Continue monitoring."
        ]



        result["root_causes"] = [
            "No suspicious behavior detected."
        ]



        result["threat_intelligence"] = get_threat_intelligence(
            "Normal"
        )



        result["mitre_attack"] = get_mitre_mapping(
            "Normal"
        )



    # ==================================================
    # Incident Report Generation
    # ==================================================


    report = generate_incident_report(
        result
    )



    # Save JSON Report

    save_report(
        report
    )



    # Save Database Record

    save_incident(
        report
    )



    result["incident_report"] = report



    return result