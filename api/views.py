from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .serializer import TenantSignUpSerializer, TenantLoginSerializer, TenantPasswordResetSerializer, TenantPasswordConfirmResetSerializer, TenantPasswordChangeSerializer, ProfileUpdateSerializer, DeveloperSignupSerializer, StaffSignupSerializer, AutomationScriptSerializer
from tenant.models import TenantUser, EmailDeviceOTP, Staff, Patient, AutomationScript, AutomationState
from .tasks import send_email_password_reset, decode_token_val, send_email, send_dev_email, send_staff_email

class TenantSignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if len(request.data) > 8 or len(request.data) < 8:
            return Response(data={'info': 'only clinic_email, clinic_name, website, phonenumber, country, address, password, re_enter_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TenantSignUpSerializer(data=request.data)
        if serializer.is_valid():  
            response_data = serializer.save()
            send_email(email=response_data['clinic_email'])
            return Response(data={'detail': 'please check your email for verification'}, status=status.HTTP_200_OK)   
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if len(request.data) > 2:
            return Response(data={'info': 'only clinic_email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TenantLoginSerializer(data=request.data)
        if serializer.is_valid():
            clinic_email = serializer.validated_data.get('clinic_email')
            password = serializer.validated_data.get('password') 
            user = authenticate(clinic_email=clinic_email, password=password)
            if not user:
                return Response(data={'error': 'Email or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            if EmailDeviceOTP.objects.filter(user=user).exists():
                EmailDeviceOTP.objects.filter(user=user).delete()
            otp_for_user = EmailDeviceOTP(user=user)
            otp_for_user.generate_otp()
            user.token_valid = False
            return Response(data={'info': 'please your email for OTP code'}, status=status.HTTP_200_OK)        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_otp(request, *args, **kwargs):
    if len(request.data) > 2:
        return(Response(data={'info': 'only clinic_email and otp_code is required'}, status=status.HTTP_400_BAD_REQUEST))
    clinic_email = request.data.get("clinic_email")
    otp_code = request.data.get("otp_code")
    if not clinic_email or not otp_code:
        return Response(data={'error': 'clinic email and otp code are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = TenantUser.objects.get(clinic_email=clinic_email)
    except TenantUser.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
    except TenantUser.DoesNotExist:
        return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST)  
    except Exception as e:
        return Response(data={'error': 'an error occured while verifying user\'s email'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.email_verified:
        return Response(data={'error': 'email has not been verified'}, status=status.HTTP_400_BAD_REQUEST) 
    
    try:
        email = EmailDeviceOTP.objects.get(user=user)
    except EmailDeviceOTP.DoesNotExist:
        return Response(data={'error': 'otp used or has not been generated for this user'}, status=status.HTTP_400_BAD_REQUEST)
    except EmailDeviceOTP.MultipleObjectsReturned:
        return Response(data={'error': 'multiple otp found for this user'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={'error': 'an error occured while verifying token'}, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_code != email.otp_code:
        return Response(data={'error': 'invalid code provided'}, status=status.HTTP_400_BAD_REQUEST)
    if not email.verify_token():
        return Response(data={'error': 'code has expired'}, status=status.HTTP_400_BAD_REQUEST)
    # Delete any token associated to the user, then create a fresh token
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    user.token_valid = True
    user.save()
    # vanish the otp after verification
    EmailDeviceOTP.objects.filter(user=user).delete()
    return Response(data={'token': token.key}, status=status.HTTP_202_ACCEPTED) 
    
class TenantPasswordResetView(GenericAPIView):
    serializer_class = TenantPasswordResetSerializer  
    authentication_classes = []     
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if len(request.data) > 1:
            return Response(data={'info': 'only email is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('clinic_email')
            try:
                tenant = TenantUser.objects.get(clinic_email=email)
                if tenant.email_verified:
                    send_email_password_reset(email=email)
            except TenantUser.DoesNotExist:
                pass
            except TenantUser.MultipleObjectsReturned:
                pass
            except Exception:
                pass 
            # sends 200 status code regardless if email exist or not
            return Response(data={'detail': 'please check your email to continue.'}, status=status.HTTP_200_OK)                       
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])   
def verify_tenant_email(request):
    if request.data:
        return Response(data={'info': 'only token is allowed in the path parameter, not data in the body parameter'})
    token = request.GET.get("token")
    if not token:
        return Response(data={'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)
    decoded_token = decode_token_val(token)
    if not decoded_token:
        return Response(data={'error': 'invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
    email = decoded_token.get('sub') # get the email attached to the token
    if not email:
        return Response(data={'error': "Token is missing email info"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        tenant = TenantUser.objects.get(clinic_email=email)
        print("Tenant checked")
    except TenantUser.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
    except TenantUser.DoesNotExist:
        return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        return Response(data={'error': 'an error occured while verifying user\'s email'}, status=status.HTTP_400_BAD_REQUEST)  
    if tenant.email_verified:
        return Response(data={'error': "Tenant has already been verified"}, status=status.HTTP_400_BAD_REQUEST)
    tenant.email_verified = True
    tenant.token_valid = True
    tenant.clinic_email = email
    tenant.save()
    token, _ = Token.objects.get_or_create(user=tenant)
    return Response(
        {'data':
            {
            'id': tenant.id,
            'clinic_name': tenant.clinic_name,
            'clinic_email': tenant.clinic_email,
            'website': tenant.website,
            'phonenumber': tenant.phonenumber,
            'address': tenant.address,
            'country': tenant.country,
            'date_joined': tenant.date_joined.date()
            },
        'token': token.key
        }, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_password_token(request): 
    if request.data:
        return Response(data={'info': 'only token is allowed in the path parameter, not data in the body parameter'}, status=status.HTTP_400_BAD_REQUEST)
    token = request.GET.get("token")
    if not token:
        return Response(data={'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)
    decoded_token = decode_token_val(token=token)
    if not decoded_token:
        return Response(data={'error': 'token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

    email = decoded_token.get('sub')
    if not email:
        return Response(data={'error': 'token is missing email info'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        tenant = TenantUser.objects.get(clinic_email=email)
        if tenant.email_verified and not tenant.token_valid:
            pass
    except TenantUser.DoesNotExist:
        return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST)
    except TenantUser.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found for this email'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(data={'error': 'an error occured when decoding the token'}, status=status.HTTP_400_BAD_REQUEST)
    tenant.token_valid = True
    tenant.save()
    return Response(data={'success': 'token is valid'})   

class TenantConfirmResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = TenantPasswordConfirmResetSerializer

    def post(self, request, *args, **kwargs):
        clinic_email = kwargs.get("clinic_email")
        if len(request.data) > 2:
            return Response(data={'info': 'only password and re_enter_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                tenant = TenantUser.objects.get(clinic_email=clinic_email)
            except TenantUser.DoesNotExist:
                return Response(data={'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except TenantUser.MultipleObjectsReturned:
                return Response(data={'error': 'Multiple account found with this email'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={'error': 'email has not been verified!'}, status=status.HTTP_400_BAD_REQUEST)           
            if tenant.token_valid and tenant.email_verified:
                new_password = make_password(password)
                tenant.password = new_password
                tenant.token_valid = True
                tenant.save()
                token = Token.objects.create(user=tenant)
                return Response(data={'token': token.key}, status=status.HTTP_200_OK)           
            return Response(data={'error': 'token has been used by user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantChangePassword(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TenantPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        email = kwargs.get("clinic_email")
        if len(request.data) > 3:
            return Response(data={'info': 'only old_password, new_password, and confirm_new_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            tenant = TenantUser.objects.get(clinic_email=email)
        except TenantUser.DoesNotExist:
            return Response(data={'error': 'user does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except TenantUser.MultipleObjectsReturned:
            return Response(data={'error': 'multiple account found with email'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={'error': 'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
        if not tenant.token_valid and tenant.email_verified:
            return Response(data={'error': 'user is not logged in yet.'}, status=status.HTTP_400_BAD_REQUEST)
        old_password = serializer.validated_data.get('old_password')
        old_accurate_pass = authenticate(request, clinic_email=tenant, password=old_password)
        if not old_accurate_pass:
            return Response(data={'error': 'The old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        harshed_password = make_password(serializer.validated_data.get('new_password'))
        if serializer.validated_data.get('new_password') == old_password:
            return Response(data={'error': 'new password is similar to the old password'}, status=status.HTTP_400_BAD_REQUEST)
        tenant.password = harshed_password
        tenant.save()
        return Response(data={'success': 'password has been changed successfully'}, status=status.HTTP_200_OK)
        
class TenantLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.data:
            return Response(data={'info': 'data in the body parameter is not allowed, just the token in the header'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.token_valid = False
        request.user.save()
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(data={'success': 'successfully logged user out.'}, status=status.HTTP_200_OK) 
    
class ProfileUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return TenantUser.objects.get(id=id)
        except TenantUser.DoesNotExist:
            return None
        except TenantUser.MultipleObjectsReturned:
            return None
        except Exception:
            return None
        
    def patch(self, request, id):
        user = self.get_object(id)
        if not user:
            return Response(data={'error': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.email_verified and user.token_valid:
            return Response(data={'error': 'user\'s email has not been verified'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            value = serializer.save()
            if type(value) == tuple:
                return Response(data={'info': 'check email for verification'}, status=status.HTTP_202_ACCEPTED)
            return Response(data={
                'data':{
                    'id': value.id,
                    'clinic_name': value.clinic_name,
                    'clinic_email': value.clinic_email,
                    'website': value.website,
                    'phonenumber': value.phonenumber,
                    'address': value.address,
                    'country': value.country,
                    'date_joined': value.date_joined.date(),
                },
                'success': 'details has been updated successfully'}, status=status.HTTP_200_OK)
        return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
    def put(self, request, id):
        user = self.get_object(id)
        print(user)
        if not user:
            return Response(data={'error': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.email_verified and user.token_valid:
            return Response(data={'error': 'user\'s email has not been verified'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            value = serializer.save()
            if type(value) == tuple:
                return Response(data={'info': 'check email for verification'}, status=status.HTTP_202_ACCEPTED) 
            return Response(data={'success': 'details has been updated successfully'}, status=status.HTTP_200_OK)
        return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])   
def verify_email_to_update(request):
    if len(request.data) > 1:
        return Response(data={'info': 'only token is allowed in the path parameter, not id data in the body parameter'})
    token = request.GET.get("token")
    id = request.data.get("id")
    if not id:
        return Response(data={'error': 'id is missing'}, status=status.HTTP_400_BAD_REQUEST)
    print(id)
    if not TenantUser.objects.filter(id=id).exists():
        return Response(data={"error": "id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    if not token:
        return Response(data={'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)
    decoded_token = decode_token_val(token)
    if not decoded_token:
        return Response(data={'error': 'invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
    email = decoded_token.get('sub') # get the email attached to the token
    if not email:
        return Response(data={'error': "Token is missing email info"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        tenant = TenantUser.objects.get(id=id)
        print("Tenant checked")
    except TenantUser.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
    except TenantUser.DoesNotExist:
        return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        return Response(data={'error': 'an error occured while verifying user\'s email'}, status=status.HTTP_400_BAD_REQUEST)  
    if not tenant.email_verified and not tenant.token_valid:
        return Response(data={'error': "user's formal email has not been verified"}, status=status.HTTP_400_BAD_REQUEST)
    tenant.clinic_email = email
    tenant.save()
    return Response(data={'success': 'email has been updated successfully'}, status=status.HTTP_202_ACCEPTED)

class DeveloperSignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if len(request.data) > 8 or len(request.data) < 8:
            return Response(data={'info': 'only clinic_email, clinic_name, website, phonenumber, country, address, password, re_enter_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DeveloperSignupSerializer(data=request.data)
        if serializer.is_valid():  
            response_data = serializer.save()
            send_dev_email(email=response_data['dev_email'])
            return Response(data={'detail': 'please check your email for verification'}, status=status.HTTP_200_OK)   
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])   
def verify_developer_email(request):
    if request.data:
        return Response(data={'info': 'only token is allowed in the path parameter, not data in the body parameter'})
    token = request.GET.get("token")
    if not token:
        return Response(data={'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)
    decoded_token = decode_token_val(token)
    if not decoded_token:
        return Response(data={'error': 'invalid or used token'}, status=status.HTTP_400_BAD_REQUEST)
    email = decoded_token.get('sub') # get the email attached to the token
    if not email:
        return Response(data={'error': "Token is missing email info"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dev = TenantUser.objects.get(clinic_email=email)
        print("Tenant checked")
    except TenantUser.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found for the email'}, status=status.HTTP_400_BAD_REQUEST)
    except TenantUser.DoesNotExist:
        return Response(data={'error': 'no account associated with this email'}, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        return Response(data={'error': 'an error occured while verifying user\'s email'}, status=status.HTTP_400_BAD_REQUEST)  
    if dev.email_verified:
        return Response(data={'error': "Developer has already been verified"}, status=status.HTTP_400_BAD_REQUEST)
    dev.email_verified = True
    dev.token_valid = True
    dev.clinic_email = email
    dev.role = "developer"
    dev.save()
    token, _ = Token.objects.get_or_create(user=dev)
    return Response(
        {'data':
            {
            'id': dev.id,
            'clinic_name': dev.clinic_name,
            'clinic_email': dev.clinic_email,
            'website': dev.website,
            'phonenumber': dev.phonenumber,
            'address': dev.address,
            'country': dev.country,
            'date_joined': dev.date_joined.date()
            },
        'token': token.key
        }, status=status.HTTP_200_OK)

class StaffSignupView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Staff.objects.all().delete()
        current_user = request.user
        print(current_user)
        try:
            tenant = TenantUser.objects.get(clinic_email=current_user)
        except TenantUser.DoesNotExist:
                return Response(data={'error': 'User who is trying to add staff does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except TenantUser.MultipleObjectsReturned:
            return Response(data={'error': 'Multiple account found with this user\'s email who is trying to add staff'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': 'user\'s email has not been verified, so user cannot add staff!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(request.data) < 5:
            return Response(data={'info': 'only username, email, position, password, re_enter_password are required as body parameters'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = StaffSignupSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.save()
            print(validated_data)
            username = validated_data['username']
            email = validated_data['email']
            position = validated_data['position']
            role = validated_data['role']
            password = validated_data['password']
            if Staff.objects.filter(username=username).exists() and Staff.objects.filter(email=email).exists():
                return Response(data={'error': 'username or email already exists!'})
            if role == 'regular':
                Staff.objects.create_user(username=username, email=email, position=position, role=role, password=password, tenant_user=tenant)
            elif role == 'admin':
                Staff.objects.create_superuser(username=username, email=email, position=position, role=role, password=password, tenant_user=tenant)
        
            validated_data.pop('password')
            send_staff_email(email=validated_data['email'])
            return Response(data={'info': 'please check your email for verification'}, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_staff_email(request):
    token = request.query_params.get('token')
    print(token)
    if request.data:
        return Response(data={'info': 'only the token is allowed as a query params, no data is allowed in the body params'}, status=status.HTTP_400_BAD_REQUEST)
    if not token:
        return Response(data={'error': 'token is required as a query params'}, status=status.HTTP_400_BAD_REQUEST)
    decoded_token = decode_token_val(token=token)
    if not decoded_token:
        return Response(data={'error': 'Invalid, or used, or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    email = decoded_token['sub']
    if not email:
        return Response(data={'error': 'token is missing an email'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        staff = Staff.objects.get(email=email)
    except Staff.DoesNotExist:
        return Response(data={'error': 'user does not exists!'}, status=status.HTTP_400_BAD_REQUEST)
    except Staff.MultipleObjectsReturned:
        return Response(data={'error': 'multiple account found with this email!'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(data={'error': 'an error occured when searching for this email'}, status=status.HTTP_400_BAD_REQUEST)
    if staff.email_verified and staff.token_valid:
        return Response(data={'error': 'this user has been verified before now'}, status=status.HTTP_400_BAD_REQUEST)
    
    staff.email_verified = True
    staff.token_valid = True
    
    if staff.role == "regular":
        try:
            view_permission = Permission.objects.get(codename="can_view_patient")
            staff.user_permissions.add(view_permission)
        except Exception as e:
            print("Error", e)
            return None
        token_exist = Token.objects.filter(user=staff.tenant_user).exists()
        if token_exist:
            Token.objects.filter(user=staff.tenant_user).delete()
        token = Token.objects.create(user=staff.tenant_user)
        staff.save()
        return Response(data={
            'data': {
                'username': staff.username,
                'email': staff.email,
                'position': staff.position,
                'role': staff.role
            },
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    elif staff.role == "admin":
        staff.email_verified = True
        staff.token_valid = True
        content_type_4_patient = ContentType.objects.get_for_model(Patient)
        try:
            all_permissions = Permission.objects.filter(content_type=content_type_4_patient,
                                      codename__in=[
                                          "can_add_patient",
                                          "can_view_patient",
                                          "can_change_patient",
                                          "can_delete_patient"
                                      ])
        except Exception as e:
            print(e)
            return None

        staff.user_permissions.set(all_permissions)
        staff.save()
        token_exist = Token.objects.filter(user=staff.tenant_user).exists()
        if token_exist:
            Token.objects.filter(user=staff.tenant_user).delete()
        token = Token.objects.create(user=staff.tenant_user)
        return Response(data={
            'data': {
                'username': staff.username,
                'email': staff.email,
                'position': staff.position,
                'role': staff.role
            },
            'token': token.key
            }, status=status.HTTP_200_OK)


# automation views

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def automation_state(request):
    if request.data:
        return Response(data={'info': 'data in the body parameter is not allowed, just the token in the header'}, status=status.HTTP_400_BAD_REQUEST)
    toggle_state = request.GET.get('s')
    automation_state, _ = AutomationState.objects.get_or_create(tenant_user=request.user)       
    if toggle_state == 'on':
        if automation_state.state:
            return Response(data={'success': 'automation is already on'}, status=status.HTTP_200_OK)
        automation_state.state = True
        automation_state.save()
    elif toggle_state == 'off':
        if not automation_state.state:
            return Response(data={'success': 'automation is already off'}, status=status.HTTP_200_OK)
        automation_state.state = False
        automation_state.save()
    else:
        return Response(data={'error': 'invalid state'}, status=status.HTTP_400_BAD_REQUEST)    
    return Response(data={'success': 'automation state has been updated', 'state': automation_state.state}, status=status.HTTP_200_OK)


class AutomationScriptsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        scripts = AutomationScript.objects.filter(tenant_user=request.user).all()
        serializer = AutomationScriptSerializer(scripts, many=True)
        if not scripts:
            return Response(data={'info': 'no automation scripts found'}, status=status.HTTP_200_OK)
        return Response(data={'success': 'automation scripts', 'scripts': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AutomationScriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'success': 'automation script has been created', 'name': serializer.data['script_name']}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AutomationScriptDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        script_id = kwargs.get('script_id')
        try:
            script = AutomationScript.objects.get(id=script_id)
        except AutomationScript.DoesNotExist:
            return Response(data={'error': 'script does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if script.tenant_user != request.user:
            return Response(data={'error': 'you are not allowed to delete this script'}, status=status.HTTP_400_BAD_REQUEST)
        script.delete()
        return Response(data={'success': 'automation script has been deleted'}, status=status.HTTP_200_OK)

