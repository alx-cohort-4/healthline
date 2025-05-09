from django.urls import path, include
from . import views
urlpatterns = [
    path('signup/', views.TenantSignupView.as_view(), name='signup'),
    path('login/', views.TenantLoginView.as_view(), name='login'),
    path('logout/', views.TenantLogoutView.as_view(), name='logout'),
    path('password/reset/', views.TenantPasswordResetView.as_view(), name='password_reset'),
    path('verify-email/<str:token>/', views.verify_email, name="verify_email"),
    path('reset/confirm/<str:clinic_email>/', views.TenantConfirmResetPasswordView.as_view(), name='reset_confirm')
]