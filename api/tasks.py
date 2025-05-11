from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
from celery import shared_task
from datetime import datetime, timezone, timedelta
import socket, jwt, os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from tenant.models import TenantUser

from dotenv import load_dotenv
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
    with open('private.pem', 'r') as file:
        private_key = file.read()
    token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
    return token

@shared_task
def send_email(email, user):
    token = send_token_to_verify_email(email)
    token_link = f"{os.getenv('API_URL')}/tenant/verify-email-complete/?token={token}"

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

@shared_task
def send_email_password_reset(email, user):
    token = send_token_to_verify_email(email)
    token_link = f"{os.getenv('API_URL')}/tenant/verify-password-reset-token/?token={token}"
    subject = "Reset Password"

    body = "Please click this link to verify your email:"
    html_content = render_to_string(
        "api/reset_password.html",
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


def decode_token(token):
    with open('public.pem', 'r') as f:
        public_key = f.read()
    try:
        decoded = jwt.decode(token, public_key, algorithms=os.getenv("ALGO"))
        print("In decoded function", decoded)
        return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return False
    except jwt.InvalidTokenError:
        print("Invalid token")
        return False
    
def send_reset_password_token(email, user):
    token = send_token_to_verify_email(user)
    send_email_password_reset.delay(email, user)
    return token



# def send_reset_password_token(email, user):
#     token = send_token_to_verify_email(user)
#     link = f"http://127.0.0.1:8000/api/v1/tenant/verify-password-reset-token/?token={token}"
#     wrapped_token = f"Click to reset Password: {link}"
#     subject = "Reset Password"

#     try:
#         send_mail(
#         subject=subject,
#         message=f"Please click this link to verify your email: {wrapped_token}",
#         from_email=os.getenv("EMAIL_HOST_USER"),
#         recipient_list=[email],
#         ) 
#         return token   
#     except SMTPAuthenticationError:
#         print("SMTP Authentication failed. Check your email credentials.")
#     except SMTPConnectError:
#         print("Failed to connect to the SMTP server. Is it reachable?")
#     except SMTPRecipientsRefused:
#         print("Recipient address was refused by the server.")
#     except SMTPSenderRefused:
#         print("Sender address was refused by the server.")
#     except SMTPDataError:
#         print("SMTP server replied with an unexpected error code (data issue).")
#     except SMTPException as e:
#         print(f"SMTP error occurred: {e}")
#     except socket.gaierror:
#         print("Network error: Unable to resolve SMTP server.")
#     except socket.timeout:
#         print("Network error: SMTP server timed out.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
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
    