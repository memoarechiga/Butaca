from django.contrib import admin
from .models import CustomUser, State, City, Country

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Country)