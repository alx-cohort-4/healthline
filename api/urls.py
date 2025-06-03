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
    # tenant's staff signup and email verification
    path('v1/tenant-staff/signup/', views.StaffSignupView.as_view()),
    path('v1/verify-staff-email/', views.verify_staff_email),
    # dev signup and email verification
    path('v1/dev-signup/', views.DeveloperSignupView.as_view(), name='dev_signup'),
    path('v1/verify-dev-email/', views.verify_developer_email, name='verify-dev-email'),
    # profile update for both the tenants and the devs
    path('v1/profile-update/<str:id>/', views.ProfileUpdateView.as_view()),
    # OTP for both the tenants and devs
    path('v1/get-otp/', views.get_otp),

    # automation routes
    # path('v1/tenant/automation/settings/', views.AutomationSettingsView.as_view(), name='automation_settings'),
    path('v1/tenant/automation/state/', views.automation_state, name='automation_state'),       
    path('v1/tenant/automation/scripts/', views.AutomationScriptsView.as_view(), name='automation_scripts'),
    path('v1/tenant/automation/scripts/delete/<str:script_id>/', views.AutomationScriptDeleteView.as_view(), name='automation_script_delete'),
    # path('v1/tenant/automation/scripts/<str:script_id>/', views.AutomationScriptDetailView.as_view(), name='automation_script_detail'),
    # path('v1/tenant/automation/schedule/', views.AutomationScheduleView.as_view(), name='automation_schedule'),
    # path('v1/tenant/automation/test/', views.TestConnectionView.as_view(), name='test_simulation'),
]
