import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from vars import smtp_server, smtp_sender_email, smtp_password

async def send_email_request(receiver_email, user_data_name, user_data_email, user_data_phone, user_data_address, user_data_data):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"FÖRFRÅGAN FRÅN: {user_data_name.upper()}"
    message["From"] = smtp_sender_email
    message["To"] = receiver_email
    text_content = f"""\n Namn: {user_data_name} \n Email: {user_data_email} \n Telefonnummer: {user_data_phone} \n Address: {user_data_address} \n Meddelande: {user_data_data}"""
    content = MIMEText(text_content, "plain")
    message.attach(content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
        server.login(smtp_sender_email, smtp_password)
        server.sendmail(
            smtp_sender_email, receiver_email, message.as_string()
        )