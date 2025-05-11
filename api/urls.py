from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/tenant/signup/', views.TenantSignupView.as_view(), name='signup'),
    path('v1/tenant/login/', views.TenantLoginView.as_view(), name='login'),
    path('v1/tenant/logout/', views.TenantLogoutView.as_view(), name='logout'),
    path("v1/tenant/verify-email-complete/", views.VerifyEmailCompleteView.as_view(), name="verify_email_complete"),
    path('v1/tenant/verify-password-reset-token/', views.VerifyPasswordTokenView.as_view(), name='verify_token'),
    path('v1/tenant/reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='reset_confirm'),
    path('v1/tenant/password/reset/', views.TenantPasswordResetView.as_view(), name='password_reset'),
    path('v1/tenant/reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='reset_confirm')

    # path('v1/verify-email/<str:token>/', views.verify_tenant_email, name='verify_email'),
    # path('v1/verify-password-reset-token/<str:token>/', views.verify_password_token, name='verify_token'),
    # path("v1/tenant/verify-email/", views.VerifyEmailView.as_view(), name="verify_email"),
    # path('signup/', views.TenantSignupView.as_view(), name='signup'),
    # path('login/', views.TenantLoginView.as_view(), name='login'),
    # path('logout/', views.TenantLogoutView.as_view(), name='logout'),
    # path('password/reset/', views.TenantPasswordResetView.as_view(), name='password_reset'),
    # path('reset/verify-email/<str:token>/', views.verify_email, name="verify_email"),
]