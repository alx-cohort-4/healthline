from datetime import datetime, timezone, timedelta
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
import socket, jwt, os
from django.template.loader import render_to_string
from dotenv import load_dotenv
load_dotenv()

# # def expiration_time(minutes=0):
# #     now = datetime.now(timezone.utc) + timedelta(minutes=minutes)
# #     return int(now.timestamp())

# def send_token_to_verify_email(user):
#     now = int(datetime.now(timezone.utc).timestamp())
#     expiry_time = expiration_time(int(os.getenv("TOKEN_EXPIRATION")))
#     PAYLOAD = {
#         'iat': now,
#         'exp': expiry_time,
#         'sub': user
#     }
#     with open('private.pem', 'r') as file:
#         private_key = file.read()
#     token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
#     return token

def decode_token(token):
    with open('public.pem', 'r') as f:
        public_key = f.read()
    try:
        decoded = jwt.decode(token, public_key, algorithms=os.getenv("ALGO"))
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(e)
        return None

<<<<<<< HEAD
# def send_email(email, user):
#     token = send_token_to_verify_email(user)
#     subject = "Email Verification"
#     html_content = render_to_string(
#         "tenant/email_verification.html",
#         {"email": email, "token": token}
#     )
=======
def send_email(email, user):
    token = send_token_to_verify_email(user)
    subject = "Email Verification"
    token_link = f"http://127.0.0.1:8000/api/vi/verify-email/{token}/"
    html_content = render_to_string(
        template_name="api/verify_email.html",
        context={"email": email, "verification_url": token_link}
    )
>>>>>>> 63a7ac6b2b2e14e26ddc052acd4a990db8723dc9

#     msg = EmailMultiAlternatives(
#         subject=subject,
#         from_email=os.getenv("EMAIL_HOST_USER"),
#         to=[email]
#     )
#     msg.attach_alternative(html_content, "text/html")

<<<<<<< HEAD
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

=======
    try:
        msg.send()
    except SMTPAuthenticationError:
        print("SMTP Authentication failed. Check your email credentials.")
        return None
    except SMTPConnectError:
        print("Failed to connect to the SMTP server. Is it reachable?")
        return None
    except SMTPRecipientsRefused:
        print("Recipient address was refused by the server.")
        return None
    except SMTPSenderRefused:
        print("Sender address was refused by the server.")
        return None
    except SMTPDataError:
        print("SMTP server replied with an unexpected error code (data issue).")
        return None
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return None
    except socket.gaierror:
        print("Network error: Unable to resolve SMTP server.")
        return None
    except socket.timeout:
        print("Network error: SMTP server timed out.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
>>>>>>> 63a7ac6b2b2e14e26ddc052acd4a990db8723dc9

def send_reset_password_token(email, user):
    token = send_token_to_verify_email(user)
    token_link = f"http://127.0.0.1:8000/api/v1/verify-password-reset-token/{token}/"
    subject = "Reset Password"

    html_content = render_to_string(
        template_name="api/reset_password.html",
        context={'subject': subject, "verification_url": token_link}
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=os.getenv("EMAIL_HOST_USER"),      
        to=[email]
    )

    msg.attach_alternative(content=html_content, mimetype="text/html")

    try:
        msg.send()  
        return True
    except SMTPAuthenticationError:
        print("SMTP Authentication failed. Check your email credentials.")
        return None
    except SMTPConnectError:
        print("Failed to connect to the SMTP server. Is it reachable?")
        return None
    except SMTPRecipientsRefused:
        print("Recipient address was refused by the server.")
        return None
    except SMTPSenderRefused:
        print("Sender address was refused by the server.")
        return None
    except SMTPDataError:
        print("SMTP server replied with an unexpected error code (data issue).")
        return None
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return None
    except socket.gaierror:
        print("Network error: Unable to resolve SMTP server.")
        return None
    except socket.timeout:
        print("Network error: SMTP server timed out.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None