from django import forms
from .models import Appointment, Service, Master, Vacation
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware

class AppointmentForm(forms.Form):
    client_name = forms.CharField(
        label='ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'})
    )

    birth_date = forms.DateField(
        label='день рождения',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    parental_consent = forms.FileField(
        label='согласие родителей',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
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
        label='Желаемая дата',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    
    time = forms.TimeField(
        label='желаемое время',
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    photo = forms.FileField(
        label='желаемый эскиз',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        label='дополнительные пожелания',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'опишите идею, размер, место на теле'})
    )
    
    def clean(self):
        cleaned_data = super().clean()

        birth_date = cleaned_data.get('birth_date')
        parental_consent = self.files.get('parental_consent')
        
        if birth_date:
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 18 and not parental_consent:
                raise forms.ValidationError(
                    "вам меньше 18 лет. для записи необходимо приложить согласие родителей!"
                )

        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        master = cleaned_data.get('master')
        
        if date and master:
            in_vacation = Vacation.objects.filter(
                master=master,
                start_date__lte=date,
                end_date__gte=date
            ).exists()

        if in_vacation:
            raise forms.ValidationError("выбранный вами мастер сейчас в отпуске, перенесите сеанс или выберите другого мастера")

        if date and date < timezone.now().date():
            raise forms.ValidationError("ну нельзя выбрать прошедшую дату")

        if date and time and master:
            
            dt = datetime.combine(date, time)
            dt_aware = make_aware(dt)
            
            existing = Appointment.objects.filter(
                master=master,
                date_time=dt_aware,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing:
                raise forms.ValidationError("это время уже занято, выберите другое время")
        
        return cleaned_data