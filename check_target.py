import pandas as pd

df = pd.read_csv(
    "data/processed_logs.csv"
)

print(df["target"].value_counts())

print("\nAttack Types:")
print(
    df[df["target"] == 1]["attack_type"].value_counts()
)