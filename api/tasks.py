from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
# from celery import shared_task
from datetime import datetime, timezone, timedelta
import socket, jwt, os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv
import random
load_dotenv()

def expiration_time(minutes=0):
    now = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return int(now.timestamp())

def send_token_to_verify_email(email):
    now = int(datetime.now(timezone.utc).timestamp())
    expiry_time = expiration_time(int(os.getenv("TOKEN_EXPIRATION")))
    PAYLOAD = {
        'iat': now,
        'exp': expiry_time,
        'sub': email
    }
    print("In send_token")
    with open('private.pem', 'r') as file:
        private_key = file.read()
    token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
    print("done token")
    return token

# @shared_task
def send_email(email):
    token = send_token_to_verify_email(email)
    print(token)
    token_link = f"{os.getenv('API_URL')}/tenant/verify-email/?token={token}/"

    subject = "Email Verification"

    body = "Please verify your email address"
    html_content = render_to_string(
        "api/verify_email.html",
        {"email": email, "verification_url": token_link}
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=os.getenv("P_EMAIL_HOST_USER"),
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except SMTPAuthenticationError:
        print("SMTP Authentication failed. Check your email credentials.")
    except SMTPConnectError:
        print("Failed to connect to the SMTP server. Is it reachable?")
    except SMTPRecipientsRefused:
        print("Recipient address was refused by the server.")
    except SMTPSenderRefused:
        print("Sender address was refused by the server.")
    except SMTPDataError:
        print("SMTP server replied with an unexpected error code (data issue).")
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except socket.gaierror:
        print("Network error: Unable to resolve SMTP server.")
    except socket.timeout:
        print("Network error: SMTP server timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# @shared_task
def send_email_password_reset(email):
    token = send_token_to_verify_email(email)
    token_link = f"{os.getenv('API_URL')}/tenant/verify-password-reset-token/?token={token}"
    subject = "Reset Password"

    html_content = render_to_string(
        template_name="api/reset_password.html",
        context={"subject": subject, "verification_url": token_link}
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=os.getenv("EMAIL_HOST_USER"),
        to=[email]
    )
    msg.attach_alternative(content=html_content, mimetype="text/html")

    try:
        msg.send()
    except SMTPAuthenticationError:
        print("SMTP Authentication failed. Check your email credentials.")
    except SMTPConnectError:
        print("Failed to connect to the SMTP server. Is it reachable?")
    except SMTPRecipientsRefused:
        print("Recipient address was refused by the server.")
    except SMTPSenderRefused:
        print("Sender address was refused by the server.")
    except SMTPDataError:
        print("SMTP server replied with an unexpected error code (data issue).")
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except socket.gaierror:
        print("Network error: Unable to resolve SMTP server.")
    except socket.timeout:
        print("Network error: SMTP server timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def decode_token_val(token):
    with open('public.pem', 'r') as f:
        public_key = f.read()
    try:
        decoded = jwt.decode(token, public_key, algorithms=os.getenv("ALGO"))
        print("In decoded function", decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    
