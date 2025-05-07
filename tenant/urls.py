from django.urls import path
from . import views

app_name = "tenant" 

urlpatterns = [
    path('home/', views.HomeView.as_view(), name="home"),
    path('signup/', views.SignupPage.as_view(), name="signup"),
    path('login/', views.LoginPage.as_view(), name="login"),
    path('add_patient/', views.PatientFormView.as_view(), name="add_patient"),
    path('verify_email/', views.testing, name="verify_email"),
    path('verify/', views.VerifyEmailComplete, name="email_verify_complete"),
    path('logout/', views.logout_user, name="logout"),
]