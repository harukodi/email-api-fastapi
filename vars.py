import os
from dotenv import load_dotenv
load_dotenv(override=True)
smtp_server = os.environ.get("SMTP_SERVER")
smtp_sender_email = os.environ.get("SENDER_EMAIL")
smtp_password = os.environ.get("SMTP_PASSWORD")