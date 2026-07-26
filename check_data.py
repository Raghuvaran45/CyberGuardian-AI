import pandas as pd

df = pd.read_csv("data/processed_logs.csv")

print(df["attack_type"].unique())

print("\nCounts:")
print(df["attack_type"].value_counts())