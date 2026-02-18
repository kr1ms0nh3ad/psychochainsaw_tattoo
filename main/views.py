from django.shortcuts import render
from .models import Master, Service

def index(request):
    """главная страница с мастерами и услугами"""
    masters = Master.objects.filter(is_active=True)[:4]
    services = Service.objects.all()[:6]
    context = {
        'masters': masters,
        'services': services,
    }
    return render(request, 'main/index.html', context)

def masters_list(request):
    """список всех мастеров"""
    masters = Master.objects.filter(is_active=True)
    return render(request, 'main/masters.html', {'masters': masters})

def services_list(request):
    """список всех услуг"""
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})
