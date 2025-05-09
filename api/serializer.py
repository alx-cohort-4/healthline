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
        validated_data.pop('re_enter_password')
        data = validated_data
        print("In here")
        try:
            TenantUser.objects.create_user(clinic_name=data['clinic_name'], clinic_email=data['clinic_email'],  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'] , password=data['password'])
            data.pop('password')
            return data
        except Exception:
            raise serializers.ValidationError({"Error": "Account already exist with either clinic_email, clinic_name, phonenumber, or website"})
    
class TenantLoginSerializer(serializers.Serializer):
    clinic_email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        clinic_email = data['clinic_email']
        tenant = TenantUser.objects.filter(clinic_email=clinic_email)
        if tenant:
            return data
        raise serializers.ValidationError({'Error': 'Email or password is incorrect!'})
    
    # def update(self, instance, validated_data):
    #     instance.clinic_name = validated_data.get('clinic_name', instance.clinic_name)
    #     instance.clinic_email = validated_data.get('clinic_email', instance.clinic_email)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.phonenumber = validated_data.get('phonenumber', instance.phonenumber)
    #     instance.subscription = validated_data.get('subscription', instance.subscription)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.website = validated_data.get('website', instance.website)
    #     return instance

class TenantPasswordResetSerializer(serializers.Serializer):
    clinic_email = serializers.EmailField()

    def validate_clinic_email(self, value):
        if not TenantUser.objects.filter(clinic_email=value).exists():
            return {'error': 'Email does not exist'}
        return value
    
class TenantPasswordConfirmResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    re_enter_password = serializers.CharField(max_length=255)

    def validate(self, data):
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'error': "password do not match!"})
        data.pop('re_enter_password')
        print(data, "coming from serializer's class")
        return data

    
        
        