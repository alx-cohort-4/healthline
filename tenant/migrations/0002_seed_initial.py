from django.db import migrations

# ✅ Directly import models
from tenant.models import TenantUser, Patient, EmailDeviceOTP, Staff, AutomationScript, AutomationState

def create_demo_tenant_and_patient(apps, schema_editor):
    # Create a demo clinic/tenant
    tenant = TenantUser.objects.create_user(
        clinic_name="Demo Clinic",
        clinic_email="demo@clinic.com",
        website="www.example@gmail.com",
        country="Nigeria",
        phonenumber="+2348012345678",
        subscription="Basic",
        address="Ikeja, Lagos",
        password="porkDemoPass12345678",  
        email_verified = False,
        token_valid = False,
        is_active=True,
        is_staff=False,
    )

    # Create a demo patient under the tenant
    Patient.objects.create(
        tenant_user=tenant,  # ForeignKey to Tenant
        first_name="John",
        last_name="Doe",
        email="test@patient.com",
        phonenumber="+2348011111111",
        date_of_birth="2000-01-01",
    )

    # Otp for tenant email
    EmailDeviceOTP.objects.create(
        user = tenant,
        otp_code = "667744",
        valid_until = "2050-01-01"
    )

    # Tenant Staff
    Staff.objects.create_user(
        tenant_user=tenant,
        username="limah",
        email="limah@gmail.com",
        position="doctor",
        role="admin_user",
        password="limah1234",
        email_verified = False,
        token_valid = False,
        is_active=True,
        is_staff=False,
    )

    # Automation state
    AutomationState.objects.create(
        tenant_user=tenant,
        state=False,
    )

    # Automation script
    AutomationScript.objects.create(
        tenant_user=tenant,
        script_name="Surgery",
        script_code="Hello Mrs. Patience, your surgery will begin tommorow.",
        created_at="2025-06-10",
        updated_at="2025-06-15"
    )

class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_tenant_and_patient),
    ]