from django.db import models
from django_multitenant.mixins import TenantManagerMixin, TenantModelMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django_otp.models import Device
from django.utils.crypto import get_random_string
from django.utils import timezone
from dotenv import load_dotenv
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPConnectError, SMTPAuthenticationError
from datetime import timedelta
from datetime import date
import os, socket, uuid

load_dotenv()

class TenantUserManager(TenantManagerMixin, BaseUserManager):
    def create_user(self, clinic_name, clinic_email, website, country, phonenumber, subscription, address, password=None, **extra_fields):
        # Check if required fields are supplied
        if not clinic_email and not clinic_name and not country and not phonenumber and not address and not password:
            raise ValidationError("All fields are required")
        
        clinic_email = self.normalize_email(clinic_email)
        # Checks if tenant email already exist
        if self.model.objects.filter(clinic_email=clinic_email).exists():
            raise ValidationError("A Tenant with this email already exist!")
        user = self.model(clinic_name=clinic_name, clinic_email=clinic_email, website=website, country=country, phonenumber=phonenumber, subscription=subscription, address=address, **extra_fields)
        # Hash the password if not none
        user.set_password(password)
        # Save to database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, clinic_name, clinic_email, website, country, phonenumber, subscription, address, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Set role for developer to seperate from tenant
        extra_fields.setdefault("role", "developer") # for developers
        return self.create_user(clinic_name=clinic_name, clinic_email=clinic_email, website=website, country=country, phonenumber=phonenumber, subscription=subscription, address=address, password=password, **extra_fields)
        
class TenantUser(TenantModelMixin, AbstractUser):
    # Choices to save both tenant and developer sharing same model
    ROLES_CHOICES = [
        ("tenant", "Tenant"),
        ("developer", "Developer")
    ]
    username = None
    email = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = "id"
    clinic_name = models.CharField(max_length=255, null=False, blank=False)
    clinic_email = models.EmailField(null=False, blank=False, unique=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False)
    phonenumber = models.CharField(max_length=16, null=False, blank=False, unique=True, validators=[RegexValidator(regex=r'^\+\d{9,15}$')])
    address  = models.TextField(null=False, blank=False)
    subscription = models.CharField(max_length=50, null=False, blank=False, default="Basic")
    email_verified = models.BooleanField(default=False)
    phonenumber_verified = models.BooleanField(default=False)
    token_valid = models.BooleanField(default=False)
    role = models.CharField(max_length=9, choices=ROLES_CHOICES, default="tenant")
    is_active = models.BooleanField(default=True)
    # Set default to false incase it is a tenant data
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "clinic_email"
    REQUIRED_FIELDS = ["clinic_name", "website", "country", "phonenumber", "location"]

    objects = TenantUserManager()

    # Strip for white spaces and set for organized data
    def save(self, *args, **kwargs):
        self.clinic_name = self.clinic_name.strip().title()
        self.clinic_email = self.clinic_email.strip().lower()
        if self.website:
            self.website = self.website.strip().lower()
        self.country = self.country.strip().capitalize()
        self.address = self.address.strip().capitalize()
        self.subscription = self.subscription.strip().capitalize()
        super().save(*args, **kwargs)

    # String representation of the object
    def __str__(self):
        return self.clinic_email

class Patient(TenantModelMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_user = models.ForeignKey(TenantUser, on_delete=models.CASCADE, related_name="patients")
    tenant_id = "tenant_user_id"
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    # Not all patients will have an email address
    email = models.EmailField(null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=False, blank=False, validators=[RegexValidator(regex=r'^\+?\d{9,15}$')])
    date_of_birth = models.DateField(null=False)

    # Enforce uniqueness between tenant and patient.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant_user", "id"], name="unique_patient_id_per_tenant"), # Human readable name for migration
            models.UniqueConstraint(fields=["tenant_user", "phonenumber"], name="unique_patient_phone_per_tenant"), # Human readable name for migration
            models.UniqueConstraint(fields=["tenant_user", "email"], condition=Q(email__isnull=False), name="unique_patient_email_per_tenant") # Human readable name for migration and only enforce uniqueness if email is not null
        ]

        # Set permissions for tenants over ther patients
        permissions = [
            ("can_add_patient", "Can add patient"),
            ("can_change_patient", "Can change patient"),
            ("can_view_patient", "Can view patient"),
            ("can_delete_patient", "Can delete patient")
        ]

    # Validates to make sure the patient date of birth is not in future.
    def clean(self):
        if self.date_of_birth > date.today():
            raise ValidationError(
                {"date_of_birth": "Date of Birth cannot be in the future!"}
            )
        return super().clean()

    # Strip for white spaces and set for organized data
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip().capitalize()
        self.last_name = self.last_name.strip().capitalize()
        if self.email:
            self.email = self.email.strip().lower()
        else:
            self.email = None
        super().save(*args, **kwargs)

    # String representation of the object
    def __str__(self):
        return f"{self.first_name.strip().capitalize()} {self.last_name.strip().capitalize()}"     
class EmailDeviceOTP(Device, TenantModelMixin):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name="otp")
    tenant_id = "user_id"
    name = None
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    valid_until = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp_code = get_random_string(length=int(os.getenv("OTP_LENGTH")), allowed_chars=os.getenv("OTP_CHARACTERS"))
        self.valid_until = timezone.now() + timedelta(minutes=int(os.getenv("TOKEN_EXPIRATION")))
        super().save()
        subject = "OTP (One Time Password)"
        html_content = render_to_string(
            template_name="api/otp.html",
            context={'OTP': self.otp_code, 'subject': subject}
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=os.getenv("EMAIL_HOST_USER"),
            to=[self.user.clinic_email]
        )
        msg.attach_alternative(content=html_content, mimetype="text/html")

        try:
            msg.send()
        except SMTPAuthenticationError:
            print("SMTP Authentication failed. Check your email credentials.")
        except SMTPConnectError:
            print("Failed to connect to the SMTP server. Is it reachable?")
        except SMTPRecipientsRefused:
            print("Recipient address was refused by the server.")
        except SMTPSenderRefused:
            print("Sender address was refused by the server.")
        except SMTPDataError:
            print("SMTP server replied with an unexpected error code (data issue).")
        except SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except socket.gaierror:
            print("Network error: Unable to resolve SMTP server.")
        except socket.timeout:
            print("Network error: SMTP server timed out.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
   
    def verify_token(self):
        print(self.valid_until)
        if timezone.now() > self.valid_until:
            return True
        return False
    
class TenantStaffManager(TenantManagerMixin, BaseUserManager):
    def create_user(self, username, email, position, role, password=None, **extrafields):
        if not any([username, email, position, role]):
            raise ValidationError("This field cannot be empty")
        email = self.normalize_email(email=email)
        if self.model.objects.filter(email=email).exists() or self.model.objects.filter(username=username).exists():
            raise ValidationError("email or username already exist!")
        user = self.model(username=username, email=email, role=role, position=position, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, role, position, password=None, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)
        extrafields.setdefault("role", "admin")
        return self.create_user(username=username, email=email, position=position,password=password, **extrafields)
        
class Staff(TenantModelMixin, AbstractUser):
    ROLE = [
        ("regular", "regular"),
        ("admin", "admin")
    ]
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_user = models.ForeignKey(TenantUser, on_delete=models.CASCADE, related_name="staff")
    tenant_id = "tenant_user_id"
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    position = models.CharField(max_length=255, null=False, blank=False)
    role = models.CharField(max_length=12, null=False, blank=False, choices=ROLE, default=ROLE[0])
    email_verified = models.BooleanField(default=False)
    token_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "position"]

    groups = models.ManyToManyField(
        Group,
        related_name="tenant_staff_groups",  # Make it unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="tenant_staff_permissions",  # Make it unique
        blank=True
    )

    objects = TenantStaffManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant_user", "id"], name="unique_staff_id_per_tenant"), # Human readable name for migration
            models.UniqueConstraint(fields=["tenant_user", "email"], name="unique_staff_email_per_tenant") # Human readable name for migration and only enforce uniqueness if email is not null
        ]

        # Set permissions for tenants over ther patients
        permissions = [
            ("can_add_staff", "Can add staff"),
            ("can_change_staff", "Can change staff"),
            ("can_view_staff", "Can view staff"),
            ("can_delete_staff", "Can delete staff")
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        self.username = self.username.strip().lower()
        self.position = self.position.strip().title()
        self.role = self.role.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    

    

