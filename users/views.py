from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm

from django.views.generic import FormView
from django.contrib.auth.views import LoginView

# Create your views here.

class UserRegistrationView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Update the model instance with the checkbox values
        instance = form.save(commit=False)
        instance.auth_age = form.cleaned_data['auth_age']
        instance.send_mail = form.cleaned_data['send_mail']
        instance.terms_conds = form.cleaned_data['terms_conds']
        instance.save()
        
        return super().form_valid(form)

class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        # Redirect to the home page or any desired URL
        return reverse_lazy('home')  # Replace 'home' with your desired URL name
