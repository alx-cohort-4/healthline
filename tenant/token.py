from datetime import datetime, timezone, timedelta
from django.core.mail import EmailMultiAlternatives, send_mail
from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
import socket, jwt, os
from django.template.loader import render_to_string
from dotenv import load_dotenv
load_dotenv()

# # def expiration_time(minutes=0):
# #     now = datetime.now(timezone.utc) + timedelta(minutes=minutes)
# #     return int(now.timestamp())

def send_token_to_verify_email(user):
    now = int(datetime.now(timezone.utc).timestamp())
    expiry_time = expiration_time(int(os.getenv("TOKEN_EXPIRATION")))
    PAYLOAD = {
        'iat': now,
        'exp': expiry_time,
        'sub': user
    }
    with open('private.pem', 'r') as file:
        private_key = file.read()
    token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
    return token

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

def send_email(email, user):
    token = send_token_to_verify_email(user)
    subject = "Email Verification"
    html_content = render_to_string(
        "tenant/email_verification.html",
        {"email": email, "token": token}
    )

#     msg = EmailMultiAlternatives(
#         subject=subject,
#         from_email=os.getenv("EMAIL_HOST_USER"),
#         to=[email]
#     )
#     msg.attach_alternative(html_content, "text/html")

#     try:
#         msg.send()
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


def send_reset_password_token(email, user):
    token = send_token_to_verify_email(user)
    link = f"http://127.0.0.1:8000/api/verify-email/{token}/"
    wrapped_token = f"Click to reset Password: {link}"
    subject = "Reset Password"

    try:
        send_mail(
        subject=subject,
        message=f"Please click this link to verify your email: {wrapped_token}",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
        ) 
        return token   
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