from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('masters/', views.masters_list, name='masters'),
    path('services/', views.services_list, name='services'),
    # path('portfolio/', views.porfolio_list, name='portfolio'),
]