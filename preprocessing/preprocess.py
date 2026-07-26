import os
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("PREPROCESSING DATASET")
print("=" * 60)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv("data/logs.csv")

print("Dataset Loaded Successfully")
print(df.shape)

# -------------------------------------------------
# HANDLE MISSING VALUES
# -------------------------------------------------

df.fillna("Unknown", inplace=True)

# -------------------------------------------------
# TARGET COLUMN
# -------------------------------------------------

df["target"] = df["label"].map({
    "Normal": 0,
    "Attack": 1
})

# -------------------------------------------------
# TIMESTAMP FEATURES
# -------------------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute
df["weekday"] = df["timestamp"].dt.weekday

# -------------------------------------------------
# BEHAVIOURAL FEATURES
# -------------------------------------------------

df["office_hours"] = df["hour"].between(8, 18).astype(int)

df["night_login"] = (~df["hour"].between(8, 18)).astype(int)

df["long_session"] = (df["session_duration"] > 120).astype(int)

df["short_session"] = (df["session_duration"] < 5).astype(int)

# -------------------------------------------------
# DROP UNUSED COLUMNS
# -------------------------------------------------

df.drop(columns=["timestamp", "event_id"], inplace=True)

# -------------------------------------------------
# LABEL ENCODING
# -------------------------------------------------

categorical_columns = [

    "entity_id",
    "entity_type",
    "source_ip",
    "geo_location",
    "resource_accessed",
    "auth_method",
    "command_sequence",
    "device_fingerprint",
    "login_status"

]

encoders = {}

for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder

# -------------------------------------------------
# SCALE NUMERIC FEATURES
# -------------------------------------------------

numerical_columns = [

    "latitude",
    "longitude",
    "session_duration",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "weekday"

]

scaler = StandardScaler()

df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# -------------------------------------------------
# CREATE MODEL DIRECTORY
# -------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(encoders, "models/encoders.pkl")

joblib.dump(scaler, "models/scaler.pkl")

# -------------------------------------------------
# SAVE DATASET
# -------------------------------------------------

df.to_csv("data/processed_logs.csv", index=False)

print("=" * 60)
print("PREPROCESSING COMPLETED")
print("=" * 60)

print(df.head())

print()

print("Processed Dataset Saved Successfully")

print("Location : data/processed_logs.csv")

print("Final Dataset Shape :", df.shape)

print("=" * 60)