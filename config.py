import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

MODEL_DIR = os.path.join(BASE_DIR, "models", "saved_models")

REPORT_DIR = os.path.join(BASE_DIR, "reports")

RANDOM_STATE = 42

TOTAL_RECORDS = 100000

ANOMALY_RATE = 0.03