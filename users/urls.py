from django.urls import path
from .views import UserRegistrationView, MyLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),name='logout'),
]
