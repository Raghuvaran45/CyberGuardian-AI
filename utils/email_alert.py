import smtplib
from email.message import EmailMessage


def send_email_alert(
        attack_type,
        risk_score,
        threat_level,
        mitre
):

    sender_email = "rayaraghuvaran@gmail.com"
    sender_password = "leae fawi ynhd tbop"

    receiver_email = "rayaraghuvaran@gmail.com"


    if threat_level not in [
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]:
        return



    message = EmailMessage()


    message["Subject"] = (
        "🚨 CyberGuardian AI Security Alert"
    )


    message["From"] = sender_email

    message["To"] = receiver_email



    message.set_content(
f"""
CyberGuardian AI Security Alert

Threat Detected

Attack Type:
{attack_type}


Risk Score:
{risk_score}


Threat Level:
{threat_level}


MITRE ATT&CK Mapping:

Technique ID:
{mitre["technique_id"]}

Technique:
{mitre["technique"]}

Tactic:
{mitre["tactic"]}


Action Required:
Investigate the activity immediately.

"""
)



    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()


        server.login(
            sender_email,
            sender_password
        )


        server.send_message(
            message
        )


        server.quit()


        print(
            "Email alert sent successfully"
        )


    except Exception as e:

        print(
            "Email Alert Error:",
            e
        )