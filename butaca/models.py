from django.db import models

# Create your models here.

class Event(models.Model):
    event_id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    date1 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    date2 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    date3 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    date4 = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location = models.CharField(max_length=50)
    ticket_price = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name