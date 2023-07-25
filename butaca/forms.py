from django import forms
from django.shortcuts import get_object_or_404
from .models import *
from users.models import *

class CreateEventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['promoter'].queryset = CustomUser.objects.filter(status='Promotor')

    class Meta:
        model = Event
        fields = ('name', 'location', 'ticket_price', 'active', 'promoter', 'min_img', 
                    'bann_img', 'state', 'city', 'country',  'ticket_charge', 'url', 'min_price',
                    'max_price', 'ticket_level', 'bck_img' )

class DateEventForm(forms.ModelForm):
    class Meta:
        model = DateEvent
        fields = ('event', 'date', 'draw_event', 'draw_limit_date', 'event_time', 'promoter', 'ticket_quantity' )
    
    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)
        promoter_id = kwargs.pop('promoter', None)
        print(promoter_id)
        super().__init__(*args, **kwargs)

        if event_id:
            event = get_object_or_404(Event, event_id=event_id)
            self.fields['event'].queryset = Event.objects.filter(event_id=event_id)
            self.fields['event'].initial = event_id

        if promoter_id:
            promoter = get_object_or_404(CustomUser, user_id=promoter_id)
            self.fields['promoter'].initial = promoter_id
            

class DrawTicketForm(forms.ModelForm):
    class Meta:
        model = DrawTicket
        fields = []  # Add other fields if needed