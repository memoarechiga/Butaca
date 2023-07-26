import datetime
import random
from .models import *
from celery import shared_task

@shared_task()
def choose_random_winners():
    # Get the list of DateEvent objects that have draw_event set to the current date
    draw_event_date = datetime.datetime.now().date()
    date_events = DateEvent.objects.filter(draw_event=draw_event_date)
    print(date_events)

    # Iterate through the DateEvent objects and choose random winners for each event
    for date_event in date_events:
        # Retrieve all DrawTicket objects associated with this DateEvent
        draw_tickets = DrawTicket.objects.filter(date_event=date_event)
        for draw_ticket in draw_tickets:
            print(draw_ticket)

        # If there are more tickets than available ticket_quantity, randomly choose winners
        if len(draw_tickets) > date_event.ticket_quantity:
            winners = random.sample(list(draw_tickets), date_event.ticket_quantity)
        else:
            winners = draw_tickets

        print(winners)

        # Save the winners to the Winner model
        for winner in winners:
            Winner.objects.create(user=winner.user, date_event=date_event)