from django.contrib import admin
from .models import Availability, Master, Service, Client, Appointment, MasterWork, Vacation
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'experience', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('name',)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['create_master_url'] = reverse('admin_create_master')
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    filter_horizontal = ('masters',) 

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('master', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('master', 'day_of_week', 'is_active')

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_date', 'end_date', 'reason')
    list_filter = ('master', 'start_date')

