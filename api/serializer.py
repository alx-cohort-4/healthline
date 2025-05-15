from rest_framework import serializers
from rest_framework.authtoken.models import Token
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
        """
        Validates each field that are required to be unique (clinic_email, phonenumber, website) and checks if the password and re-entered password matches.

        :param data: A dictionary containing the data to be validated
        :raises serializers.ValidationError: If any of the required fields already exist
        :return: The validated data
        """
        # Validates each field that are required to be unique
        if TenantUser.objects.filter(clinic_email=data['clinic_email']).exists():
            raise serializers.ValidationError({'email': 'email already exist'})
        if TenantUser.objects.filter(phonenumber=data['phonenumber']).exists():
            raise serializers.ValidationError({'phonenumber': 'phonenumber already exist'})
        website = data['website']
        if website and TenantUser.objects.filter(website=website).exists():
            raise serializers.ValidationError({'website': 'website already exist'})
        if len(data['password']) < 8  or len(data['re_enter_password']) < 8:
            raise serializers.ValidationError({'password_length': 'minimum length of password required is 8'})
        # Checks if the password match
        if data['password'] != data['re_enter_password']:
            raise serializers.ValidationError({'password': 'password do not match'})
        print("done")
        print("serializer data: ", data)
        return data

    def create(self, validated_data):
        """
        Creates a new tenant user with the provided validated data after ensuring the password
        confirmation field is removed and the password is hashed. If account creation fails due
        to existing unique fields (clinic_email, clinic_name, phonenumber, or website), it raises
        a ValidationError.

        :param validated_data: A dictionary containing validated data from the serializer
        :return: The validated data without the password field
        :raises serializers.ValidationError: If an account already exists with unique field conflicts
        """
        validated_data.pop('re_enter_password')
        data = validated_data
        email = data['clinic_email']
        print("I am in create function")
        try:
            TenantUser.objects.create_user(clinic_name=data['clinic_name'], clinic_email=email,  country=data['country'], phonenumber=data['phonenumber'], address=data['address'], subscription='Basic', website=data['website'] , password=data['password'])
            data.pop('password')
            return data
        except Exception:
            raise serializers.ValidationError({"Error": "Account already exist with either clinic_email, clinic_name, phonenumber, or website"})
        
    def update(self, instance, validated_data):
        instance.clinic_name = validated_data.get('clinic_name', instance.clinic_name)
        print(instance.clinic_name)
        return instance
        
class TenantLoginSerializer(serializers.Serializer):
    clinic_email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Validates the provided data for tenant login by checking if a tenant with the given
        clinic_email exists. If a tenant is found, the data is returned as valid. Otherwise,
        raises a ValidationError indicating that the email or password is incorrect.

        :param data: A dictionary containing the login data to be validated, which includes 'clinic_email'.
        :raises serializers.ValidationError: If no tenant is found with the provided clinic_email.
        :return: The validated data if the clinic_email exists in the database.
        """
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
        """
        Validates the provided clinic_email by checking if a tenant with the given
        clinic_email exists in the database. If the email does not exist, it raises a
        ValidationError with a message "Email does not exist". If the email exists,
        it returns the validated value.

        :param value: The clinic_email to be validated.
        :raises serializers.ValidationError: If the email does not exist in the database.
        :return: The validated value if the email exists in the database.
        """
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
        """
        Validates the password fields by ensuring that the 'password' and 're_enter_password'
        fields match. If they do not match, a ValidationError is raised. The 're_enter_password'
        field is then removed from the data dictionary before returning the validated data.

        :param data: A dictionary containing the data to be validated, which includes 'password'
                    and 're_enter_password'.
        :raises serializers.ValidationError: If the 'password' and 're_enter_password' fields do not match.
        :return: The validated data with the 're_enter_password' field removed.
        """
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
    
class TenantUpdateSerializer(serializers.Serializer):
    clinic_name = serializers.CharField(max_length = 255)
    clinic_email = serializers.EmailField()
    website = serializers.CharField(required=True, allow_null=True, allow_blank=True, max_length=255)
    country = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phonenumber = serializers.RegexField(max_length=16, regex=r'^\+\d{9,15}$')