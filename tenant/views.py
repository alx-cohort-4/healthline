from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404
from datetime import date
import os, jwt
from .models import TenantUser, Patient
# from .token import send_email
from .tasks import send_email
from . import forms

class HomeView(LoginRequiredMixin, generic.ListView, FormView):
    login_url = settings.LOGIN_URL
    redirect_field_name = None
    template_name = "tenant/home.html"
    form_class = forms.PatientForm
    model = Patient
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        user = self.request.user.clinic_name
        context = super().get_context_data(**kwargs)
        context['name'] = user
        return context 
    
    def get_queryset(self):
        try:
            # Ensure that tenant really exist
            tenant = TenantUser.objects.get(clinic_email=self.request.user)
        except TenantUser.DoesNotExist:
            raise Http404("Tenant does not exist")
        return Patient.objects.filter(tenant_user=tenant)
    
def testing(request):
    email = request.user.clinic_email
    username = request.user.clinic_name
    send_email.delay(email=email, user=username)
    return render(request, "tenant/email_message.html", {'email': email, 'name': username})

class SignupPage(FormView):
    template_name = "tenant/sign_up.html"
    form_class = forms.TenantUserForm
    success_url = reverse_lazy("tenant:home")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Successfully logged in as {user.clinic_name}")
        
        # Send verification email
        email = user.clinic_email
        username = user.clinic_name
        send_email.delay(email=email, user=username)
        return render(self.request, "tenant/email_message.html", {'email': email, 'name': username})
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form(self.form_class)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         print("Logged user in")
    #         messages.success(request, message=f"Successfully logged in as {user.clinic_name}")
    #         return testing()
    #         return redirect(reverse_lazy(self.success_url))
    #     print(form.errors)
    #     return super().post(request, *args, **kwargs)
    
class LoginPage(FormView):
    template_name = "tenant/login.html"
    form_class = forms.LoginForm
    success_url = "tenant:home"

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            email = form.cleaned_data.get('clinic_email')
            password = form.cleaned_data.get('password')
            print(email, password)
            user = authenticate(request, clinic_email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, message=f"Successfully logged in as {user.clinic_name}")
                return redirect(reverse_lazy(self.success_url))
            messages.error(request, message="Email or password is incorrect")
        return self.form_invalid(form)

class PatientFormView(LoginRequiredMixin, FormView):
    template_name = "tenant/home.html"
    form_class = forms.PatientForm
    success_url = "tenant:home"
    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        tenant = request.user.clinic_name
        tenant_exist = TenantUser.objects.filter(clinic_name=tenant).exists()
        if tenant_exist:
            tenant_data = TenantUser.objects.get(clinic_name=tenant)
            if form.is_valid():
                phonenumber = form.cleaned_data.get('phonenumber')
                # Check if patient with this phone number exists in this tenant
                if Patient.objects.filter(phonenumber=phonenumber, tenant_user=tenant_data).exists():
                    messages.error(self.request, "Patient with this phone number already exists.")
                    return self.form_invalid(form)
                # Else save to database
                patient = form.save(commit=False)
                patient.tenant_user = tenant_data
                patient.save()
                messages.success(request, message=f"{patient} has been added to list successfully")
                return redirect(reverse_lazy(self.success_url))
        return super().post(request, *args, **kwargs)
    
def VerifyEmailComplete(request):
    token = request.GET.get("token")
    with open('public.pem', 'r') as pub_file:
        public_key = pub_file.read()
    try:
        payload = jwt.decode(token, public_key, os.getenv('ALGO'))
        user = payload.get("sub")
    except jwt.ExpiredSignatureError:
        return HttpResponse("Token has expired", status=400)
    except jwt.InvalidTokenError:
        return HttpResponse("Invalid token", status=400)
    
    try:
        user_exists = TenantUser.objects.get(clinic_email=user)
        if user_exists:
            # print("User Exists")
            # from django.contrib.auth import login
            # login(request, user_exists)
            return redirect("tenant:home")
    except TenantUser.DoesNotExist:
        return HttpResponse("Tenant does not exist", status=404)
    # res =verify_email.delay(token)
    # try:
    # return HttpResponse(res)
    
@login_required
def logout_user(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)