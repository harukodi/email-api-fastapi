import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from vars import smtp_server, smtp_sender_email, smtp_password

async def send_confirmation_email(receiver_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Bekräftelse"
    message["From"] = smtp_sender_email
    message["To"] = receiver_email
    text_content = f"""Tack vi har tagit emot din förfrågan och kommer att återkomma så snart som möjligt!"""
    content = MIMEText(text_content, "plain")
    message.attach(content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
        server.login(smtp_sender_email, smtp_password)
        server.sendmail(
            smtp_sender_email, receiver_email, message.as_string()
        )