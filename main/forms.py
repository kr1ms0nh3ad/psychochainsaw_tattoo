from django import forms
from .models import Appointment, Client, Service, Master
from django.utils import timezone

class AppointmentForm(forms.Form):
    client_name = forms.CharField(
        label='ваше имя',
        max_length=100,
        widget=forms.TextInput()
    )