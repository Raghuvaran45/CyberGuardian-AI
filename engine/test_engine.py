from engine.prediction_engine import predict_event

# Predict the event
result = predict_event("data/live_event.csv")

print("=" * 70)
print("          CYBERGUARDIAN AI - INCIDENT REPORT")
print("=" * 70)

print(f"Status           : {result['status']}")
print(f"Attack Type      : {result['attack_type']}")
print(f"Risk Score       : {result['risk_score']:.2f}")
print(f"Threat Level     : {result['threat_level']}")

print("\n" + "=" * 70)
print("ROOT CAUSE ANALYSIS")
print("=" * 70)

for i, cause in enumerate(result["root_causes"], start=1):
    print(f"{i}. {cause}")

print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

for i, rec in enumerate(result["recommendations"], start=1):
    print(f"{i}. {rec}")

print("\n" + "=" * 70)
print("INCIDENT REPORT")
print("=" * 70)

report = result["incident_report"]

print(f"Timestamp        : {report['timestamp']}")
print(f"Status           : {report['status']}")
print(f"Attack Type      : {report['attack_type']}")
print(f"Risk Score       : {report['risk_score']:.2f}")
print(f"Threat Level     : {report['threat_level']}")

print("\nRoot Causes:")
for i, cause in enumerate(report["root_causes"], start=1):
    print(f"  {i}. {cause}")

print("\nRecommendations:")
for i, rec in enumerate(report["recommendations"], start=1):
    print(f"  {i}. {rec}")

print("\n" + "=" * 70)
print("Report successfully saved in the 'reports' folder.")
print("=" * 70)