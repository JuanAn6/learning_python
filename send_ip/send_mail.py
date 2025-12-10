import os
import smtplib
from email.mime.text import MIMEText
import config

def send_mail(mail_server, port, sender, password, recipient):
    try:

        print(sender, password, recipient)

        msg = MIMEText("Body of message")
        msg["Subject"] = "Subject of message"
        msg["From"] = sender
        msg["To"] = recipient

        with smtplib.SMTP_SSL(mail_server, port) as server:
            server.login(sender, password)
            server.send_message(msg)

        print("Mail sended!")
    except Exception as e:
        print("An error occurred:", str(e))



send_mail(config.MAILSERVER, config.PORT, config.MAIL, config.PASSWORD, config.RECIPIENT)