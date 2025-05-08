from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_data(apps, schema_editor):
    """
    Create initial data for the application.
    Using apps.get_model() to get the historical version of models.
    """
    # Get the historical version of the models
    TenantUser = apps.get_model('tenant', 'TenantUser')
    Patient = apps.get_model('tenant', 'Patient')

    # Create demo clinic/tenant
    demo_clinic = TenantUser.objects.create(
        clinic_name="Demo Clinic",
        clinic_email="demo@clinic.com",
        website="www.example.com",
        country="Nigeria",
        phonenumber="+2348012345678",
        subscription="Basic",
        location="Ikeja, Lagos",
        password=make_password("demo123456"),  # Properly hash the password
        is_active=True,
        email_verified=True,
        is_staff=False,
    )

    # Create demo patient
    Patient.objects.create(
        tenant_user=demo_clinic,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phonenumber="+2348011111111",
        date_of_birth="2000-01-01",
    )

def reverse_initial_data(apps, schema_editor):
    """
    Reverse the initial data creation.
    This is called when the migration is reversed.
    """
    TenantUser = apps.get_model('tenant', 'TenantUser')
    Patient = apps.get_model('tenant', 'Patient')
    
    # Delete in reverse order to handle foreign key constraints
    Patient.objects.filter(email="john.doe@example.com").delete()
    TenantUser.objects.filter(clinic_email="demo@clinic.com").delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_initial_data,
            reverse_initial_data,  # Provide reverse function for rollback
        ),
    ] 