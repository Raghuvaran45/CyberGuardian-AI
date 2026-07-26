def generate_recommendation(
        attack_type,
        threat_level
):


    recommendations = {


        "Brute Force":[

            "Enable account lockout",
            "Force password reset",
            "Monitor repeated login attempts"

        ],



        "Low and Slow":[

            "Monitor session duration",
            "Verify user identity",
            "Inspect command activity"

        ],



        "SQL Injection":[

            "Block suspicious requests",
            "Review database logs",
            "Apply input validation"

        ],



        "DDoS":[

            "Enable traffic filtering",
            "Apply rate limiting",
            "Monitor network traffic"

        ],



        "Malware":[

            "Isolate affected device",
            "Run malware scan",
            "Collect forensic evidence"

        ]

    }



    if attack_type in recommendations:

        return recommendations[attack_type]



    return [

        "Continue monitoring activity",
        "Collect additional security logs"

    ]