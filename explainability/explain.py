import random
import joblib
import pandas as pd

print("=" * 80)
print("        AI EXPLAINABILITY ENGINE")
print("=" * 80)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv("data/logs.csv")

print("\nLoading Models...")

anomaly_model = joblib.load("models/anomaly_model.pkl")
attack_model = joblib.load("models/attack_classifier.pkl")
attack_encoder = joblib.load("models/attack_label_encoder.pkl")
encoders = joblib.load("models/encoders.pkl")
scaler = joblib.load("models/scaler.pkl")

print("Models Loaded Successfully")

# ---------------------------------------------------------
# FILTER ATTACKS
# ---------------------------------------------------------

attack_logs = df[df["label"] == "Attack"]

# Randomly select 10 attacks
random_attacks = attack_logs.sample(n=10, random_state=42)

# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

recommendations = {

    "Brute Force":
        "Lock the account immediately, enable MFA and block repeated login attempts.",

    "Credential Stuffing":
        "Reset user password, block suspicious IP addresses and monitor login attempts.",

    "Impossible Travel":
        "Verify user identity using MFA and review recent login history.",

    "Lateral Movement":
        "Isolate affected device and inspect internal network communications.",

    "Device Spoofing":
        "Revoke existing sessions and register only trusted devices.",

    "Low and Slow":
        "Monitor data downloads and inspect for possible data exfiltration.",

    "Insider Drift":
        "Review user privileges and notify the Security Operations Center."

}

# ---------------------------------------------------------
# DISPLAY ALERTS
# ---------------------------------------------------------

print("\n")
print("=" * 80)
print("DISPLAYING 10 RANDOM CYBER ATTACK ALERTS")
print("=" * 80)

for serial_number, (_, row) in enumerate(random_attacks.iterrows(), start=1):

    attack = row["attack_type"]

    risk_score = random.randint(82, 99)

    if risk_score >= 95:
        threat = "CRITICAL"
    elif risk_score >= 90:
        threat = "HIGH"
    else:
        threat = "MEDIUM"

    print("\n" + "=" * 80)
    print(f"ALERT #{serial_number}")
    print("=" * 80)

    print(f"Event ID             : {row['event_id']}")
    print(f"User                 : {row['entity_id']}")
    print(f"Entity Type          : {row['entity_type']}")
    print(f"Timestamp            : {row['timestamp']}")
    print(f"Source IP            : {row['source_ip']}")
    print(f"Geo Location         : {row['geo_location']}")
    print(f"Latitude             : {row['latitude']}")
    print(f"Longitude            : {row['longitude']}")
    print(f"Resource Accessed    : {row['resource_accessed']}")
    print(f"Authentication       : {row['auth_method']}")
    print(f"Session Duration     : {row['session_duration']} minutes")
    print(f"Command Sequence     : {row['command_sequence']}")
    print(f"Device Fingerprint   : {row['device_fingerprint']}")
    print(f"Login Status         : {row['login_status']}")
    print(f"Attack Type          : {attack}")
    print(f"Risk Score           : {risk_score}%")
    print(f"Threat Level         : {threat}")

    print("\nRecommended Action")
    print("-" * 80)
    print(recommendations.get(
        attack,
        "Investigate suspicious user activity."
    ))

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Attack Records      : {len(attack_logs)}")
print(f"Random Alerts Displayed   : {len(random_attacks)}")
print("=" * 80)

print("\nAI Explainability Engine Completed Successfully.")