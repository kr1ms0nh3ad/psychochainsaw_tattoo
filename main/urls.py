from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('masters/', views.masters_list, name='masters'),
    path('services/', views.services_list, name='services'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('booking/success/<int:appointment_id>/', views.booking_success, name='booking_success'),
    path('master/<int:master_id>/', views.master_detail, name='master_detail'),
    path('api/available-slots/', views.api_available_slots, name='api_available_slots'),
]