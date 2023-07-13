from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class CustomUser(AbstractUser):
    TAMPICO = 'tampico'
    ALTAMIRA = 'altamira'
    CDMADERO = 'cd. mader'
    TAMAULIPAS = 'tamaulipas'
    VERACRUZ = 'veracruz'
    OTRO = 'otro'

    CIUDADES = [
        (TAMPICO, 'Tampico'),
        (ALTAMIRA, 'Altamira'),
        (CDMADERO, 'Cd. Madero'),
        (OTRO, 'Otro'),
    ]

    ESTADOS = [
        (TAMAULIPAS, 'Tamaulipas'),
        (VERACRUZ, 'Veracruz'),
        (OTRO, 'Otro'),
    ]

    user_id = models.CharField(max_length=20, primary_key=True, unique=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    address = models.CharField(max_length=150, null=True)
    telephone = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=50,choices=CIUDADES, null=True)
    state = models.CharField(max_length=50, choices=ESTADOS, null=True)
    auth_age = models.BooleanField(default=False)
    send_mail = models.BooleanField(default=False)
    terms_conds = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).split('-')[0]
        super().save(*args, **kwargs)