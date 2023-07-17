from django.urls import path
from .views import UserRegistrationView, MyLoginView, VerificateEmail
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('email_verification', VerificateEmail.as_view(), name='email_verification'), 
]
