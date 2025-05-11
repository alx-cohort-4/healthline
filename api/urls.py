from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/signup/', views.TenantSignupView.as_view(), name='signup'),
    path('v1/login/', views.TenantLoginView.as_view(), name='login'),
    path('v1/logout/', views.TenantLogoutView.as_view(), name='logout'),
    path('v1/verify-email/<str:token>/', views.verify_tenant_email, name='verify_email'),
    path('v1/password/reset/', views.TenantPasswordResetView.as_view(), name='password_reset'),
    path('v1/verify-password-reset-token/<str:token>/', views.verify_password_token, name='verify_token'),
    path('v1/reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='reset_confirm')
]