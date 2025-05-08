from rest_framework import serializers
from tenant.models import TenantUser

class TenantSerializer(serializers.Serializer):
    clinic_name = serializers.CharField(required=True, label="HealthCare Name", max_length = 255)
    clinic_email = serializers.EmailField(required=True, label="Email Address")
    website = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=255)
    country = serializers.CharField(required=True, max_length=255)
    address = serializers.CharField(required=True, max_length=255)
    phonenumber = serializers.RegexField(required=True, max_length=16, regex=r'^\+\d{9,15}$')
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

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
        TenantUser.objects.create_user(clinic_name=data['clinic_name'], clinic_email=data['clinic_email'],  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'] , password=data['password'])
        data.pop('password')
        return data