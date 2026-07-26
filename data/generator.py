import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid
import os

fake = Faker()

# -----------------------------
# CONFIGURATION
# -----------------------------

TOTAL_RECORDS = 100000
ANOMALY_PERCENTAGE = 0.03

NORMAL_RECORDS = int(TOTAL_RECORDS * (1 - ANOMALY_PERCENTAGE))
ATTACK_RECORDS = TOTAL_RECORDS - NORMAL_RECORDS

OUTPUT_FILE = "logs.csv"

random.seed(42)
np.random.seed(42)

# -----------------------------
# USERS
# -----------------------------

USERS = [f"USER_{i:03d}" for i in range(1,201)]

ENTITY_TYPES = [
    "user",
    "service_account",
    "edge_device"
]

AUTH_METHODS = [
    "Password",
    "MFA",
    "Token",
    "Certificate",
    "Biometric"
]

LOGIN_STATUS = [
    "Success",
    "Failure"
]

# -----------------------------
# LOCATIONS
# -----------------------------

LOCATIONS = {

    "Bangalore":(12.9716,77.5946),
    "Hyderabad":(17.3850,78.4867),
    "Chennai":(13.0827,80.2707),
    "Mumbai":(19.0760,72.8777),
    "Delhi":(28.7041,77.1025),
    "Pune":(18.5204,73.8567),
    "Singapore":(1.3521,103.8198),
    "Tokyo":(35.6762,139.6503),
    "London":(51.5072,-0.1276),
    "New York":(40.7128,-74.0060)

}

# -----------------------------
# RESOURCES
# -----------------------------

RESOURCES = [

    "Payroll_DB",
    "HR_Portal",
    "Finance_Server",
    "Employee_API",
    "Sales_Dashboard",
    "Engineering_Git",
    "Production_Server",
    "Email_Server",
    "CRM",
    "VPN"

]

# -----------------------------
# COMMAND SEQUENCES
# -----------------------------

COMMANDS = [

    "login->query->logout",

    "login->download->logout",

    "login->update->logout",

    "login->view->logout",

    "login->api->logout"

]

# -----------------------------
# DEVICE FINGERPRINTS
# -----------------------------

DEVICES = [

    "Windows11_HP",
    "Windows11_Dell",
    "Ubuntu22_Lenovo",
    "MacOS_M2",
    "Windows10_HP",
    "Android_Device",
    "iPhone16"

]

# -----------------------------
# USER PROFILES
# -----------------------------

user_profiles = {}

for user in USERS:

    city = random.choice(list(LOCATIONS.keys()))

    profile = {

        "home_city":city,

        "device":random.choice(DEVICES),

        "resource":random.choice(RESOURCES),

        "auth":random.choice(AUTH_METHODS),

        "login_hour":random.randint(8,10),

        "session":random.randint(15,90)

    }

    user_profiles[user] = profile

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def random_ip():

    return fake.ipv4_public()

def random_timestamp():

    start = datetime(2026,1,1)

    end = datetime(2026,12,31)

    delta = end-start

    seconds = random.randint(0,int(delta.total_seconds()))

    return start + timedelta(seconds=seconds)

def generate_session():

    return random.randint(5,180)

def generate_uuid():

    return str(uuid.uuid4())[:8]
# -----------------------------
# NORMAL LOG GENERATION
# -----------------------------

def generate_normal_log(user):

    profile = user_profiles[user]

    timestamp = random_timestamp()

    login_hour = max(0, min(23, profile["login_hour"] + random.randint(-1, 1)))

    timestamp = timestamp.replace(
        hour=login_hour,
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

    city = profile["home_city"]

    record = {

        "event_id": generate_uuid(),

        "entity_id": user,

        "entity_type": random.choice(ENTITY_TYPES),

        "timestamp": timestamp,

        "source_ip": random_ip(),

        "geo_location": city,

        "latitude": LOCATIONS[city][0],

        "longitude": LOCATIONS[city][1],

        "resource_accessed": profile["resource"],

        "auth_method": profile["auth"],

        "session_duration": max(
            5,
            int(np.random.normal(profile["session"], 10))
        ),

        "command_sequence": random.choice(COMMANDS),

        "device_fingerprint": profile["device"],

        "login_status": "Success",

        "label": "Normal",

        "attack_type": "None"

    }

    return record
# -----------------------------
# CREATE NORMAL DATASET
# -----------------------------

logs = []

print("Generating normal behaviour...")

for i in range(NORMAL_RECORDS):

    user = random.choice(USERS)

    logs.append(generate_normal_log(user))

    if (i + 1) % 10000 == 0:
        print(f"{i+1} normal logs generated...")
# -----------------------------
# BRUTE FORCE ATTACK
# -----------------------------

def generate_brute_force():

    user = random.choice(USERS)
    profile = user_profiles[user]

    timestamp = random_timestamp()

    return {
        "event_id": generate_uuid(),
        "entity_id": user,
        "entity_type": "user",
        "timestamp": timestamp,
        "source_ip": random_ip(),
        "geo_location": profile["home_city"],
        "latitude": LOCATIONS[profile["home_city"]][0],
        "longitude": LOCATIONS[profile["home_city"]][1],
        "resource_accessed": profile["resource"],
        "auth_method": "Password",
        "session_duration": 1,
        "command_sequence": "login",
        "device_fingerprint": profile["device"],
        "login_status": "Failure",
        "label": "Attack",
        "attack_type": "Brute Force"
    }
# -----------------------------
# IMPOSSIBLE TRAVEL
# -----------------------------

def generate_impossible_travel():

    user = random.choice(USERS)

    city = random.choice(["London","Tokyo","Singapore","New York"])

    timestamp = random_timestamp()

    return {

        "event_id": generate_uuid(),
        "entity_id": user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":random_ip(),
        "geo_location":city,
        "latitude":LOCATIONS[city][0],
        "longitude":LOCATIONS[city][1],
        "resource_accessed":"VPN",
        "auth_method":"Password",
        "session_duration":20,
        "command_sequence":"login->vpn",
        "device_fingerprint":"Unknown_Device",
        "login_status":"Success",
        "label":"Attack",
        "attack_type":"Impossible Travel"

    }
# -----------------------------
# CREDENTIAL STUFFING
# -----------------------------

def generate_credential_stuffing():

    user = random.choice(USERS)

    timestamp = random_timestamp()

    return {

        "event_id":generate_uuid(),
        "entity_id":user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":"185.92.11."+str(random.randint(1,255)),
        "geo_location":"Unknown",
        "latitude":0,
        "longitude":0,
        "resource_accessed":"Login Portal",
        "auth_method":"Password",
        "session_duration":1,
        "command_sequence":"login",
        "device_fingerprint":"Bot_Device",
        "login_status":"Failure",
        "label":"Attack",
        "attack_type":"Credential Stuffing"

    }
# -----------------------------
# LATERAL MOVEMENT
# -----------------------------

def generate_lateral():

    user=random.choice(USERS)

    timestamp=random_timestamp()

    return{

        "event_id":generate_uuid(),
        "entity_id":user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":random_ip(),
        "geo_location":user_profiles[user]["home_city"],
        "latitude":LOCATIONS[user_profiles[user]["home_city"]][0],
        "longitude":LOCATIONS[user_profiles[user]["home_city"]][1],
        "resource_accessed":"Production_Server",
        "auth_method":"Token",
        "session_duration":140,
        "command_sequence":"login->server->finance->git->logout",
        "device_fingerprint":user_profiles[user]["device"],
        "login_status":"Success",
        "label":"Attack",
        "attack_type":"Lateral Movement"

    }
# -----------------------------
# DEVICE SPOOFING
# -----------------------------

def generate_device_spoof():

    user=random.choice(USERS)

    timestamp=random_timestamp()

    return{

        "event_id":generate_uuid(),
        "entity_id":user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":random_ip(),
        "geo_location":user_profiles[user]["home_city"],
        "latitude":LOCATIONS[user_profiles[user]["home_city"]][0],
        "longitude":LOCATIONS[user_profiles[user]["home_city"]][1],
        "resource_accessed":user_profiles[user]["resource"],
        "auth_method":"Password",
        "session_duration":25,
        "command_sequence":"login",
        "device_fingerprint":"Spoofed_Device",
        "login_status":"Success",
        "label":"Attack",
        "attack_type":"Device Spoofing"

    }
# -----------------------------
# LOW AND SLOW EXFILTRATION
# -----------------------------

def generate_low_slow():

    user=random.choice(USERS)

    timestamp=random_timestamp()

    return{

        "event_id":generate_uuid(),
        "entity_id":user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":random_ip(),
        "geo_location":user_profiles[user]["home_city"],
        "latitude":LOCATIONS[user_profiles[user]["home_city"]][0],
        "longitude":LOCATIONS[user_profiles[user]["home_city"]][1],
        "resource_accessed":"Payroll_DB",
        "auth_method":"MFA",
        "session_duration":180,
        "command_sequence":"login->download->download->download->logout",
        "device_fingerprint":user_profiles[user]["device"],
        "login_status":"Success",
        "label":"Attack",
        "attack_type":"Low and Slow"

    }
# -----------------------------
# INSIDER DRIFT
# -----------------------------

def generate_insider():

    user=random.choice(USERS)

    timestamp=random_timestamp()

    return{

        "event_id":generate_uuid(),
        "entity_id":user,
        "entity_type":"user",
        "timestamp":timestamp,
        "source_ip":random_ip(),
        "geo_location":user_profiles[user]["home_city"],
        "latitude":LOCATIONS[user_profiles[user]["home_city"]][0],
        "longitude":LOCATIONS[user_profiles[user]["home_city"]][1],
        "resource_accessed":"Finance_Server",
        "auth_method":"MFA",
        "session_duration":120,
        "command_sequence":"login->finance->hr->git->logout",
        "device_fingerprint":user_profiles[user]["device"],
        "login_status":"Success",
        "label":"Attack",
        "attack_type":"Insider Drift"

    }
# -----------------------------
# GENERATE ATTACK RECORDS
# -----------------------------

print("Generating attack behaviour...")

ATTACK_GENERATORS = [
    generate_brute_force,
    generate_impossible_travel,
    generate_credential_stuffing,
    generate_lateral,
    generate_device_spoof,
    generate_low_slow,
    generate_insider
]

attack_logs = []

for i in range(ATTACK_RECORDS):

    attack = random.choice(ATTACK_GENERATORS)

    attack_logs.append(attack())

    if (i + 1) % 500 == 0:
        print(f"{i+1} attack logs generated...")

# -----------------------------
# MERGE DATASETS
# -----------------------------

logs.extend(attack_logs)

random.shuffle(logs)

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

df = pd.DataFrame(logs)

# -----------------------------
# SAVE CSV FILES
# -----------------------------

os.makedirs("data", exist_ok=True)

logs_file = os.path.join("data", "logs.csv")
attacks_file = os.path.join("data", "attacks.csv")

df.to_csv(logs_file, index=False)

df[df["label"] == "Attack"].to_csv(attacks_file, index=False)

print("\n" + "=" * 60)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Total Records      : {len(df)}")
print(f"Normal Records     : {len(df[df['label']=='Normal'])}")
print(f"Attack Records     : {len(df[df['label']=='Attack'])}")

print("\nAttack Distribution")
print(df["attack_type"].value_counts())

print(f"\nDataset Saved To   : {logs_file}")
print(f"Attacks Saved To   : {attacks_file}")

print("=" * 60)
