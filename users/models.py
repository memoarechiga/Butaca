from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    
    user_id = models.CharField(max_length=20, primary_key=True, unique=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    address = models.CharField(max_length=150, null=True)
    telephone = models.CharField(max_length=150, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    auth_age = models.BooleanField(default=False, blank=True)
    send_mail = models.BooleanField(default=False, blank=True)
    terms_conds = models.BooleanField(default=False, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).split('-')[0]
        super().save(*args, **kwargs)