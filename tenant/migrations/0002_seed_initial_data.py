from django.db import migrations

# ✅ Directly import models
from tenant.models import TenantUser, Patient

def create_demo_tenant_and_patient(apps, schema_editor):
    # Create a demo clinic/tenant
    tenant = TenantUser.objects.create(
        clinic_name="Demo Clinic",
        clinic_email="demo@clinic.com",
        website="www.example@gmail.com",
        country="Nigeria",
        phonenumber="+2348012345678",
        subscription="Basic",
        address="Ikeja, Lagos",
        # profile_photo = "ndufkjfijfjfoijeeoni"
        password="porkDemoPass12345678",  
        email_verified = False,
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

class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_tenant_and_patient),
    ]