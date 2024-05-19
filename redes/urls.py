from django.urls import path
from . import views

app_name = 'redes'

urlpatterns = [
    path('interfaces/', views.interfaces, name='interfaces'),
    path('dhcp/', views.dhcp, name='dhcp'),
    path('reserva_ip/', views.reserva_ip, name='reserva_ip'),
    path('enrutamiento/', views.enrutamiento, name='enrutamiento'),
    path('pingtester/', views.pingtester, name='pingtester'),
]
