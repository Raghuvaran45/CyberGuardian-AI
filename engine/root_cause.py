"""
Root Cause Analysis Engine

This module explains WHY an event
was classified as suspicious.
"""


def analyze_root_cause(event, attack_type):

    reasons = []

    row = event.iloc[0]

    # ---------------------------------------------------
    # Night Login
    # ---------------------------------------------------

    if "night_login" in row.index:

        if row["night_login"] == 1:

            reasons.append(
                "Login occurred during night hours."
            )

    # ---------------------------------------------------
    # Office Hours
    # ---------------------------------------------------

    if "office_hours" in row.index:

        if row["office_hours"] == 0:

            reasons.append(
                "Login outside office hours."
            )

    # ---------------------------------------------------
    # Failed Login Attempts
    # ---------------------------------------------------

    if "failed_login_attempts" in row.index:

        if row["failed_login_attempts"] >= 5:

            reasons.append(
                "Multiple failed login attempts detected."
            )

    # ---------------------------------------------------
    # Long Session
    # ---------------------------------------------------

    if "long_session" in row.index:

        if row["long_session"] == 1:

            reasons.append(
                "Unusually long session detected."
            )

    # ---------------------------------------------------
    # Short Session
    # ---------------------------------------------------

    if "short_session" in row.index:

        if row["short_session"] == 1:

            reasons.append(
                "Very short session detected."
            )

    # ---------------------------------------------------
    # Login Status
    # ---------------------------------------------------

    if "login_status" in row.index:

        if row["login_status"] == 0:

            reasons.append(
                "Failed authentication attempt."
            )

    # ---------------------------------------------------
    # Device Fingerprint
    # ---------------------------------------------------

    if "device_fingerprint" in row.index:

        if row["device_fingerprint"] == 0:

            reasons.append(
                "Unknown device detected."
            )

    # ---------------------------------------------------
    # High Command Sequence
    # ---------------------------------------------------

    if "command_sequence" in row.index:

        if row["command_sequence"] > 15:

            reasons.append(
                "Abnormal command sequence detected."
            )

    # ---------------------------------------------------
    # Geo Location
    # ---------------------------------------------------

    if "geo_location" in row.index:

        if row["geo_location"] > 5:

            reasons.append(
                "Suspicious geographical location."
            )

    if len(reasons) == 0:

        reasons.append(
            "No suspicious indicators found."
        )

    return reasons