from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard_promoter/', DashboardPromoter.as_view(), name='dashboard_promoter'),
    path('dashboard_user/', DashboardUser.as_view(), name='dashboard_user'),

    path('event_list/', EventListView.as_view(), name='event_list'),
    path('event_list_promoter/', EventListPromoterView.as_view(), name='event_list_promoter'),
    path('event_new/', EventNew.as_view(), name='event_new'),
    path('event_new_promoter/', EventPromoterNew.as_view(), name='event_new_promoter'),
    path('event_update/<str:event_id>/', EventUpdateview.as_view(), name='event_update'),
    path('event_update_promoter/<str:event_id>/', EventUpdatePromoterview.as_view(), name='event_update_promoter'),
    path('event_detail/<str:event_id>/', EventDetailView.as_view(), name='event_detail'),
    path('event_detail_promoter/<str:event_id>/', EventDetailPromoterView.as_view(), name='event_detail_promoter'),
    path('event_detail_user/<str:event_id>/', EventDetailUserView.as_view(), name='event_detail_user'),
    path('event_date/new/<str:event_id>/', DateEventNew.as_view(), name='event_date_new'),
    path('event/<str:event_id>/delete/', event_delete, name='event_delete'),
    path('date_event/<str:date_event_id>/delete/', dateevent_delete, name='date_event_delete'),
    path('date_event_update/<str:date_event_id>/', DateEventUpdate.as_view(), name='date_event_update'),
    path('date_event_update_pr/<str:date_event_id>/', DateEventPromoterUpdate.as_view(), name='date_event_update_pro'),
    path('ticket_promoter_list/', TicketEventPromoterList.as_view(), name="ticket_promoter_list"),

    path('create_draw_ticket/<str:date_event_id>/', create_draw_ticket, name='create_draw_ticket'),

    path('promoter_list/', PromotorListView.as_view(), name='promoter_list'),
    path('promoter/<str:user_id>/delete/', promoter_delete, name='promoter_delete'),

    path('suscriber_list/', SuscriberListView.as_view(), name='suscriber_list'),
    path('suscriber/<str:user_id>/delete/', suscriber_delete, name='suscriber_delete'),

    path('settings_admin/', SettingsAdmin.as_view(), name="settings_admin"), 
    path('city_new/', city_new, name='city_new'),
    path('start_task/', start_task, name="start_task"),


    ]