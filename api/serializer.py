from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from tenant.models import TenantUser

class TenantSignUpSerializer(serializers.Serializer):
    clinic_name = serializers.CharField(max_length = 255)
    clinic_email = serializers.EmailField()
    website = serializers.CharField(required=True, allow_null=True, allow_blank=True, max_length=255)
    country = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phonenumber = serializers.RegexField(max_length=16, regex=r'^\+\d{9,15}$')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        TenantUser.objects.all().delete()
        # Validates each field that are required to be unique
        if TenantUser.objects.filter(clinic_email=data['clinic_email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if TenantUser.objects.filter(phonenumber=data['phonenumber']).exists():
            raise serializers.ValidationError({'phonenumber': 'phonenumber already exist'})
        website = data['website']
        if website and TenantUser.objects.filter(website=website).exists():
            raise serializers.ValidationError({'website': 'website already exist'})
        # Checks if the password match
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'password': 'password do not match'})
        print("serializer data: ", data)
        return data

    def create(self, validated_data):
        # validated_data.pop('re_enter_password')
        # data = validated_data
        # print("1")
        # try:
        #     TenantUser.objects.create_user(clinic_name=data['clinic_name'], clinic_email=data['clinic_email'],  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'] , password=data['password'])
        #     data.pop('password')
        #     print('Tenant created')
        #     print("data:", data)
        #     return data
        # except Exception:
        #     raise serializers.ValidationError({"Error": "Account already exist with either clinic_email, clinic_name, phonenumber, or website"})
    
        validated_data.pop('re_enter_password')
        data = validated_data
        email = data['clinic_email']

        try:
            TenantUser.objects.create_user(clinic_name=data['clinic_name'], clinic_email=email,  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'] , password=data['password'])
            data.pop('password')
            return data
        except Exception:
            raise serializers.ValidationError({"Error": "Account already exist with either clinic_email, clinic_name, phonenumber, or website"})
    
class TenantLoginSerializer(serializers.Serializer):
    clinic_email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        clinic_email = data['clinic_email']
        try:
            TenantUser.objects.get(clinic_email=clinic_email)
        except TenantUser.DoesNotExist:
            raise serializers.ValidationError({'error': 'Email or password is incorrect!'})
        except TenantUser.MultipleObjectsReturned:
            raise serializers.ValidationError({'error': 'Multiple account found for this email'})
        return data
        
class TenantPasswordResetSerializer(serializers.Serializer):
    clinic_email = serializers.EmailField()

    def validate_clinic_email(self, value):
        try:
            tenant = TenantUser.objects.get(clinic_email=value)
        except TenantUser.DoesNotExist:
            return {'error': 'Email does not exist'}
        except TenantUser.MultipleObjectsReturned:
            return {'error': 'Multiple account found for this email'}
        tenant.token_valid = False            
        return value
    
class TenantPasswordConfirmResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    def validate(self, data):
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'error': "password do not match!"})
        data.pop('re_enter_password')
        print(data, "coming from serializer's class")
        return data

    