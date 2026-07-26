"""
CyberGuardian AI
Report Storage Engine
"""

import json
import os
from datetime import datetime


REPORTS_FOLDER = "reports"


def save_report(report):
    """
    Save the incident report as a JSON file.
    """

    # Create reports folder if it doesn't exist
    os.makedirs(REPORTS_FOLDER, exist_ok=True)

    # Create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"incident_{timestamp}.json"

    filepath = os.path.join(REPORTS_FOLDER, filename)

    # Save report
    with open(filepath, "w") as file:
        json.dump(report, file, indent=4)

    return filepath