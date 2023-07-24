from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register_admin/', UserRegistrationAdminView.as_view(), name='register_admin'),
    path('register_suscriber_admin/', UserRegistrationSuscriberView.as_view(), name='register_suscriber_admin'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('email_verification', VerificateEmail.as_view(), name='email_verification'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]
