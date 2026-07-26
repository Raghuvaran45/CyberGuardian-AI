from engine.report_storage import save_report

sample_report = {

    "timestamp": "2026-07-25 15:45:00",

    "status": "ANOMALY DETECTED",

    "attack_type": "Credential Theft",

    "risk_score": 91.4,

    "threat_level": "CRITICAL",

    "root_causes": [

        "Night Login",

        "Unknown Device"

    ],

    "recommendations": [

        "Reset Password",

        "Enable MFA"

    ]
}

path = save_report(sample_report)

print("=" * 60)
print("REPORT SAVED SUCCESSFULLY")
print("=" * 60)
print(path)