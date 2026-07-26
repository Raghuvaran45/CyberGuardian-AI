import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)




import joblib
import pandas as pd

from utils.risk_engine import (
    calculate_risk_score,
    get_threat_level
)

from utils.recommendation_engine import (
    generate_recommendation
)



# ===============================
# LOAD MODELS
# ===============================

anomaly_model = joblib.load(
    "models/anomaly_model.pkl"
)

attack_model = joblib.load(
    "models/attack_classifier.pkl"
)

encoder = joblib.load(
    "models/attack_label_encoder.pkl"
)

encoders = joblib.load(
    "models/encoders.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)



print("=" * 60)
print("CYBERGUARDIAN AI - REAL TIME PREDICTION")
print("=" * 60)



# ===============================
# LOAD LIVE EVENT
# ===============================

sample = pd.read_csv(
    "data/live_event.csv"
)



print("\nIncoming Event\n")

print(sample)



# ===============================
# REMOVE TARGET COLUMNS
# ===============================

remove_columns = [

    "attack_type",
    "label",
    "target"

]


sample_input = sample.drop(
    columns=remove_columns,
    errors="ignore"
)



# ===============================
# FEATURE ALIGNMENT
# ===============================

expected_features = (
    anomaly_model.feature_names_in_
)



for feature in expected_features:


    if feature not in sample_input.columns:

        sample_input[feature] = 0



sample_input = sample_input[
    expected_features
]



# ===============================
# ANOMALY DETECTION
# ===============================

anomaly = anomaly_model.predict(
    sample_input
)


anomaly_score = anomaly_model.decision_function(
    sample_input
)[0]



# ===============================
# PROCESS RESULT
# ===============================


if anomaly[0] == -1:


    print("\n⚠️ ANOMALY DETECTED")



    # Attack Prediction

    attack = attack_model.predict(
        sample_input
    )


    attack_name = encoder.inverse_transform(
        attack
    )[0]



    # Risk Calculation

    risk_score = calculate_risk_score(

        anomaly_score,

        sample,

        attack_name

    )



    threat_level = get_threat_level(
        risk_score
    )



    print("\nAttack Type :",
          attack_name)



    print(
        "Risk Score :",
        risk_score,
        "/100"
    )


    print(
        "Threat Level :",
        threat_level
    )



    # Recommendation Engine

    recommendations = generate_recommendation(

        attack_name,

        threat_level

    )



    print("\nAI Recommended Actions:")



    for item in recommendations:

        print("-", item)



else:


    print("\n✅ NORMAL USER BEHAVIOUR")



    risk_score = calculate_risk_score(

        anomaly_score,

        sample

    )



    print(
        "\nRisk Score :",
        risk_score,
        "/100"
    )


    print(
        "Threat Level : LOW"
    )



    print(
        "\nAI Recommendation:"
    )


    print(
        "- Continue monitoring"
    )