from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Availability, Master, MasterWork, Service, Appointment, Client, Vacation
from django.views.decorators.http import require_GET
from .forms import AppointmentForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .utils import get_available_slots

def index(request):
    """главная страница с мастерами и услугами"""
    # masters = Master.objects.filter(is_active=True)[:4]
    masters = Master.objects.all()[:4]
    services = Service.objects.all()[:6]
    context = {
        'masters': masters,
        'services': services,
    }
    return render(request, 'main/index.html', context)

def masters_list(request):
    """список всех мастеров"""
    # masters = Master.objects.filter(is_active=True)
    masters = Master.objects.all()[:4]
    return render(request, 'main/masters.html', {'masters': masters})

def services_list(request):
    """список всех услуг"""
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})

# def book_appointment(request):
#     """форма записи на сеанс"""
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             phone = form.cleaned_data['client_phone']
#             client, created = Client.objects.get_or_create(
#                 phone=phone,
#                 defaults={
#                     'name': form.cleaned_data['client_name'],
#                     'email': form.cleaned_data['client_email'],
#                     'birth_date': form.cleaned_data['birth_date'],
#                 }
#             )

#             if not created:
#                 client.name = form.cleaned_data['client_name']
#                 client.email = form.cleaned_data['client_email']
#                 client.birth_date = form.cleaned_data['birth_date']
                
#                 # сохраняем согласие, если загрузили
#                 if form.cleaned_data.get('parental_consent'):
#                     client.parental_consent = form.cleaned_data['parental_consent']
                
#                 client.save()
            
#             dt = datetime.combine(
#                 form.cleaned_data['date'],
#                 form.cleaned_data['time']
#             )
#             dt_aware = make_aware(dt)
            
#             appointment = Appointment.objects.create(
#                 client=client,
#                 master=form.cleaned_data['master'],
#                 service=form.cleaned_data['service'],
#                 date_time=dt_aware,
#                 photo=form.cleaned_data['photo'],
#                 notes=form.cleaned_data['notes'],
#                 status='pending'
#             )
            
#             return redirect('booking_success', appointment_id=appointment.id)
#     else:
#         form = AppointmentForm()
    
#     print("FILES:", request.FILES)
#     print("parental_consent in FILES:", 'parental_consent' in request.FILES)

#     return render(request, 'main/book.html', {'form': form})

def book_appointment(request):
    """форма записи на сеанс"""
    if request.method == 'POST':
        print("="*50)
        print("ДАННЫЕ ФОРМЫ:")
        print("POST:", request.POST)
        print("FILES:", request.FILES)
        
        form = AppointmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("ФОРМА ВАЛИДНА")
            print("cleaned_data:", form.cleaned_data)
            
            phone = form.cleaned_data['client_phone']
            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': form.cleaned_data['client_name'],
                    'email': form.cleaned_data['client_email'],
                    'birth_date': form.cleaned_data['birth_date'],
                }
            )
            
            # ОТЛАДКА: что приходит в date и time
            selected_date = form.cleaned_data['date']
            selected_time = form.cleaned_data['time']
            print(f"Выбранная дата: {selected_date}")
            print(f"Выбранное время: {selected_time}")
            print(f"Тип времени: {type(selected_time)}")
            
            dt = datetime.combine(selected_date, selected_time)
            print(f"Скомбинировано (naive): {dt}")
            
            dt_aware = make_aware(dt)
            print(f"С часовым поясом: {dt_aware}")
            
            # Проверяем, что сохранится в БД
            print(f"Будет сохранено: {dt_aware}")
            print(f"Время в БД (час): {dt_aware.hour}")
            print(f"Время в БД (минуты): {dt_aware.minute}")
            
            appointment = Appointment.objects.create(
                client=client,
                master=form.cleaned_data['master'],
                service=form.cleaned_data['service'],
                date_time=dt_aware,
                photo=form.cleaned_data['photo'],
                notes=form.cleaned_data['notes'],
                status='pending'
            )
            
            print(f"СОЗДАНА ЗАПИСЬ ID: {appointment.id}")
            print(f"Время в созданной записи: {appointment.date_time}")
            print(f"Час: {appointment.date_time.hour}")
            print("="*50)
            
            return redirect('booking_success', appointment_id=appointment.id)
        else:
            print("ФОРМА НЕВАЛИДНА")
            print("Ошибки:", form.errors)
    else:
        form = AppointmentForm()
    
    return render(request, 'main/book.html', {'form': form})

def booking_success(request, appointment_id):
    """страница успешной записи"""
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'main/booking_success.html', {'appointment': appointment})

def master_detail(request, master_id):
    """страница конкретного мастера с его портфолио"""
    # master = get_object_or_404(Master, id=master_id, is_active=True)
    
    master = get_object_or_404(Master, id=master_id)
    
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
    # masters = Master.objects.filter(is_active=True)[:4] 
    masters = Master.objects.all()[:4]
    services = Service.objects.all()[:6]  
    
    # последние 8 работ из портфолио (всех мастеров)
    latest_works = MasterWork.objects.select_related('master').all().order_by('-created_at')[:8]
    
    context = {
        'masters': masters,
        'services': services,
        'latest_works': latest_works,
    }
    return render(request, 'main/index.html', context)

@require_GET
def api_available_slots(request):
    try:
        master_id = request.GET.get('master_id')
        date_str = request.GET.get('date')
        
        print(f"=== ЗАПРОС СЛОТОВ: master={master_id}, date={date_str} ===")
        
        if not master_id or not date_str:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        try:
            master = Master.objects.get(id=master_id)
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Master not found'}, status=404)
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        # Проверка отпуска
        in_vacation = Vacation.objects.filter(
            master=master,
            start_date__lte=date,
            end_date__gte=date
        ).exists()
        
        if in_vacation:
            return JsonResponse({'slots': []})
        
        # Получаем расписание
        day_of_week = date.weekday()
        try:
            availability = Availability.objects.get(
                master=master,
                day_of_week=day_of_week,
                is_active=True
            )
        except Availability.DoesNotExist:
            return JsonResponse({'slots': []})
        
        # Получаем ЗАНЯТЫЕ слоты
        busy_appointments = Appointment.objects.filter(
            master=master,
            date_time__date=date,
            status__in=['pending', 'confirmed']
        )
        
        # Получаем текущий часовой пояс
        local_tz = timezone.get_current_timezone()
        
        # СОЗДАЕМ МНОЖЕСТВО занятых слотов В МЕСТНОМ ВРЕМЕНИ
        busy_set = set()
        for apt in busy_appointments:
            # Конвертируем UTC в местное время
            local_time = apt.date_time.astimezone(local_tz)
            # Получаем час в местном времени
            local_hour = local_time.hour
            time_str = f"{local_hour:02d}:00"
            busy_set.add(time_str)
            print(f"✖ ЗАНЯТО (UTC: {apt.date_time.hour}:00 -> LOCAL: {local_hour}:00)")
        
        print(f"Всего занятых слотов (в местном времени): {sorted(busy_set)}")
        
        # Генерируем слоты в местном времени
        slots = []
        start_hour = availability.start_time.hour
        end_hour = availability.end_time.hour
        
        print(f"Рабочие часы (местное время): {start_hour}:00 - {end_hour}:00")
        
        for hour in range(start_hour, end_hour):
            time_str = f"{hour:02d}:00"
            
            if time_str in busy_set:
                print(f"❌ ЗАНЯТО (местное): {time_str}")
            else:
                slots.append(time_str)
                print(f"✅ СВОБОДНО: {time_str}")
        
        print(f"ИТОГО свободных слотов: {slots}")
        return JsonResponse({'slots': slots})
        
    except Exception as e:
        print(f"!!! ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)
    



print("\033[32m[ ONLINE http://127.0.0.1:8000/ ]\033[0m")