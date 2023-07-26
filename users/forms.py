from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from .models import CustomUser, City, State, Country

class CustomUserCreationForm(UserCreationForm):
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'first_name', 
                    'last_name', 'email', 'birthday', 'address', 'telephone',
                    'city', 'state', 'auth_age', 'send_mail', 'terms_conds', 'status', )

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class CityNewForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']  # Add other fields if needed

class StateNewForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name']  # Add other fields if needed

class CountryNewForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']  # Add other fields if needed