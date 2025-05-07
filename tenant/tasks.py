from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
from celery import shared_task
from datetime import datetime, timezone, timedelta
import socket, jwt, os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseBadRequest
from .models import TenantUser

from dotenv import load_dotenv
load_dotenv()

@shared_task
def expiration_time(minutes=0):
    now = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return int(now.timestamp())

@shared_task
def send_token_to_verify_email(email):
    now = int(datetime.now(timezone.utc).timestamp())
    expiry_time = expiration_time(int(os.getenv("TOKEN_EXPIRATION")))
    PAYLOAD = {
        'iat': now,
        'exp': expiry_time,
        'sub': email
    }
    with open('private.pem', 'r') as file:
        private_key = file.read()
    token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
    return token

@shared_task
def send_email(email, user):
    token = send_token_to_verify_email(email)
    subject = "Email Verification"
    url = os.getenv("APP_URL");

    body = "Please verify your email address"
    html_content = render_to_string(
        "tenant/email_verification.html",
        {"email": email, "token": token, "app_url": url}
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=os.getenv("EMAIL_HOST_USER"),
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
# def verify_email(token):
#     with open('public.pem', 'r') as pub_file:
#         public_key = pub_file.read()
#     payload = jwt.decode(token, public_key, os.getenv('ALGO'))
#     user = payload.get("sub")
#     try:
#         user_exists = TenantUser.objects.filter(clinic_email=user)
#         if user_exists:
#             print("User Exists")
#     except TenantUser.DoesNotExist:
#         print("Tenant does not exist")
    