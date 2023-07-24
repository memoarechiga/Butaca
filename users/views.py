from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, SetPasswordForm, PasswordResetForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q

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
    mail_subject = "Activa tu cuenta."
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
    success_url = reverse_lazy('email_verification')

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
            messages.error(request, "Algo salio mal")
            messages.error(self.request, f'Error occurred: {str(e)}')
            return super().form_invalid(form)

        return super().form_valid(form)


class UserRegistrationAdminView(LoginRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register_admin.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            instance.status = "Promotor"
            instance.save()
            
        except Exception as e:
            messages.error(request, "Algo salio mal")
            messages.error(self.request, f'Error occurred: {str(e)}')
            return super().form_invalid(form)

        return super().form_valid(form)


class UserRegistrationSuscriberView(LoginRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register_suscriber_admin.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            instance.save()
            
        except Exception as e:
            messages.error(request, "Algo salio mal")
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
        user = self.request.user
        if user.is_authenticated:
            if user.status == 'admin':  
                return reverse_lazy('dashboard')  
            elif user.status == 'Promotor':  
                return reverse_lazy('dashboard_promoter') 
            else:
                return reverse_lazy('dashboard_user')  # Default dashboard URL for other authenticated users
        else:
            return reverse_lazy('login')  # Redirect to login if the user is not authenticated

@method_decorator(login_required, name='dispatch')
class VerificateEmail(TemplateView):
    template_name = 'verification_email.html'



@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = CustomUser.objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Solicitud de Restablecimiento de Contraseña"
                message = render_to_string("users/template_password_reset.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

        #for key, error in list(form.errors.items()):
        #    if key == 'captcha' and error[0] == 'This field is required.':
        #        messages.error(request, "You must pass the reCAPTCHA test")
        #        continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="users/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(user_id=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")