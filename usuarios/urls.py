from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_usuarios_secuenciales/', views.crear_usuarios_secuenciales, name='crear_usuarios_secuenciales'),
    path('modificar_usuario/', views.modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('analizar_contrasena/', views.analizar_contrasena, name='analizar_contrasena'),
    path('validar_contrasena/', views.validar_contrasena, name='validar_contrasena' ),
    path('configurar_permisos/', views.configurar_permisos, name='configurar_permisos'),
    path('cambiar_usuario_grupo/', views.cambiar_usuario_grupo, name='cambiar_usuario_grupo'),
]
