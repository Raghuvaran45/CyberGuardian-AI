import random
import pandas as pd
import time

OUTPUT_FILE = "data/live_event.csv"

attack_types = [
    "Brute Force",
    "Credential Stuffing",
    "Impossible Travel",
    "Low and Slow",
    "Device Spoofing",
    "Lateral Movement",
    "Normal"
]

while True:

    attack = random.choice(attack_types)

    if attack == "Brute Force":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 0,
            "office_hours": 1,
            "long_session": 0,
            "failed_attempts": random.randint(20,60)
        }

    elif attack == "Credential Stuffing":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 1,
            "office_hours": 0,
            "long_session": 0,
            "failed_attempts": random.randint(10,25)
        }

    elif attack == "Impossible Travel":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 0,
            "office_hours": 1,
            "long_session": 0,
            "failed_attempts": 0
        }

    elif attack == "Low and Slow":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 1,
            "office_hours": 0,
            "long_session": 1,
            "failed_attempts": 2
        }

    elif attack == "Device Spoofing":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 0,
            "office_hours": 1,
            "long_session": 0,
            "failed_attempts": 1
        }

    elif attack == "Lateral Movement":

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 1,
            "office_hours": 0,
            "long_session": 1,
            "failed_attempts": 5
        }

    else:

        event = {
            "entity_id": random.randint(100,150),
            "night_login": 0,
            "office_hours": 1,
            "long_session": 0,
            "failed_attempts": 0
        }

    df = pd.DataFrame([event])

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Generated Event: {attack}")

    time.sleep(10)