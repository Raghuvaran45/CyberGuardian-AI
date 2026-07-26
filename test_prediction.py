from engine.prediction_engine import predict_event
from engine.incident_report import display_incident_report


result = predict_event(
    "data/live_event.csv"
)


print("\n==============================")
print("CYBERGUARDIAN AI RESULT")
print("==============================")


print("\nStatus:")
print(result["status"])


print("\nAttack Type:")
print(result["attack_type"])


print("\nRisk Score:")
print(result["risk_score"])


print("\nThreat Level:")
print(result["threat_level"])


print("\nMITRE ATT&CK")
print("------------------------------")

mitre = result["mitre_attack"]

print("Technique ID :", mitre["technique_id"])
print("Technique    :", mitre["technique"])
print("Tactic       :", mitre["tactic"])



print("\nIncident Report")

display_incident_report(
    result["incident_report"]
)