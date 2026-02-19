from django import forms
from django.contrib.auth.forms import AuthenticationForm
from main.models import MasterWork

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="пароль")

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = MasterWork
        fields = ['title', 'description', 'image', 'category', 'body_part']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '--- выберите категорию ---'),
                ('ornamental', 'киберсигилизм'),
                ('realism', 'реализм'),
                ('oldschool', 'олдскул'),
                ('abstract', 'абстракция'),
                ('dotwork', 'дотворк'),
                ('other', 'другое'),
            ]),
            'body_part': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '--- выберите часть тела ---'),
                ('arm', 'рука'),
                ('leg', 'нога'),
                ('back', 'спина'),
                ('chest', 'грудь'),
                ('shoulder', 'плечо'),
                ('hand', 'кисть'),
                ('neck', 'шея'),
                ('other', 'другое'),
            ]),
        }