from django.urls import path, include
from . import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('v1/tenant/signup/', views.TenantSignupView.as_view(), name='tenant_signup'),
    
    path('v1/tenant/login/', views.TenantLoginView.as_view(), name='login'),
    path('v1/tenant/logout/', views.TenantLogoutView.as_view(), name='logout'),
    path('v1/tenant/verify-email/', views.verify_tenant_email, name='tenant_verify_email'),
    path('v1/tenant/password/reset/', views.TenantPasswordResetView.as_view(), name='tenant_password_reset'),
    path('v1/tenant/verify-password-reset-token/', views.verify_password_token, name='verify_tenant_password_token'),
    path('v1/tenant/password-reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='tenant_password_reset_confirm'),
    path('v1/tenant/verify-change-password/<str:clinic_email>/', views.TenantChangePassword.as_view(), name='tenant_password_reset_confirm'),
    path('v1/tenant/verify-email-update/', views.verify_email_to_update, name='verify_email_update'),
    # dev signup and email verification
    path('v1/dev-signup/', views.DeveloperSignupView.as_view(), name='dev_signup'),
    path('v1/verify-dev-email/', views.verify_developer_email, name='verify-dev-email'),
    # profile update for both the tenants and the devs
    path('v1/profile-update/<str:id>/', views.ProfileUpdateView.as_view()),
    # OTP for both the tenants and devs
    path('v1/get-otp/', views.get_otp),
]
