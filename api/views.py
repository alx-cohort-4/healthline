from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
import jwt, os
from tenant.models import TenantUser
from .tasks import send_email
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def verify_email(request) -> Response:
    """
    This function is used to send the verification email to the user.
    """
    user = request.user
    email = user.clinic_email
    username = user.clinic_name
    email_verified = user.email_verified

    if not email_verified:
        send_email.delay(email=email, user=username)    
        return Response({"message": "Verification email sent."}, status=200)
    else:
        return Response({"message": "Email already verified."}, status=200)

@api_view(["GET"])
def verify_email_complete(request) -> Response:
    """
    This function is used to verify the email of the user.
    """
    token = request.GET.get("token")
    with open('public.pem', 'r') as pub_file:
        public_key = pub_file.read()
    try:
        payload = jwt.decode(token, public_key, os.getenv('ALGO'))
        user = payload.get("sub")
    except jwt.ExpiredSignatureError:
        return Response({"message": "Token has expired"}, status=400)
    except jwt.InvalidTokenError:
        return Response({"message": "Invalid token"}, status=400)
    
    try:
        user_exists = TenantUser.objects.get(clinic_email=user)
        if user_exists:
            user_exists.email_verified = True
            user_exists.save()
            login(request, user_exists)
            return Response({"message": "Email verified successfully"}, status=200)
    except TenantUser.DoesNotExist:
        return Response({"message": "Tenant does not exist"}, status=404)
    



    