from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Event)
admin.site.register(DateEvent)
admin.site.register(DrawTicket)
admin.site.register(Winner)