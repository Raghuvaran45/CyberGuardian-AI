def get_threat_intelligence(attack_type):
    

    threat_database = {


        "Brute Force": {

            "severity": "HIGH",

            "category": "Credential Attack",

            "description":
            "Multiple failed login attempts detected. "
            "The attacker may be attempting to guess valid credentials.",

            "impact":
            "Unauthorized account access and possible account compromise.",

            "ioc": [
                "Multiple authentication failures",
                "Repeated login attempts",
                "Suspicious source IP activity"
            ]

        },


        "Credential Stuffing": {

            "severity": "HIGH",

            "category": "Credential Attack",

            "description":
            "Previously leaked username and password combinations "
            "are being tested against accounts.",

            "impact":
            "Account takeover and unauthorized access.",

            "ioc": [
                "Repeated login failures",
                "Unknown login locations",
                "Multiple account access attempts"
            ]

        },


        "Impossible Travel": {

            "severity": "MEDIUM",

            "category": "Identity Threat",

            "description":
            "User login activity detected from geographically "
            "impossible locations within a short time period.",

            "impact":
            "Possible stolen credentials or compromised account.",

            "ioc": [
                "Unusual geographic location",
                "Rapid location change",
                "Suspicious authentication pattern"
            ]

        },


        "Lateral Movement": {

            "severity": "HIGH",

            "category": "Network Attack",

            "description":
            "Suspicious internal movement detected between systems.",

            "impact":
            "Attackers may gain access to sensitive resources.",

            "ioc": [
                "Internal communication anomalies",
                "Unexpected remote access",
                "Abnormal resource access"
            ]

        },


        "Device Spoofing": {

            "severity": "MEDIUM",

            "category": "Device Security",

            "description":
            "A device identity mismatch was detected.",

            "impact":
            "Unauthorized device access.",

            "ioc": [
                "Unknown device fingerprint",
                "Changed device identity",
                "Suspicious authentication"
            ]

        },


        "Low and Slow": {

            "severity": "MEDIUM",

            "category": "Stealth Attack",

            "description":
            "Slow suspicious activity pattern detected over time.",

            "impact":
            "Possible data theft or hidden malicious activity.",

            "ioc": [
                "Long duration activity",
                "Low frequency requests",
                "Unusual access patterns"
            ]

        },


        "Normal": {

            "severity": "LOW",

            "category": "Normal Activity",

            "description":
            "No malicious behavior detected.",

            "impact":
            "No security impact identified.",

            "ioc": []

        }


    }



    return threat_database.get(

        attack_type,

        {

            "severity": "UNKNOWN",

            "category": "Unknown",

            "description":
            "No threat intelligence available.",

            "impact":
            "Unknown",

            "ioc": []

        }

    )