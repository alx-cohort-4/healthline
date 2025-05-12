from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .serializer import TenantSignUpSerializer, TenantLoginSerializer, TenantPasswordResetSerializer, TenantPasswordConfirmResetSerializer
from tenant.models import TenantUser
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
import jwt, os
from tenant.models import TenantUser
from .tasks import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

# from tenant.token import send_reset_password_token, decode_token

# class VerifyEmailView(APIView):
#     """
#     View to handle email verification requests
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request) -> Response:
#         user = request.user
#         email = user.clinic_email
#         username = user.clinic_name
#         email_verified = user.email_verified

#         if not email_verified:
            # send_email.delay(email=email, user=username)    
#             return Response({"message": "Verification email sent."}, status=200)
#         return Response({"message": "Email already verified."}, status=200)

class VerifyEmailCompleteView(APIView):
    """
    View to handle email verification completion
    """
    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        token = request.GET.get("token")
        with open('public.pem', 'r') as pub_file:
            public_key = pub_file.read()
        try:
            payload = jwt.decode(token, public_key, os.getenv('ALGO'))
            if not payload:
                return Response(data={'error': 'invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
            user = payload.get("sub")
            if not user:
                return Response(data={'error': 'token is missing email info'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_exists = TenantUser.objects.get(clinic_email=user)
        except TenantUser.MultipleObjectsReturned:
            return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
        except TenantUser.DoesNotExist:
            return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_404_NOT_FOUND)   
        if user_exists.email_verified:
            return Response(data={'error': "Tenant has already been verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_exists.email_verified = True
        user_exists.save()
        login(request, user_exists)
        token, _ = Token.objects.get_or_create(user=user_exists)
        return Response(data={'success': 'user has been registered successfully', 'token': token.key}, status=status.HTTP_200_OK)
    
class VerifyPasswordTokenView(APIView):
    """
    View to handle password reset token verification
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        token = request.GET.get("token")
        if not token:
            return Response(data={'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = decode_token_val(token=token)
            if not decoded_token:
                return Response(data={'error': 'token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

            email = decoded_token.get('sub')
            if not email:
                return Response(data={'error': 'token is missing email info'}, status=status.HTTP_400_BAD_REQUEST)
            
            tenant = TenantUser.objects.get(clinic_email=email)
            if tenant.email_verified and not tenant.token_valid:
                pass

            tenant.token_valid = True
            tenant.save()
            return Response(data={'success': 'token is valid'})

        except TenantUser.DoesNotExist:
            return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_404_NOT_FOUND)
        except TenantUser.MultipleObjectsReturned:
            return Response(data={'error': 'multiple account found for this email'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': f'an error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
class TenantSignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # TenantUser.objects.all().delete()
        serializer = TenantSignUpSerializer(data=request.data)
        if serializer.is_valid():  
            response_data = serializer.save()
            send_email.delay(email=response_data['clinic_email'], user=response_data['clinic_email'])
            return Response(data={'detail': 'please check your email for verification'}, status=status.HTTP_200_OK)   
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

class TenantPasswordResetView(GenericAPIView):
    serializer_class = TenantPasswordResetSerializer  
    authentication_classes = []     
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('clinic_email')            
            try:
                return Response(data={'reset_token': send_reset_password_token(email=email, user=email)}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
# def verify_email(request, token):
#     from django.http import HttpResponse
#     if decode_token(token):
#         return HttpResponse("Verified", True)
#     return HttpResponse("Not Verified", False) 

class TenantConfirmResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = TenantPasswordConfirmResetSerializer

    def post(self, request, *args, **kwargs):
        clinic_email = kwargs['clinic_email']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                tenant = TenantUser.objects.get(clinic_email=clinic_email)
                new_password = make_password(password)
                tenant.password = new_password
                tenant.save()
            except TenantUser.DoesNotExist:
                return Response(data={'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except TenantUser.MultipleObjectsReturned:
                return Response(data={'error': ''}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'success': 'password has been changed successfully'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([AllowAny])   
# def verify_tenant_email(request, token):
#     from django.http import HttpResponse
#     decoded_token = decode_token(token)
#     if not decoded_token:
#         return Response(data={'error': 'invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
#     email = decoded_token.get('sub') # get the email attached to the token
#     if not email:
#         return Response(data={'error': "Token is missing email info"}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         tenant = TenantUser.objects.get(clinic_email=email)
#     except TenantUser.MultipleObjectsReturned:
#         return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
#     except TenantUser.DoesNotExist:
#         return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST)   
#     if tenant.email_verified:
#         return Response(data={'error': "Tenant has already been verified"}, status=status.HTTP_400_BAD_REQUEST)
    
#     tenant.email_verified = True
#     tenant.token_valid = True
#     tenant.save()
#     login(request, user=tenant)
#     token, _ = Token.objects.get_or_create(user=tenant)
#     return Response(data={'success': 'user has been registered successfully', 'token': token.key}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([AllowAny])
# def verify_password_token(request, token):
#     decoded_token = decode_token(token=token)
#     if not decoded_token:
#         return Response(data={'error': 'token is valid or expired'}, status=status.HTTP_400_BAD_REQUEST)

#     email = decoded_token.get('sub')
#     if not email:
#         return Response(data={'error': 'token is missing email info'}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         tenant = TenantUser.objects.get(clinic_email=email)
#         if tenant.email_verified and not tenant.token_valid:
#             pass
#     except TenantUser.DoesNotExist:
#         return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST)
#     except TenantUser.MultipleObjectsReturned:
#         return Response(data={'error': 'multiple account found for this email'}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception:
#         return Response(data={'error': 'an error occured when decoding the token'}, status=status.HTTP_400_BAD_REQUEST)
#     tenant.token_valid = True
#     return Response(data={'success': 'token is valid'})

 