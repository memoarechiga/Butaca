from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'first_name', 
                    'last_name', 'email', 'birthday', 'address', 'telephone',
                    'city', 'state', 'auth_age', 'send_mail', 'terms_conds'  )
