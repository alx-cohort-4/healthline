from django.urls import path
from . import views
urlpatterns = [
    path("v1/tenant/verify-email/", views.verify_email, name="verify_email"),
    path("v1/tenant/verify-email-complete/", views.verify_email_complete, name="verify_email_complete"),
]