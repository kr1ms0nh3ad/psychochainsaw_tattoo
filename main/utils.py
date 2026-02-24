from datetime import datetime, timedelta, timezone
from .models import Appointment, Availability, Vacation

def get_available_slots(master, date):
    """
    Возвращает список свободных слотов для мастера на указанную дату
    """
    # Проверяем, не в отпуске ли мастер
    if Vacation.objects.filter(
        master=master,
        start_date__lte=date,
        end_date__gte=date
    ).exists():
        return []  # В отпуске - нет слотов
    
    # Получаем день недели (0 - понедельник, 6 - воскресенье)
    day_of_week = date.weekday()
    
    # Получаем расписание мастера на этот день
    try:
        availability = Availability.objects.get(
            master=master,
            day_of_week=day_of_week,
            is_active=True
        )
    except Availability.DoesNotExist:
        return []  # Нет расписания - нет слотов
    
    # Получаем все ЗАНЯТЫЕ слоты на эту дату
    busy_appointments = Appointment.objects.filter(
        master=master,
        date_time__date=date,
        status__in=['pending', 'confirmed']  # Только активные записи
    ).values_list('date_time', flat=True)
    
    # Преобразуем в список времени
    busy_times = [apt.time() for apt in busy_appointments]
    
    # Генерируем все возможные слоты (например, с шагом 1 час)
    all_slots = []
    current_time = datetime.combine(date, availability.start_time)
    end_time = datetime.combine(date, availability.end_time)
    
    while current_time < end_time:
        # Проверяем, не занят ли этот слот
        if current_time.time() not in busy_times:
            # Проверяем, что слот не в прошлом
            if current_time > timezone.now():
                all_slots.append(current_time.strftime('%H:%M'))
        
        current_time += timedelta(hours=1)  # Шаг 1 час
    
    return all_slots