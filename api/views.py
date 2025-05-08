from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializer import TenantSerializer
from tenant.models import TenantUser, Patient

class TenantRegisterView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():  
            response_data = serializer.save()
            return Response(data=response_data, status=status.HTTP_201_CREATED)   
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    