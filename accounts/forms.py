from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from main.models import MasterWork

class MasterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, label='имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # поля мастера
    specialty = forms.CharField(max_length=200, label='специализация', widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience = forms.IntegerField(label='опыт (лет)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, label='телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = 'логин для входа в систему'
        self.fields['password1'].help_text = 'пароль должен содержать минимум 8 символов'
        self.fields['password2'].help_text = 'введите тот же пароль для подтверждения'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = MasterWork
        fields = ['title', 'description', 'image', 'category', 'body_part']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '--- Выберите категорию ---'),
                ('realism', 'Реализм'),
                ('traditional', 'Традиция'),
                ('oldschool', 'Олдскул'),
                ('newschool', 'Ньюскул'),
                ('graphic', 'Графика'),
                ('dotwork', 'Дотворк'),
                ('ornamental', 'Орнаментал'),
                ('other', 'Другое'),
            ]),
            'body_part': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', '--- Выберите часть тела ---'),
                ('arm', 'Рука'),
                ('leg', 'Нога'),
                ('back', 'Спина'),
                ('chest', 'Грудь'),
                ('shoulder', 'Плечо'),
                ('hand', 'Кисть'),
                ('neck', 'Шея'),
                ('other', 'Другое'),
            ]),
        }