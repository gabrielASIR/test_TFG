from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator
from django.forms import ValidationError
import os

def crear_usuario(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        grupo_principal = request.POST.get('grupo_principal')
        otros_grupos = request.POST.get('otros_grupos')
        nombre_completo = request.POST.get('nombre_completo')
        directorios = request.POST.get('directorios')
        skel = request.POST.get('skel')
        directorio_principal = request.POST.get('home')
        shell = request.POST.get('shell')
        expire = request.POST.get('expire')
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        inactivo = request.POST.get('inactivo')
        crear_directorio_principal = request.POST.get('crear_directorio_principal')
        copiar_skel = request.POST.get('copiar_skel')

        # Validación de campos obligatorios
        if not nombre_usuario or not contrasena or not grupo_principal or not shell:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'Los campos nombre de usuario, contraseña, grupo principal y shell son obligatorios.'})

        # Validación de formato de campos
        # Puedes agregar más validaciones según sea necesario

        # Validación de contraseña
        if len(contrasena) < 6:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'La contraseña debe tener al menos 6 caracteres.'})

        # Validación de shell
        shells_validos = ['/bin/bash', '/bin/sh', '/bin/zsh']
        if shell not in shells_validos:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El shell especificado no es válido.'})

        # Ruta al script de Bash para crear usuarios
        ruta_script = 'usuarios/bash/crear_usuario.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_usuario}', nombre_usuario)
        contenido_script = contenido_script.replace('{contrasena}', contrasena)
        contenido_script = contenido_script.replace('{grupo_principal}', grupo_principal)
        contenido_script = contenido_script.replace('{shell}', shell)
        if otros_grupos:
            contenido_script = contenido_script.replace('{otros_grupos}', otros_grupos)
        if nombre_completo:
            contenido_script = contenido_script.replace('{nombre_completo}', nombre_completo)
        if directorios:
            contenido_script = contenido_script.replace('{directorios}', directorios)
        if skel:
            contenido_script = contenido_script.replace('{skel}', skel)
        if directorio_principal:
            contenido_script = contenido_script.replace('{directorio_principal}', directorio_principal)
        if expire:
            contenido_script = contenido_script.replace('{expire}', expire)
        if uid:
            contenido_script = contenido_script.replace('{uid}', uid)
        if gid:
            contenido_script = contenido_script.replace('{gid}', gid)
        if inactivo:
            contenido_script = contenido_script.replace('{inactivo}', inactivo)
        if crear_directorio_principal == 'yes':
            contenido_script = contenido_script.replace('{crear_directorio_principal}', '-m')
        else:
            contenido_script = contenido_script.replace('{crear_directorio_principal}', '')
        if copiar_skel == 'yes':
            contenido_script = contenido_script.replace('{copiar_skel}', '-k {skel}')
        else:
            contenido_script = contenido_script.replace('{copiar_skel}', '')

        # Devolver el script de Bash como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="crear_usuario.sh"'
        return respuesta
    else:
        return render(request, 'usuarios/crear_usuario.html')

def crear_usuarios_secuenciales(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        prefijo = request.POST.get('prefijo')
        inicio = int(request.POST.get('inicio'))
        fin = int(request.POST.get('fin'))

        # Ruta al script de Bash para crear usuarios
        script_path = 'usuarios/bash/crear_usuarios_secuenciales.sh'

        # Inicializar script_content
        script_content = ""

        if prefijo is not None:
            script_content += f"#!/bin/bash\n"
            for i in range(inicio, fin + 1):
                usuario = f"{prefijo}{i}"
                script_content += f"useradd {usuario}\n"
                script_content += f"echo 'Usuario {usuario} creado'\n"

            # Devolver el script de Bash como una descarga de archivo
            response = HttpResponse(script_content, content_type='application/x-shellscript')
            response['Content-Disposition'] = 'attachment; filename="crear_usuarios_secuenciales.sh"'
            return response
        else:
            return HttpResponse("No se proporcionó un prefijo para la creación de usuarios secuenciales.", status=400)
    else:
        return render(request, 'usuarios/crear_usuario.html')

def modificar_usuario(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        grupo_principal = request.POST.get('grupo_principal')
        otros_grupos = request.POST.get('otros_grupos')
        nombre_completo = request.POST.get('nombre_completo')
        directorios = request.POST.get('directorios')
        skel = request.POST.get('skel')
        directorio_home = request.POST.get('home')
        shell = request.POST.get('shell')
        expire = request.POST.get('expire')
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        inactive = request.POST.get('inactive')
        crear_home = request.POST.get('create_home')
        copiar_skel = request.POST.get('copy_skel')

        # Ruta al script de Bash para modificar usuarios
        script_path = 'usuarios/bash/modificar_usuario.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        script_content = script_content.replace('{nombre_usuario}', nombre_usuario)
        script_content = script_content.replace('{contrasena}', contrasena)
        script_content = script_content.replace('{grupo_principal}', grupo_principal)
        script_content = script_content.replace('{otros_grupos}', otros_grupos)
        script_content = script_content.replace('{nombre_completo}', nombre_completo)
        script_content = script_content.replace('{directorios}', directorios)
        script_content = script_content.replace('{skel}', skel)
        script_content = script_content.replace('{directorio_home}', directorio_home)
        script_content = script_content.replace('{shell}', shell)
        script_content = script_content.replace('{expire}', expire)
        script_content = script_content.replace('{uid}', uid)
        script_content = script_content.replace('{gid}', gid)
        script_content = script_content.replace('{inactive}', inactive)

        if crear_home == 'yes':
            script_content = script_content.replace('{crear_home}', '-m')
        else:
            script_content = script_content.replace('{crear_home}', '')

        if copiar_skel == 'yes':
            script_content = script_content.replace('{copiar_skel}', '-k {skel}')
        else:
            script_content = script_content.replace('{copiar_skel}', '')

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="modificar_usuario.sh"'
        return response
    else:
        return render(request, 'usuarios/modificar_usuario.html')

def eliminar_usuario(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        realizar_backup = request.POST.get('backup')

        # Ruta al script de Bash para eliminar usuarios
        script_path = 'usuarios/bash/eliminar_usuario.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        script_content = script_content.replace('{nombre_usuario}', nombre_usuario)

        if realizar_backup == 'yes':
            script_content = script_content.replace('{realizar_backup}', 'S')
        else:
            script_content = script_content.replace('{realizar_backup}', 'N')

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="eliminar_usuario.sh"'
        return response
    else:
        return render(request, 'usuarios/eliminar_usuario.html')

def analizar_contrasena(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        contrasena = request.POST.get('contrasena')

        # Ruta al script de Bash para analizar contraseñas
        script_path = 'usuarios/bash/analizar_contrasena.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        script_content = script_content.replace('{contrasena}', contrasena)
        script_content = script_content.replace('{validacion}', 'True' if validar_contrasena(contrasena) else 'False')

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="analizar_contrasena.sh"'
        return response
    else:
        return render(request, 'usuarios/analizar_contrasena.html')

def validar_contrasena(contrasena):
    # Verificar la longitud de la contraseña
    if len(contrasena) < 8:
        return False

    # Verificar si la contraseña contiene al menos una letra mayúscula
    if not any(caracter.isupper() for caracter in contrasena):
        return False

    # Verificar si la contraseña contiene al menos una letra minúscula
    if not any(caracter.islower() for caracter in contrasena):
        return False

    # Verificar si la contraseña contiene al menos un dígito
    if not any(caracter.isdigit() for caracter in contrasena):
        return False

    # Verificar si la contraseña contiene al menos un símbolo
    if not any(caracter in '!@#$%^&*()_-+={}[]:;"\'|<>,.?/~`' for caracter in contrasena):
        return False

    # Si la contraseña pasa todas las validaciones, se considera segura
    return True

def configurar_permisos(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        directorio = request.POST.get('directorio')
        usuario = request.POST.get('usuario')
        permisos = request.POST.get('permisos')
        permisos_grupo = request.POST.get('permisos_grupo')
        permisos_otros = request.POST.get('permisos_otros')

        # Ruta al script de Bash para configurar permisos
        script_path = 'usuarios/bash/configurar_permisos.sh'

        # Verificar si se proporcionaron datos suficientes
        if directorio and usuario and permisos and permisos_grupo and permisos_otros:
            # Leer contenido del script de Bash
            with open(script_path, 'r') as script_file:
                script_content = script_file.read()

            # Reemplazar marcadores de posición con datos del formulario
            script_content = script_content.replace('{directorio}', directorio)
            script_content = script_content.replace('{usuario}', usuario)
            script_content = script_content.replace('{permisos}', permisos)
            script_content = script_content.replace('{permisos_grupo}', permisos_grupo)
            script_content = script_content.replace('{permisos_otros}', permisos_otros)

            # Devolver el script de Bash como una descarga de archivo
            response = HttpResponse(script_content, content_type='application/x-shellscript')
            response['Content-Disposition'] = 'attachment; filename="configurar_permisos.sh"'
            return response
        else:
            return HttpResponse("Datos insuficientes para configurar permisos.", status=400)
    else:
        return render(request, 'usuarios/configurar_permisos.html')

def cambiar_usuario_grupo(request):
    if request.method == 'POST':
        # Recoger datos del segundo formulario
        directorio = request.POST.get('directorio')
        usuario = request.POST.get('usuario')
        grupo = request.POST.get('grupo')
        tipo =  request.POST.get('tipo')

        # Ruta al script de Bash para configurar permisos
        script_path = 'usuarios/bash/cambiar_usuario_grupo.sh'

        # Leer contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Reemplazar marcadores de posición con datos del segundo formulario
        script_content = script_content.replace('{directorio}', directorio)
        script_content = script_content.replace('{usuario}', usuario)
        script_content = script_content.replace('{grupo}', grupo)
        script_content = script_content.replace('{tipo}', tipo)

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="cambiar_usuario_grupo.sh"'
        return response
    else:
        return render(request, 'usuarios/configurar_permisos.html')
