from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import TenantUser, Patient

class TenantUserForm(UserCreationForm):
    clinic_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Healthcare Facility Name")
    clinic_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Faculty email")
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phonenumber = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label ="Password")
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label ="Confirm password")

    class Meta:
        model = TenantUser
        fields = ['clinic_name', 'clinic_email', 'website', 'country', 'phonenumber', 'location']

class LoginForm(forms.Form):
    clinic_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label="Faculty Email")
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Email can be optional")
    phonenumber = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))

    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "email", "phonenumber", "date_of_birth"]