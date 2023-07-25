from django.db import models
from django.conf import settings
from users.models import *

# Create your models here.

class Event(models.Model):
    event_id = models.CharField(max_length=20, primary_key=True, unique=True)
    min_img = models.ImageField(default='', upload_to='event_galery', blank=True)
    bann_img = models.ImageField(default='', upload_to='event_galery', blank=True)
    bck_img = models.ImageField(default='', upload_to='event_galery', blank=True, null=True)
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    ticket_price = models.CharField(max_length=50, null=True)
    ticket_charge = models.CharField(max_length=50, null=True)
    ticket_level = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=50, null=True)
    min_price = models.CharField(max_length=50, null=True)
    max_price = models.CharField(max_length=50, null=True)
    active = models.BooleanField(default=False)
    promoter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promoter', null=True, blank=True)

    def __str__(self):
        return self.name

class DateEvent(models.Model):
    date_event_id = models.CharField(max_length=20, primary_key=True, unique=True, default='1')
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    event = models.CharField(max_length=50, null=True)
    promoter = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    ticket_quantity = models.IntegerField(null=True)
    draw_event = models.DateField(auto_now=False, auto_now_add=False, null=True)
    draw_limit_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    event_time = models.TimeField(auto_now=False, auto_now_add=False, null=True) 
    status = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.event_name.name

    def get_related_event(self):
        try:
            return Event.objects.get(event_id=self.event)
        except Event.DoesNotExist:
            return None

class DrawTicket(models.Model):
    draw_ticket_id = models.CharField(max_length=20, primary_key=True, unique=True, default='1')
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_event = models.ForeignKey(DateEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f' Usuario: {self.user} - Event: {self.date_event.event_name} - Fecha: {self.date_event.date} - Horario: {self.date_event.event_time}' 

class Winner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_event = models.ForeignKey(DateEvent, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Winner: {self.user.username} - Event: {self.date_event.event_name} - Date: {self.date_event.date} - Time: {self.date_event.event_time}'