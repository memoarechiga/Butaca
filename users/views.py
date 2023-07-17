from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .decorators import user_not_authenticated
from .tokens import account_activation_token

from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView

# Create your views here.

def activate(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(user_id=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Email confirmado!, ya puedes acceder a tu cuenta.")
        return redirect('login')
    else:
        messages.error(request, "Link de activación invalido")

    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("users/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        pass
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@method_decorator(user_not_authenticated, name='dispatch')
class UserRegistrationView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            instance.auth_age = form.cleaned_data['auth_age']
            instance.send_mail = form.cleaned_data['send_mail']
            instance.terms_conds = form.cleaned_data['terms_conds']
            instance.is_active = False  # Set the user as inactive until email verification
            instance.save()

            activateEmail(self.request, instance, form.cleaned_data.get('email'))  # Pass the email value as 'to_email'

            
        except Exception as e:
            messages.error(self.request, f'Error occurred: {str(e)}')
            return super().form_invalid(form)

        return super().form_valid(form)

@method_decorator(user_not_authenticated, name='dispatch')
class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        # Redirect to the home page or any desired URL
        return reverse_lazy('home')  # Replace 'home' with your desired URL name
