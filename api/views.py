    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializer import TenantSignUpSerializer, TenantLoginSerializer
from tenant.models import TenantUser
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

class TenantSignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TenantSignUpSerializer(data=request.data)
        if serializer.is_valid():  
            response_data = serializer.save()
            print(response_data['clinic_email'])
            tenant = TenantUser.objects.get(clinic_email=response_data['clinic_email'])
            token = Token.objects.create(user=tenant)
            login(request, tenant)
            return Response(data={'token': token.key}, status=status.HTTP_201_CREATED)   
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TenantLoginSerializer(data=request.data)
        if serializer.is_valid():
            clinic_email = serializer.validated_data.get('clinic_email')
            password = serializer.validated_data.get('password')  
            user = authenticate(clinic_email=clinic_email, password=password)
            if not user:
                return Response(data={'error': 'Email or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            login(request, user)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_202_ACCEPTED)         
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
class TenantLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.user)
        Token.objects.filter(user=request.user).delete()
        logout(request)
        print(request.user)
        return Response(data={'success': 'successfully logged user out.'}, status=status.HTTP_200_OK) 
        