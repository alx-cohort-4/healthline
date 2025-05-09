from django.urls import path
from . import views
urlpatterns = [
    path("v1/tenant/verify-email/", views.verify_email, name="verify_email"),
    path("v1/tenant/verify-email-complete/", views.verify_email_complete, name="verify_email_complete"),
    path('signup/', views.TenantSignupView.as_view(), name='signup'),
    path('login/', views.TenantLoginView.as_view(), name='login'),
    path('logout/', views.TenantLogoutView.as_view(), name='logout')
]