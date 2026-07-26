"""
CyberGuardian AI
MITRE ATT&CK Mapping Module
"""


MITRE_ATTACK = {

    "Brute Force": {
        "technique_id": "T1110",
        "technique": "Brute Force",
        "tactic": "Credential Access"
    },


    "Credential Stuffing": {
        "technique_id": "T1078",
        "technique": "Valid Accounts",
        "tactic": "Defense Evasion"
    },


    "Impossible Travel": {
        "technique_id": "T1021",
        "technique": "Remote Services",
        "tactic": "Lateral Movement"
    },


    "Lateral Movement": {
        "technique_id": "T1021",
        "technique": "Remote Services",
        "tactic": "Lateral Movement"
    },


    "Device Spoofing": {
        "technique_id": "T1036",
        "technique": "Masquerading",
        "tactic": "Defense Evasion"
    },


    "Low and Slow": {
        "technique_id": "T1071",
        "technique": "Application Layer Protocol",
        "tactic": "Command and Control"
    },


    "Insider Drift": {
        "technique_id": "T1087",
        "technique": "Account Discovery",
        "tactic": "Discovery"
    },


    # Normal traffic
    "Normal": {
        "technique_id": "-",
        "technique": "None",
        "tactic": "None"
    },


    # Dataset uses Unknown for normal traffic
    "Unknown": {
        "technique_id": "-",
        "technique": "None",
        "tactic": "None"
    }

}



def get_mitre_mapping(attack_type):

    return MITRE_ATTACK.get(
        attack_type,
        {
            "technique_id": "Unknown",
            "technique": "Unknown",
            "tactic": "Unknown"
        }
    )