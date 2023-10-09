from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json


from django.views.generic import TemplateView, ListView, FormView, DeleteView, UpdateView, DetailView, CreateView
from .tasks import *
from users.models import *
from users.forms import CityNewForm, StateNewForm, CountryNewForm
from .models import *
from .forms import CreateEventForm, DateEventForm, DrawTicketForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .custom_decorators import promoter_required

from django.utils.timezone import make_aware
import datetime

# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'



class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'butaca/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_count"] = CustomUser.objects.filter(status=None).count()
        context["pro_count"] = CustomUser.objects.filter(status="Promotor").count()
        context["event_count"] = Event.objects.filter(active=True).count()

        # Filter the last 5 active events based on upload date (sorted from newest to oldest)
        last_5_events = Event.objects.filter(active=True).order_by('-date')[:4]
        context["event_lists"] = last_5_events

        current_date = make_aware(datetime.datetime.now())  # Get the current date in the server's timezone
        current_year = current_date.year

        # Create a list to store data for each month in the current year
        monthly_data = []

        for month in range(1, 13):  # Loop through months from January to December
            # Filter CustomUser count for each month in the current year
            users_count_this_month = CustomUser.objects.filter(status=None, date_joined__year=current_year, date_joined__month=month).count()
            
            # Append the data for the current month to the list
            monthly_data.append({
                'month': month,
                'users_count_month': users_count_this_month,
            })

        # Add the monthly data to the context
        context['monthly_data'] = monthly_data
        return context

class DashboardPromoter(LoginRequiredMixin, TemplateView):
    template_name = 'butaca/dashboard_promoter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(promoter=self.request.user).count()
        return context
    
class DashboardUser(LoginRequiredMixin, TemplateView):
    template_name = 'butaca/dashboard_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(active=True)
        # Get the list of city names that have associated active events
        active_cities = Event.objects.filter(active=True).values_list('city__name', flat=True).distinct()
        print(active_cities)
        # Query the City model to get only those cities with active events
        context["cities"] = City.objects.filter(name__in=active_cities)

        return context


    
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "butaca/event_list.html"
    context_object_name = 'events'

class EventListPromoterView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "butaca/event_list_promoter.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(promoter=self.request.user)
        return context
    

    @method_decorator(promoter_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class EventNew(LoginRequiredMixin, FormView):
    form_class = CreateEventForm
    template_name = "butaca/event_new.html"
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.event_id = str(uuid.uuid4())[:8]
        obj.date = datetime.datetime.now()
        obj.save()
        messages.success(self.request, 'Evento creado satisfactoriamente.')
        return super().form_valid(form)

class EventPromoterNew(LoginRequiredMixin, FormView):
    form_class = CreateEventForm
    template_name = "butaca/event_new_promoter.html"
    success_url = reverse_lazy('event_list_promoter')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.event_id = str(uuid.uuid4())[:8]
        obj.date = datetime.datetime.now()
        obj.promoter = self.request.user
        obj.save()
        messages.success(self.request, 'Evento creado satisfactoriamente.')
        return super().form_valid(form)

class EventUpdateview(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'location', 'ticket_price', 'active', 'promoter', 'min_img', 
                    'bann_img', 'state', 'city', 'country',  'ticket_charge', 'url', 'min_price',
                    'max_price', 'ticket_level', 'bck_img']
    template_name = "butaca/event_update.html"
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(event_id=event_id)
        return obj

class EventUpdatePromoterview(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'location', 'ticket_price', 'active', 'min_img', 
                    'bann_img', 'state', 'city', 'country',  'ticket_charge', 'url', 'min_price',
                    'max_price', 'ticket_level', 'bck_img']
    template_name = "butaca/event_update_promoter.html"
    success_url = reverse_lazy('event_list')

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(event_id=event_id)
        return obj

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "butaca/event_detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(event_id=event_id)
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and has status set to "none"
        if not request.user.is_authenticated or request.user.status != "admin":
            raise Http404("You are not allowed to access this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['event_id']
        context["date"] = DateEvent.objects.filter(event=event_id)
        return context


class EventDetailPromoterView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "butaca/event_detail_promoter.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(event_id=event_id)
        return obj

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and has status set to "none"
        if not request.user.is_authenticated or request.user.status != "Promotor":
            raise Http404("You are not allowed to access this page.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['event_id']
        context["date"] = DateEvent.objects.filter(event=event_id)
        return context

class EventDetailUserView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "butaca/event_detail_user.html"
    context_object_name = "events"

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(event_id=event_id)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object.event_id
        # Get related DateEvent objects for the current event
        date_events = DateEvent.objects.filter(event=event)
        # Filter events to get the one closest to the actual date
        current_date = datetime.datetime.now().date()
        closest_event = Event.objects.filter(active=True, date__lt=current_date).order_by('-date').first()
        context["closest_event"] = closest_event
        print("current day:", current_date)
        print("this is:", closest_event.date)

        context['date_events'] = date_events
        return context



class DateEventNew(LoginRequiredMixin, FormView):
    form_class = DateEventForm
    template_name = "butaca/event_date_new.html"

    def get_success_url(self):
        event_id = self.kwargs.get('event_id')
        return reverse_lazy('event_detail', kwargs={'event_id': event_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event_id = self.kwargs.get('event_id')
        kwargs['event_id'] = event_id
        promoter_id = Event.objects.get(event_id=event_id).promoter_id
        kwargs['promoter'] = promoter_id
        print(promoter_id)
        return kwargs

    def form_valid(self, form):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, event_id=event_id)
        obj = form.save(commit=False)
        obj.date_event_id = str(uuid.uuid4())[:8]
        obj.event_name = event
        obj.save()
        messages.success(self.request, 'Fecha de Evento creado satisfactoriamente.')
        return super().form_valid(form)

        try:
            obj.save()
            messages.success(self.request, 'Fecha de Evento creado satisfactoriamente.')
        except Exception as e:
            messages.error(self.request, f'Error occurred: {str(e)}')
        return super().form_valid(form)

class DateEventUpdate(LoginRequiredMixin, UpdateView):
    model = DateEvent
    fields = ['date', 'draw_event', 'draw_limit_date', 'event_time', 'ticket_quantity' ]
    template_name = "butaca/event_date_update.html"
    success_url = reverse_lazy('event_detail')

    def get_success_url(self):
        date_event_instance = self.get_object()  # Get the DateEvent instance being updated
        event_id = date_event_instance.event_name.event_id  # Get the event_id from the related Event instance
        return reverse_lazy('event_detail', kwargs={'event_id': event_id})

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        date_event_id = self.kwargs['date_event_id']
        obj = DateEvent.objects.get(date_event_id=date_event_id)
        return obj

class DateEventPromoterUpdate(LoginRequiredMixin, UpdateView):
    model = DateEvent
    fields = ['date', 'draw_event', 'draw_limit_date', 'event_time', 'ticket_quantity' ]
    template_name = "butaca/event_date_update_promoter.html"
    success_url = reverse_lazy('event_detail_promoter')

    def get_success_url(self):
        date_event_instance = self.get_object()  # Get the DateEvent instance being updated
        event_id = date_event_instance.event_name.event_id  # Get the event_id from the related Event instance
        return reverse_lazy('event_detail_promoter', kwargs={'event_id': event_id})

    def get_object(self, queryset=None):
        # Fetch the object based on your custom ID field
        date_event_id = self.kwargs['date_event_id']
        obj = DateEvent.objects.get(date_event_id=date_event_id)
        return obj


class DateEventList(LoginRequiredMixin, ListView):
    template_name = "date_event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = DateEvent.objects.filter(status=True)
        return context

class DateEventPromoterList(LoginRequiredMixin, ListView):
    template_name = "date_event_list_promoter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = DateEvent.objects.filter(status=True).filter()
        return context

class TicketEventPromoterList(LoginRequiredMixin, ListView):
    model = DateEvent
    template_name = "butaca/ticket_list_promoter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = DateEvent.objects.all()
        return context
    
    


def event_delete(request, event_id):
    if request.method == 'DELETE':
        try:
            event = Event.objects.get(event_id=event_id)
            event.delete()
            return JsonResponse({'message': 'Promoter deleted successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Promoter not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def dateevent_delete(request, date_event_id):
    if request.method == 'DELETE':
        try:
            date_event = DateEvent.objects.get(date_event_id=date_event_id)
            date_event.delete()
            return JsonResponse({'message': 'Promoter deleted successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Promoter not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)





class PromotorListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "butaca/promoter_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["promoters"] = CustomUser.objects.filter(status='Promotor')
        return context

def promoter_delete(request, user_id):
    if request.method == 'DELETE':
        try:
            promoter = CustomUser.objects.get(user_id=user_id)
            promoter.delete()
            return JsonResponse({'message': 'Promoter deleted successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Promoter not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)






class SuscriberListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "butaca/suscriber_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["suscribers"] = CustomUser.objects.filter(status=None)
        return context

def suscriber_delete(request, user_id):
    if request.method == 'DELETE':
        try:
            suscriber = CustomUser.objects.get(user_id=user_id)
            suscriber.delete()
            return JsonResponse({'message': 'Promoter deleted successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Promoter not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



def create_draw_ticket(request, date_event_id):
    date_event = get_object_or_404(DateEvent, date_event_id=date_event_id)
    try:
        if request.method == 'POST':
            form = DrawTicketForm(request.POST)
            if form.is_valid():
                user = request.user

                date_event_id = date_event.date_event_id

                # Check if a ticket with the same date_event_id and user already exists
                existing_ticket = DrawTicket.objects.filter(date_event__date_event_id=date_event_id, user=user).first()

                if existing_ticket:
                    # If a ticket already exists, handle it accordingly (e.g., show an error message)
                    messages.error(request, "Ya tienes este boleto registrado.")
                    return redirect('dashboard_user')

                draw_ticket = form.save(commit=False)
                draw_ticket.draw_ticket_id = str(uuid.uuid4())[:8]
                draw_ticket.date_event = date_event
                draw_ticket.date = datetime.datetime.now()
                draw_ticket.user = user
                draw_ticket.save()

                # Optionally, you can set other fields here based on the ticket or form data
                messages.success(request, "Boleto registrado satisfactoriamente!, Te llegara un correo con toda la información.")
                # Redirect the user to a success page or any other desired view
                return redirect('dashboard_user')  # Replace 'dashboard_user' with the URL name of the dashboard_user view

        else:
            return HttpResponse("Invalid request")
    
        response_data = {'status': 'success', 'message': 'Draw ticket created successfully.'}

        return JsonResponse(response_data)
    except Exception as e:
        # Handle errors and return an error response
        error_data = {'status': 'error', 'message': str(e)}
        return JsonResponse(error_data, status=400)  # Use appropriate status code for errors



class SettingsAdmin(TemplateView):
    template_name = "butaca/settings_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        context["states"] = State.objects.all()
        context["countries"] = Country.objects.all()
        return context

def city_new(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city_name = data.get('name', '')
            print(city_name)
            if city_name:
                city = City(name=city_name)
                city.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'City name is missing'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
            

    


def start_task(request):
    # You can call the task function here or in any other view
    choose_random_winners()
    # Add any other logic you need for the view

    return HttpResponse("Task started successfully!")