print("EMAIL_ALERT_FILE_LOADED")

import smtplib
from email.message import EmailMessage


def send_alert(department, fraud_score):

    sender = "sheezhami7@gmail.com"
    password = "Xdcsjtsrmpaqvthq"

    receiver = "sheezhami7@gmail.com"

    msg = EmailMessage()

    msg["Subject"] = "MedVision AI Fraud Alert"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(f"""
High Risk Claim Detected

Department: {department}
Risk Score: {fraud_score:.2f}%

Immediate investigation recommended.
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            print("Sender:", sender)
            print("Password Length:", len(password))

            smtp.login(sender, password)
            smtp.send_message(msg)

            print("Email Sent Successfully")

    except Exception as e:
        print("Email Error:", e)


if __name__ == "__main__":

    print("Testing email...")

    send_alert("ICU", 91.5)

    print("Finished")