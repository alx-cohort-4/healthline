from django.db import models
from django_multitenant.mixins import TenantManagerMixin, TenantModelMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from datetime import date
import uuid

class TenantUserManager(TenantManagerMixin, BaseUserManager):
    def create_user(self, clinic_name, clinic_email, website, country, phonenumber, subscription, location, password=None, **extra_fields):
        # Check if required fields are supplied
        if not all([clinic_name, clinic_email, website, country, phonenumber, location, password]):
            raise ValidationError("All fields are required")
        
        clinic_email = self.normalize_email(clinic_email)
        # Checks if tenant email already exist
        if self.model.objects.filter(clinic_email=clinic_email).exists():
            raise ValidationError("A Tenant with this email already exist!")
        user = self.model(clinic_name=clinic_name, clinic_email=clinic_email, website=website, country=country, phonenumber=phonenumber, subscription=subscription, location=location, **extra_fields)
        # Hash the password if not none
        user.set_password(password)
        # Save to database
        user.save(using=self._db)
        return user
    
    def create_superuser(self, clinic_name, clinic_email, website, country, phonenumber, subscription, location, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Set role for developer to seperate from tenant
        extra_fields.setdefault("role", "developer") # for developers
        return self.create_user(clinic_name=clinic_name, clinic_email=clinic_email, website=website, country=country, phonenumber=phonenumber, subscription=subscription, location=location, password=password, **extra_fields)
        
class TenantUser(TenantModelMixin, AbstractUser):
    # Choices to save both tenant and developer sharing same model
    ROLES_CHOICES = [
        ("tenant", "Tenant"),
        ("developer", "Developer")
    ]
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = "id"
    clinic_name = models.CharField(max_length=255, null=False, blank=False)
    clinic_email = models.EmailField(null=False, blank=False, unique=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False)
    phonenumber = models.CharField(max_length=15, null=False, blank=False, unique=True, validators=[RegexValidator(regex=r'^\+?\d{9,15}$')])
    location  = models.TextField(null=False, blank=False)
    subscription = models.CharField(max_length=50, null=False, blank=False, default="Basic")
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
        self.location = self.location.strip().capitalize()
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

    # Enforce uniqueness between tenant and pateint.
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
                {"date of birth": "Date of Birth cannot be in the future!"}
            )
        return super().clean()

    # Strip for white spaces and set for organized data
    def save(self, *args, **kwargs):
        self.full_clean()
        self.first_name = self.first_name.strip().capitalize()
        self.last_name = self.last_name.strip().capitalize()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    # String representation of the object
    def __str__(self):
        return f"{self.first_name} {self.last_name}"     