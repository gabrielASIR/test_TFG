from django.urls import path
from . import views

app_name = 'seguridad'

urlpatterns = [
    path('firewall/', views.firewall, name='firewall'),
    path('proxy/', views.proxy, name='proxy'),
    path('certificados/', views.certificados, name='certificados'),
]

