import pandas as pd


def detect_new_entities(
        current_event,
        historical_data
):

    result = {

        "new_user": False,

        "new_device": False,

        "new_ip": False,

        "risk": "LOW"

    }


    # -----------------------------
    # USER CHECK
    # -----------------------------

    if "entity_id" in current_event:

        user = current_event["entity_id"]


        if user not in historical_data["entity_id"].values:

            result["new_user"] = True



    # -----------------------------
    # DEVICE CHECK
    # -----------------------------

    if "device_fingerprint" in current_event:

        device = current_event[
            "device_fingerprint"
        ]


        if device not in historical_data[
            "device_fingerprint"
        ].values:

            result["new_device"] = True



    # -----------------------------
    # IP CHECK
    # -----------------------------

    if "source_ip" in current_event:

        ip = current_event[
            "source_ip"
        ]


        if ip not in historical_data[
            "source_ip"
        ].values:

            result["new_ip"] = True



    # -----------------------------
    # RISK ASSIGNMENT
    # -----------------------------

    if (

        result["new_user"]

        or

        result["new_device"]

        or

        result["new_ip"]

    ):

        result["risk"] = "MEDIUM"



    return result