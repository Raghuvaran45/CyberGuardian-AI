from engine.incident_report import generate_incident_report

sample_result = {

    "status": "ANOMALY DETECTED",

    "attack_type": "Credential Theft",

    "risk_score": 91.4,

    "threat_level": "CRITICAL",

    "root_causes": [

        "Night Login",

        "Unknown Device",

        "Multiple Failed Login Attempts"

    ],

    "recommendations": [

        "Reset Password",

        "Enable MFA",

        "Monitor User Activity"

    ]
}

report = generate_incident_report(sample_result)

print("=" * 60)
print("INCIDENT REPORT")
print("=" * 60)

for key, value in report.items():

    print(f"{key} : {value}")