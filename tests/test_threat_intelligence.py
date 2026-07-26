from utils.threat_intelligence import get_threat_intelligence

attack = "Credential Theft"

info = get_threat_intelligence(attack)

print("=" * 60)
print("THREAT INTELLIGENCE")
print("=" * 60)

print("Attack :", attack)
print("Severity :", info["severity"])
print("Description :", info["description"])

print("\nIndicators of Compromise")

for i in info["ioc"]:
    print("-", i)

print("\nImpact")
print(info["impact"])