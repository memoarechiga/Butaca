from django.shortcuts import render
from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'

@method_decorator(login_required, name='dispatch')
class Dashboard(TemplateView):
    template_name = 'butaca/dashboard.html'

