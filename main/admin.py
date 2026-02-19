from django.contrib import admin
from .models import Master, Service, Client, Appointment, MasterWork, Vacation

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
    list_display = ('name', 'phone', 'email', 'registered_at', 'birth_date', 'age', 'needs_consent', 'parental_consent')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('registered_at',)

    def age(self, obj):
        return obj.age()
    
    age.short_description = "Возраст"
    
    def needs_consent(self, obj):
        return obj.needs_consent()
    
    needs_consent.boolean = True
    needs_consent.short_description = "Нужно согласие"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'date_time', 'status')
    list_filter = ('status', 'master', 'date_time')
    search_fields = ('client__name', 'client__phone')
    date_hierarchy = 'date_time'

@admin.register(MasterWork)
class MasterWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'master', 'category', 'created_at')
    list_filter = ('master', 'category', 'body_part')
    search_fields = ('title', 'description')

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_date', 'end_date', 'reason')
    list_filter = ('master', 'start_date')