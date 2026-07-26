import sqlite3


conn = sqlite3.connect(
    "database/incidents.db"
)

cursor = conn.cursor()


columns = [

    ("incident_id","TEXT"),

    ("affected_entity","TEXT"),

    ("source_ip","TEXT"),

    ("device_information","TEXT"),

    ("attack_summary","TEXT"),

    ("analyst_action","TEXT")

]


for column,datatype in columns:

    try:

        cursor.execute(
            f"""
            ALTER TABLE incidents
            ADD COLUMN {column} {datatype}
            """
        )

    except:

        pass



conn.commit()

conn.close()


print(
    "Database Updated"
)