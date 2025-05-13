from django.urls import path
from . import views
urlpatterns = [
    path('v1/tenant/signup/', views.TenantSignupView.as_view(), name='tenant_signup'),
    path('v1/tenant/login/', views.TenantLoginView.as_view(), name='login'),
    path('v1/tenant/logout/', views.TenantLogoutView.as_view(), name='logout'),
    path('v1/tenant/verify-email/', views.verify_tenant_email, name='tenant_verify_email'),
    path('v1/tenant/password/reset/', views.TenantPasswordResetView.as_view(), name='tenant_password_reset'),
    path('v1/tenant/verify-password-reset-token/', views.verify_password_token, name='verify_tenant_password_token'),
    path('v1/tenant/password-reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='tenant_password_reset_confirm'),
    path('v1/tenant/verify-change-password/<str:clinic_email>/', views.TenantChangePassword.as_view(), name='tenant_password_reset_confirm')
]