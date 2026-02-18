from django import forms
from .models import Appointment, Service, Master
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware

class AppointmentForm(forms.Form):
    client_name = forms.CharField(
        label='ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'леон кеннеди'})
    )

    client_phone = forms.CharField(
        label='телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+78005553535'})
    )

    client_email = forms.EmailField(
        label='электронная почта',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'psycho@chainsaw.ru'})
    )
    
    service = forms.ModelChoiceField(
        label='выберите услугу',
        queryset=Service.objects.all(),
        empty_label="--- выберите услугу ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    master = forms.ModelChoiceField(
        label='выберите мастера',
        queryset=Master.objects.filter(is_active=True),
        empty_label="--- выберите мастера ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date = forms.DateField(
        label='желаемая дата',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().date()})
    )
    
    time = forms.TimeField(
        label='желаемое время',
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    
    notes = forms.CharField(
        label='дополнительные пожелания',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'может вы что-то еще хотите.......'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        master = cleaned_data.get('master')
        
        if date and date < timezone.now().date():
            raise forms.ValidationError("ну нельзя выбрать прошедшую дату")
        
        # Проверка на занятость мастера (упрощенная)
        if date and time and master:
            
            dt = datetime.combine(date, time)
            # Делаем дату временной зоны
            dt_aware = make_aware(dt)
            
            existing = Appointment.objects.filter(
                master=master,
                date_time=dt_aware,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing:
                raise forms.ValidationError("это время уже занято, выберите другое время")
        
        return cleaned_data