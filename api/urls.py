from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.TenantRegisterView.as_view(), name='signup')
]