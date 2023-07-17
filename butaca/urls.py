from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
]
