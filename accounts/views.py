from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm, PortfolioForm
from main.models import Master, Appointment, MasterWork

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # проверяем, есть ли у пользователя профиль мастера
                try:
                    master = Master.objects.get(user=user)
                    return redirect('master_dashboard')
                except Master.DoesNotExist:
                    messages.warning(request, 'У вас нет прав мастера')
                    return redirect('index')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def master_dashboard(request):
    # получаем профиль мастера
    try:
        master = Master.objects.get(user=request.user)
    except Master.DoesNotExist:
        return redirect('index')
    
    # получаем записи к этому мастеру
    today = timezone.now().date()
    
    # предстоящие записи
    upcoming_appointments = Appointment.objects.filter(
        master=master,
        date_time__date__gte=today,
        status__in=['pending', 'confirmed']
    ).order_by('date_time')
    
    # прошедшие записи
    past_appointments = Appointment.objects.filter(
        master=master,
        date_time__date__lt=today
    ).order_by('-date_time')[:10]
    
    # статистика
    total_appointments = Appointment.objects.filter(master=master).count()
    completed_appointments = Appointment.objects.filter(master=master, status='completed').count()
    pending_appointments = Appointment.objects.filter(master=master, status='pending').count()
    
    context = {
        'master': master,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # проверяем, что это мастер для этой записи
    if appointment.master.user != request.user:
        messages.error(request, 'У вас нет прав для этого действия')
        return redirect('master_dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['confirmed', 'completed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Статус записи изменен на {appointment.get_status_display()}')
    
    return redirect('master_dashboard')

@login_required
def master_portfolio(request):
    """Просмотр и управление портфолио"""
    try:
        master = Master.objects.get(user=request.user)
    except Master.DoesNotExist:
        messages.error(request, 'Профиль мастера не найден')
        return redirect('index')
    
    works = MasterWork.objects.filter(master=master)
    return render(request, 'accounts/portfolio.html', {'works': works, 'master': master})

@login_required
def add_portfolio_work(request):
    """Добавление новой работы"""
    try:
        master = Master.objects.get(user=request.user)
    except Master.DoesNotExist:
        messages.error(request, 'Профиль мастера не найден')
        return redirect('index')
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.master = master
            work.save()
            messages.success(request, 'Работа добавлена в портфолио!')
            return redirect('master_portfolio')
    else:
        form = PortfolioForm()
    
    return render(request, 'accounts/add_work.html', {'form': form, 'master': master})

@login_required
def delete_portfolio_work(request, work_id):
    """Удаление работы"""
    work = get_object_or_404(MasterWork, id=work_id)
    
    # Проверяем, что это работа текущего мастера
    if work.master.user != request.user:
        messages.error(request, 'У вас нет прав для этого действия')
        return redirect('master_portfolio')
    
    if request.method == 'POST':
        work.image.delete()  # Удаляем файл
        work.delete()
        messages.success(request, 'Работа удалена из портфолио')
    
    return redirect('master_portfolio')