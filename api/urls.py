from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.TenantSignupView.as_view(), name='signup'),
    path('login/', views.TenantLoginView.as_view(), name='login'),
    path('logout/', views.TenantLogoutView.as_view(), name='logout')
]