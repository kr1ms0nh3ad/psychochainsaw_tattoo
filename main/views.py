from django.shortcuts import get_object_or_404, render, redirect
from .models import Master, MasterWork, Service, Appointment, Client
from .forms import AppointmentForm
from datetime import datetime
from django.utils.timezone import make_aware

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

def book_appointment(request):
    """форма записи на сеанс"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['client_phone']
            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': form.cleaned_data['client_name'],
                    'email': form.cleaned_data['client_email']
                }
            )
            
            dt = datetime.combine(
                form.cleaned_data['date'],
                form.cleaned_data['time']
            )
            dt_aware = make_aware(dt)
            
            appointment = Appointment.objects.create(
                client=client,
                master=form.cleaned_data['master'],
                service=form.cleaned_data['service'],
                date_time=dt_aware,
                notes=form.cleaned_data['notes'],
                status='pending'
            )
            
            return redirect('booking_success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    return render(request, 'main/book.html', {'form': form})

def booking_success(request, appointment_id):
    """страница успешной записи"""
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'main/booking_success.html', {'appointment': appointment})

def master_detail(request, master_id):
    """страница конкретного мастера с его портфолио"""
    master = get_object_or_404(Master, id=master_id, is_active=True)
    
    portfolio = MasterWork.objects.filter(master=master).order_by('-created_at')
    
    services = Service.objects.filter(masters=master)
    
    works_count = portfolio.count()
    completed_appointments = Appointment.objects.filter(master=master, status='completed').count()
    
    context = {
        'master': master,
        'portfolio': portfolio,
        'services': services,
        'works_count': works_count,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'main/master_detail.html', context)

def index(request):
    """главная страница: показывает мастеров, услуги и последние работы"""
    masters = Master.objects.filter(is_active=True)[:4]  # Первые 4 мастера
    services = Service.objects.all()[:6]  # Первые 6 услуг
    
    # последние 8 работ из портфолио (всех мастеров)
    latest_works = MasterWork.objects.select_related('master').all().order_by('-created_at')[:8]
    
    context = {
        'masters': masters,
        'services': services,
        'latest_works': latest_works,
    }
    return render(request, 'main/index.html', context)

print("\033[32m[ ONLINE http://127.0.0.1:8000/ ]\033[0m")