import sqlite3
import json


conn = sqlite3.connect(
    "database/incidents.db"
)

cursor = conn.cursor()


cursor.execute(
    """
    SELECT id, attack_type, root_causes, recommendations
    FROM incidents
    """
)


rows = cursor.fetchall()



for row in rows:

    incident_id = row[0]
    attack_type = row[1]

    root_causes = row[2]
    recommendations = row[3]


    incident_code = (
        "CG-"
        +
        str(incident_id)
    )


    summary = (
        "A possible "
        +
        str(attack_type)
        +
        " activity was detected "
        "through behavioral anomaly analysis."
    )


    actions = json.dumps(
        [
            "Verify affected user activity",
            "Review authentication logs",
            "Investigate source IP",
            "Monitor future behavior"
        ]
    )


    cursor.execute(
        """
        UPDATE incidents

        SET

        incident_id=?,

        attack_summary=?,

        analyst_action=?

        WHERE id=?

        """,

        (
            incident_code,
            summary,
            actions,
            incident_id
        )
    )



conn.commit()

conn.close()


print(
    "Old reports updated successfully"
)