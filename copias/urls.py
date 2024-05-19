from django.urls import path
from . import views

app_name = 'copias'

urlpatterns = [
    path('configuracion_backups/', views.configuracion_backups, name='configuracion_backups'),
    path('programar_copia/', views.programar_copia, name='programar_copia'),
    path('configuracion_nas/', views.configuracion_nas, name='configuracion_nas'),
    path('subida_archivos_nas/', views.subida_archivos_nas, name='subida_archivos_nas'),
]

