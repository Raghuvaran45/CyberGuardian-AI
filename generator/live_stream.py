import os
import sys
import time
import random
import pandas as pd


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from engine.prediction_engine import predict_event


print("=" * 60)
print("CyberGuardian AI Real-Time Threat Stream Started")
print("=" * 60)


# Load dataset

df = pd.read_csv(
    "data/processed_logs.csv"
)


normal_rows = df[
    df["attack_type"] == "Unknown"
]


attack_rows = df[
    df["attack_type"] != "Unknown"
]


while True:


    # Generate event

    if random.random() < 0.7:

        sample = normal_rows.sample(1)

    else:

        sample = attack_rows.sample(1)



    print("\nSelected Event:")

    print(
        sample[["attack_type"]]
    )



    # Remove labels

    live_event = sample.drop(
        columns=[
            "attack_type",
            "label",
            "target"
        ],
        errors="ignore"
    )



    # Save current event

    live_event.to_csv(
        "data/live_event.csv",
        index=False
    )



    # Prediction

    result = predict_event(
        "data/live_event.csv"
    )



    print("-"*50)

    print(
        "Status:",
        result["status"]
    )


    print(
        "Attack:",
        result["attack_type"]
    )


    print(
        "Risk:",
        result["risk_score"]
    )


    print(
        "Threat:",
        result["threat_level"]
    )


    print("-"*50)



    # Wait before next event

    time.sleep(10)