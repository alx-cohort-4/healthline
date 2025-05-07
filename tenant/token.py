# from datetime import datetime, timezone, timedelta
# from django.core.mail import EmailMultiAlternatives
# # from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
# import socket, jwt, os
# from django.template.loader import render_to_string
# # from dotenv import load_dotenv
# # load_dotenv()

# # def expiration_time(minutes=0):
# #     now = datetime.now(timezone.utc) + timedelta(minutes=minutes)
# #     return int(now.timestamp())

# # def send_token_to_verify_email(user):
#     now = int(datetime.now(timezone.utc).timestamp())
#     expiry_time = expiration_time(int(os.getenv("TOKEN_EXPIRATION")))
#     PAYLOAD = {
#         'iat': expiry_time,
#         'exp': now,
#         'sub': user
#     }
#     with open('private.pem', 'r') as file:
#         private_key = file.read()
#     token = jwt.encode(payload=PAYLOAD, key=private_key, algorithm=os.getenv("ALGO"))
#     return token

# # def send_email(email, user):
#     token = send_token_to_verify_email(user)
#     subject = "Email Verification"
#     html_content = render_to_string(
#         "tenant/email_verification.html",
#         {"email": email, "token": token}
#     )

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

# # with open('public.pem', 'r') as f:
# #     public_key = f.read()

# # decoded = jwt.decode(token, public_key, algorithms=["RS256"])
# # print(decoded)

