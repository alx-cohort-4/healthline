from rest_framework import serializers
from rest_framework.authtoken.models import Token
from tenant.models import TenantUser, Staff
from .tasks import send_email_for_update

class TenantSignUpSerializer(serializers.Serializer):
    clinic_name = serializers.CharField(max_length = 255)
    clinic_email = serializers.EmailField()
    website = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=255)
    country = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phonenumber = serializers.RegexField(max_length=16, regex=r'^\+\d{9,15}$')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        # TenantUser.objects.all().delete()
        Token.objects.all().delete()
        # Validates each field that are required to be unique
        if TenantUser.objects.filter(clinic_email=data['clinic_email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if TenantUser.objects.filter(phonenumber=data['phonenumber']).exists():
            raise serializers.ValidationError({'phonenumber': 'phonenumber already exist'})
        if len(data['password']) < 8  or len(data['re_enter_password']) < 8:
            raise serializers.ValidationError({'password_length': 'minimum length of password required is 8'})
        # Check if the password match
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'password': 'password do not match'})
        return data

    def create(self, validated_data):
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
        Token.objects.filter(user=tenant).delete()
        tenant.token_valid = False
        tenant.save()            
        return value
    
class TenantPasswordConfirmResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    def validate(self, data):
        if len(data['password']) < 8 or len(data['re_enter_password']) < 8:
            raise serializers.ValidationError({'password_length': 'minimum length of password required is 8'})
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'error': "password do not match!"})
        data.pop('re_enter_password')
        print(data, "coming from serializer's class")
        return data

class TenantPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    def validate(self, data):
        if len(data['new_password']) < 8 or len(data['confirm_new_password']) < 8:
            raise serializers.ValidationError({'password_length': 'minimum length of password required is 8'})
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'error': 'the two new passwords do not match'})
        data.pop('confirm_new_password')
        return data
    
class ProfileUpdateSerializer(serializers.Serializer):
    clinic_name = serializers.CharField(max_length = 255, required=False, allow_null=True, allow_blank=True)
    clinic_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    website = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    phonenumber = serializers.RegexField(max_length=16, regex=r'^\+\d{9,15}$', required=False, allow_null=True, allow_blank=True)

    def validate(self, data):
        if not any(value for value in data.values() if value not in [None, ""]):
            raise serializers.ValidationError('Profile details cannot be empty')
        return data
      
    def update(self, instance, validated_data):
        new_email = validated_data.get('clinic_email')
        if new_email not in [None, ""] and new_email != instance.clinic_email:
            if TenantUser.objects.filter(clinic_email=new_email).exists():
                return serializers.ValidationError("You can not use this email to update")
            
            # Trigger email verification
            send_email_for_update(email=new_email)
            return (validated_data, "email_for_verification")
        # Track whether anything was updated
        updated_profile = False
        
        for key, value in validated_data.items():
            if value not in [None, ""]:
                setattr(instance, key, value)
                updated_profile = True
        if updated_profile:
            instance.save()
            return instance
        return serializers.ValidationError("No changes detected!")
        
class DeveloperSignupSerializer(serializers.Serializer):
    dev_name = serializers.CharField(max_length = 255)
    dev_email = serializers.EmailField()
    website = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=255)
    country = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phonenumber = serializers.RegexField(max_length=16, regex=r'^\+\d{9,15}$')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        TenantUser.objects.all().delete()
        Token.objects.all().delete()
        # Validates each field that are required to be unique
        print(data['dev_email'])
        if TenantUser.objects.filter(clinic_email=data['dev_email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if TenantUser.objects.filter(phonenumber=data['phonenumber']).exists():
            raise serializers.ValidationError({'phonenumber': 'phonenumber already exist'})
        if len(data['password']) < 8  or len(data['re_enter_password']) < 8:
            raise serializers.ValidationError({'password_length': 'minimum length of password required is 8'})
        # Check if the password match
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'password': 'password do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('re_enter_password')
        data = validated_data
        email = data['dev_email']
        try:
            TenantUser.objects.create_superuser(clinic_name=data['dev_name'], clinic_email=email,  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'], password=data['password'])
            data.pop('password')
            return data
        except Exception:
            raise serializers.ValidationError({"Error": "Account already exist with either clinic_email, clinic_name, phonenumber, or website"})
             
class StaffSignupSerializer(serializers.Serializer):
    # Staff.objects.all().delete()
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    position = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    re_enter_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if len(data['username']) < 3:
            raise serializers.ValidationError({'name_error': 'length of name must be greater than 2!'})
        if len(data['position']) < 3:
            raise serializers.ValidationError({'position_error': 'length of the position must be greater than 2!'})
        if data['role'].lower() not in ["admin", "regular"]:
            raise serializers.ValidationError({'role': 'role must be set to admin or regular!'})
        if len(data['password']) < 8 or len(data['re_enter_password']) < 8:
            raise serializers.ValidationError({'password_length': 'length of password must be greater than or equal to 8!'})
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'mismatch': 'passwords do not match!'})
        data.pop('re_enter_password')
        return data
    
    def create(self, validated_data):
        return validated_data
    

        