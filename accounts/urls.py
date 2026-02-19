from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.master_dashboard, name='master_dashboard'),
    path('appointment/<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),
    path('portfolio/', views.master_portfolio, name='master_portfolio'),
    path('portfolio/add/', views.add_portfolio_work, name='add_portfolio_work'),
    path('portfolio/delete/<int:work_id>/', views.delete_portfolio_work, name='delete_portfolio_work'),
]