import sqlite3
import os
import json

DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "incidents.db")


def create_table():

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        status TEXT,

        attack_type TEXT,

        risk_score REAL,

        threat_level TEXT,

        mitre_id TEXT,

        technique TEXT,

        tactic TEXT,

        root_causes TEXT,

        recommendations TEXT,

        threat_intelligence TEXT

    )
    """)

    conn.commit()
    conn.close()


def save_incident(report):

    create_table()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    mitre = report.get(
        "mitre_attack",
        {
            "technique_id": "Unknown",
            "technique": "Unknown",
            "tactic": "Unknown"
        }
    )

    cursor.execute("""
    INSERT INTO incidents
    (
        timestamp,
        status,
        attack_type,
        risk_score,
        threat_level,
        mitre_id,
        technique,
        tactic,
        root_causes,
        recommendations,
        threat_intelligence
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        report.get("timestamp"),
        report.get("status"),
        report.get("attack_type"),
        report.get("risk_score"),
        report.get("threat_level"),
        mitre.get("technique_id"),
        mitre.get("technique"),
        mitre.get("tactic"),
        json.dumps(report.get("root_causes", [])),
        json.dumps(report.get("recommendations", [])),
        json.dumps(report.get("threat_intelligence", {}))
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()

    print("Database created successfully.")