def calculate_risk_score(
        anomaly_score,
        event,
        attack_type=None
):

    risk_score = 0


    # -----------------------------------------
    # ML anomaly contribution
    # -----------------------------------------

    anomaly_risk = abs(anomaly_score) * 50

    risk_score += anomaly_risk



    # -----------------------------------------
    # Suspicious behaviour indicators
    # -----------------------------------------

    if "night_login" in event.columns:

        if event["night_login"].iloc[0] == 1:
            risk_score += 15



    if "long_session" in event.columns:

        if event["long_session"].iloc[0] == 1:
            risk_score += 15



    # -----------------------------------------
    # Device behaviour
    # -----------------------------------------

    if "device_fingerprint" in event.columns:

        risk_score += 10



    # -----------------------------------------
    # Attack Severity Mapping
    # -----------------------------------------

    high_risk_attacks = [

        "Brute Force",
        "Credential Stuffing",
        "Device Spoofing",
        "Lateral Movement"

    ]


    medium_risk_attacks = [

        "Insider Drift",
        "Impossible Travel",
        "Low and Slow"

    ]



    if attack_type in high_risk_attacks:

        risk_score += 35



    elif attack_type in medium_risk_attacks:

        risk_score += 25



    # -----------------------------------------
    # Minimum risk for detected attacks
    # -----------------------------------------

    if attack_type and attack_type != "Normal":

        if risk_score < 40:

            risk_score = 40



    # Maximum limit

    if risk_score > 100:

        risk_score = 100



    return round(risk_score,2)





def get_threat_level(score):


    if score >= 70:

        return "HIGH"



    elif score >= 40:

        return "MEDIUM"



    else:

        return "LOW"