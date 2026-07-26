import pandas as pd

df = pd.read_csv("data/logs.csv")

print(df["attack_type"].value_counts())