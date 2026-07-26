"""
CyberGuardian AI
Advanced SOC Incident Report Generator
"""


from datetime import datetime



def generate_incident_report(result):


    event = result.get(
        "event",
        {}
    )


    mitre = result.get(
        "mitre_attack",
        {

            "technique_id": "Unknown",

            "technique": "Unknown",

            "tactic": "Unknown"

        }
    )


    threat = result.get(
        "threat_intelligence",
        {

            "severity": "Unknown",

            "description": "Unavailable",

            "impact": "Unavailable",

            "ioc": []

        }
    )


    report = {


        # -------------------------
        # Incident Information
        # -------------------------

        "incident_id":

            "CG-" +

            datetime.now().strftime(
                "%Y%m%d%H%M%S"
            ),


        "timestamp":

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),



        # -------------------------
        # Security Summary
        # -------------------------

        "status":

            result.get(
                "status",
                "UNKNOWN"
            ),



        "attack_type":

            result.get(
                "attack_type",
                "Unknown"
            ),



        "risk_score":

            result.get(
                "risk_score",
                0
            ),



        "threat_level":

            result.get(
                "threat_level",
                "LOW"
            ),



        # -------------------------
        # Entity Information
        # -------------------------

        "affected_entity":

            event.get(
                "entity_id",
                "Unknown"
            ),



        "source_ip":

            event.get(
                "source_ip",
                "Unknown"
            ),



        "device_information":

            event.get(
                "device_fingerprint",
                "Unknown"
            ),



        # -------------------------
        # Attack Explanation
        # -------------------------

        "attack_summary":

            (
                "A possible "

                +

                str(
                    result.get(
                        "attack_type",
                        "security"
                    )
                )

                +

                " activity was detected "
                
                "through behavioral anomaly analysis."
            ),



        "detection_reason":

            result.get(
                "root_causes",
                []
            ),



        # -------------------------
        # MITRE ATT&CK
        # -------------------------

        "mitre_attack":

            mitre,



        # -------------------------
        # Threat Intelligence
        # -------------------------

        "threat_intelligence":

            threat,



        # -------------------------
        # Response Actions
        # -------------------------

        "recommended_actions":

            result.get(
                "recommendations",
                []
            ),



        "analyst_action":

            [

                "Verify affected user activity",

                "Review authentication logs",

                "Investigate source IP",

                "Monitor future behavior"

            ]

    }



    return report