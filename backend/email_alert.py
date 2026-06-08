import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("EMAIL_SENDER", "")
password = os.getenv("EMAIL_PASSWORD", "")
receiver = os.getenv("EMAIL_RECEIVER", "")


def send_email_alert(senior, bp, sugar, hr, risk):

    if risk != "High Risk":
        return

    subject = "🚨 High Health Risk Alert"

    body = f"""
High Health Risk Detected

Senior: {senior}

Blood Pressure: {bp}
Sugar Level: {sugar}
Heart Rate: {hr}

Please check immediately.
"""

    send_mail(subject, body)


def send_missed_med_alert(senior, medicine):

    subject = "⚠️ Missed Medication Alert"

    body = f"""
Missed Medication

Senior: {senior}
Medicine: {medicine}

Medicine was not taken within time window.
"""

    send_mail(subject, body)


def send_mail(subject, body):

    if not sender or not password or not receiver:
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)