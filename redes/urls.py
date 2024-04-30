from django.urls import path
from . import views

app_name = 'redes'

urlpatterns = [
    path('interfaces/', views.interfaces, name='interfaces'),
    path('dhcp/', views.dhcp, name='dhcp'),
    path('dns/', views.dns, name='dns'),
    path('enrutamiento/', views.enrutamiento, name='enrutamiento'),
]
