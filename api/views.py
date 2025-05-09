from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializer import TenantSignUpSerializer, TenantLoginSerializer
from tenant.models import TenantUser

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
        