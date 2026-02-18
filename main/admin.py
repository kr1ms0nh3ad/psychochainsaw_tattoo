from django.contrib import admin
from .models import Master, Service, Client, Appointment

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'experience', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    filter_horizontal = ('masters',) 

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'registered_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('registered_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'date_time', 'status')
    list_filter = ('status', 'master', 'date_time')
    search_fields = ('client__name', 'client__phone')
    date_hierarchy = 'date_time'