from utils.mitre_mapping import get_mitre_mapping

attack = "Credential Theft"

mapping = get_mitre_mapping(attack)

print("=" * 60)
print("MITRE ATT&CK MAPPING")
print("=" * 60)

print("Attack :", attack)
print("Technique ID :", mapping["technique_id"])
print("Technique :", mapping["technique"])
print("Tactic :", mapping["tactic"])