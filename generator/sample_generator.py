import pandas as pd

# Load processed dataset
df = pd.read_csv("data/processed_logs.csv")

# Select a random ATTACK row
sample = df[df["target"] == 1].sample(1)

# Print what was selected
print("\nSelected Event")
print(sample[["attack_type", "label", "target"]])

# Remove columns not used for prediction
live_event = sample.drop(
    columns=[
        "attack_type",
        "label",
        "target"
    ],
    errors="ignore"
)

# Save for prediction
live_event.to_csv(
    "data/live_event.csv",
    index=False
)

print("\nLive event generated successfully.")