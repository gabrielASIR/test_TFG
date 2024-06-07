from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator
from django.forms import ValidationError
import os
import re

def crear_usuario(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')
        grupo_principal = request.POST.get('grupo_principal')
        otros_grupos = request.POST.get('otros_grupos')
        nombre_completo = request.POST.get('nombre_completo')
        skel = request.POST.get('skel')
        directorio_principal = request.POST.get('home')
        shell = request.POST.get('shell')
        expire = request.POST.get('expire')
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        inactivo = request.POST.get('inactivo')

        # Validación de campos obligatorios
        if not nombre_usuario or not contrasena or not grupo_principal or not shell:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'Los campos nombre de usuario, contraseña, grupo principal y shell son obligatorios.'})

        # Validación de contraseña
        if len(contrasena) < 6:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'La contraseña debe tener al menos 6 caracteres.'})

        # Validación de shell
        shells_validos = ['/bin/bash', '/bin/sh', '/bin/zsh']
        if shell not in shells_validos:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El shell especificado no es válido.'})

        if not uid.isdigit() or not int(uid) >= 1000:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El UID debe ser un número igual o mayor a 1000'})

        if not gid.isdigit() and gid != '' or (gid.isdigit() and int(gid) < 1000):
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El GID debe ser un número igual o mayor a 1000'})

        # Ruta al script de Bash para crear usuarios
        ruta_script = 'usuarios/bash/crear_usuario.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_usuario}', nombre_usuario)
        contenido_script = contenido_script.replace('{contrasena}', contrasena)
        contenido_script = contenido_script.replace('{grupo_principal}', grupo_principal)
        contenido_script = contenido_script.replace('{directorio_principal}', directorio_principal)
        contenido_script = contenido_script.replace('{shell}', shell)
        if otros_grupos:
            contenido_script = contenido_script.replace('{otros_grupos}', otros_grupos or '')
        if nombre_completo:
            contenido_script = contenido_script.replace('{nombre_completo}', nombre_completo or '')
        if skel:
            contenido_script = contenido_script.replace('{skel}', skel or '/etc/skel')
        if expire:
            contenido_script = contenido_script.replace('{expire}', expire or '')
        if uid:
            contenido_script = contenido_script.replace('{uid}', uid or '')
        if gid:
            contenido_script = contenido_script.replace('{gid}', gid or '')
        if inactivo:
            contenido_script = contenido_script.replace('{inactivo}', inactivo or '')

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
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')

        # Validaciones
        if not prefijo:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El prefijo del usuario es obligatorio.'})

        try:
            inicio = int(inicio)
            fin = int(fin)
        except ValueError:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'Los números de inicio y fin deben ser enteros válidos.'})

        if inicio < 1 or fin < 1:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'Los números de inicio y fin deben ser mayores a 0.'})

        if inicio > fin:
            return render(request, 'usuarios/crear_usuario.html', {'mensaje_error': 'El número de inicio no puede ser mayor que el número de fin.'})

        # Ruta al script de Bash existente
        ruta_script = 'usuarios/bash/crear_usuarios_secuenciales.sh'

        # Función para leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Envío de datos al script bash
        contenido_script = contenido_script.replace('{prefijo}', prefijo)
        contenido_script = contenido_script.replace('{inicio}', str(inicio))
        contenido_script = contenido_script.replace('{fin}', str(fin))

        # Devolver el script de Bash como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="crear_usuarios_secuenciales.sh"'
        return respuesta
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
        skel = request.POST.get('skel')
        directorio_home = request.POST.get('home')
        shell = request.POST.get('shell')
        expira = request.POST.get('expire')
        uid = request.POST.get('uid')
        gid = request.POST.get('gid')
        inactivo = request.POST.get('inactive')

        # Validaciones
        if not nombre_usuario or not grupo_principal or not shell:
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'Los campos nombre de usuario, grupo principal y shell son obligatorios.'})

        if contrasena and len(contrasena) < 6:
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'La contraseña debe tener al menos 6 caracteres.'})
            
        shells_validos = ['/bin/bash', '/bin/sh', '/bin/zsh']
        if shell not in shells_validos:
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'El shell especificado no es válido.'})

        if uid and (not uid.isdigit() or int(uid) < 1000):
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'El UID debe ser un número igual o mayor a 1000.'})

        if gid and (not gid.isdigit() or int(gid) < 1000):
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'El GID debe ser un número igual o mayor a 1000.'})

        if expira:
            if not re.match(r'\d{2}/\d{2}/\d{4}', expira):
                return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'La fecha de expiración no tiene el formato correcto (Día/Mes/Año).'})

        if inactivo and not inactivo.isdigit():
            return render(request, 'usuarios/modificar_usuario.html', {'mensaje_error': 'Los días de inactividad deben ser un número válido.'})

        # Ruta al script de Bash para modificar usuarios
        ruta_script = 'usuarios/bash/modificar_usuario.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_usuario}', nombre_usuario or '')
        contenido_script = contenido_script.replace('{contrasena}', contrasena or '')
        contenido_script = contenido_script.replace('{grupo_principal}', grupo_principal or '')
        contenido_script = contenido_script.replace('{otros_grupos}', otros_grupos or '')
        contenido_script = contenido_script.replace('{nombre_completo}', nombre_completo or '')
        contenido_script = contenido_script.replace('{skel}', skel or '')
        contenido_script = contenido_script.replace('{directorio_home}', directorio_home or '')
        contenido_script = contenido_script.replace('{shell}', shell or '')
        contenido_script = contenido_script.replace('{expira}', expira or '')
        contenido_script = contenido_script.replace('{uid}', uid or '')
        contenido_script = contenido_script.replace('{gid}', gid or '')
        contenido_script = contenido_script.replace('{inactivo}', inactivo or '')

        # Devolver el script de Bash como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="modificar_usuario.sh"'
        return respuesta
    else:
        return render(request, 'usuarios/modificar_usuario.html')

def eliminar_usuario(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        realizar_copia = request.POST.get('realizar_copia')
        directorio_copia = request.POST.get('directorio_copia')
        eliminar_correo = request.POST.get('eliminar_correo')
        eliminar_crontab = request.POST.get('eliminar_crontab')
        forzar_eliminacion = request.POST.get('forzar_eliminacion')
        eliminar_grupos = request.POST.get('eliminar_grupos')
        eliminar_home = request.POST.get('eliminar_home')

        # Validaciones
        mensaje_error = None

        # Validar nombre de usuario
        if not nombre_usuario:
            mensaje_error = "El nombre de usuario es obligatorio."
        # Añadir más validaciones para nombre_usuario si es necesario

        # Validar directorio de copia de seguridad si se especificó
        if realizar_copia == 'yes' and not directorio_copia:
            mensaje_error = "Debe especificar un directorio para la copia de seguridad."
        if directorio_copia and not os.path.exists(directorio_copia):
            mensaje_error = "El directorio especificado para la copia de seguridad no existe."
        if directorio_copia and not os.path.isdir(directorio_copia):
            mensaje_error = "La ruta especificada no es un directorio."

        # Si hay algún error, renderizar el formulario con el mensaje de error
        if mensaje_error:
            return render(request, 'usuarios/eliminar_usuario.html', {'mensaje_error': mensaje_error})

        # Ruta al script de Bash para crear usuarios
        ruta_script = 'usuarios/bash/eliminar_usuario.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_usuario}', nombre_usuario)
        contenido_script = contenido_script.replace('{realizar_copia}', realizar_copia or '')
        contenido_script = contenido_script.replace('{directorio_copia}', directorio_copia or '')
        contenido_script = contenido_script.replace('{eliminar_correo}', eliminar_correo or '')
        contenido_script = contenido_script.replace('{eliminar_crontab}', eliminar_crontab or '')
        contenido_script = contenido_script.replace('{forzar_eliminacion}', forzar_eliminacion or '')
        contenido_script = contenido_script.replace('{eliminar_grupos}', eliminar_grupos or '')
        contenido_script = contenido_script.replace('{eliminar_home}', eliminar_home or '')

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(contenido_script, content_type='application/x-shellscript')
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

        # Validaciones
        mensaje_error = None

        if not directorio:
            mensaje_error = "El directorio es obligatorio."
        elif not os.path.exists(directorio):
            mensaje_error = "El directorio especificado no existe."
        elif not os.path.isdir(directorio):
            mensaje_error = "La ruta especificada no es un directorio."

        if not usuario:
            mensaje_error = "El usuario es obligatorio."

        if permisos not in [str(i) for i in range(8)]:
            mensaje_error = "Los permisos para usuario son inválidos."

        if permisos_grupo not in [str(i) for i in range(8)]:
            mensaje_error = "Los permisos para grupo son inválidos."

        if permisos_otros not in [str(i) for i in range(8)]:
            mensaje_error = "Los permisos para otros son inválidos."

        # Si hay algún error, renderizar el formulario con el mensaje de error
        if mensaje_error:
            return render(request, 'usuarios/configurar_permisos.html', {'mensaje_error': mensaje_error})

        # Ruta al script de Bash para configurar permisos
        ruta_script = 'usuarios/bash/configurar_permisos.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{directorio}', directorio)
        contenido_script = contenido_script.replace('{usuario}', usuario)
        contenido_script = contenido_script.replace('{permisos}', permisos)
        contenido_script = contenido_script.replace('{permisos_grupo}', permisos_grupo)
        contenido_script = contenido_script.replace('{permisos_otros}', permisos_otros)

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(contenido_script, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="configurar_permisos.sh"'
        return response
    else:
        return render(request, 'usuarios/configurar_permisos.html')

def cambiar_usuario_grupo(request):
    if request.method == 'POST':
        # Recoger datos del formulario
        directorio = request.POST.get('directorio')
        usuario = request.POST.get('usuario')
        grupo = request.POST.get('grupo')
        tipo = request.POST.get('tipo')

        # Validaciones
        mensaje_error = None

        if not directorio:
            mensaje_error = "El directorio es obligatorio."

        if tipo == 'u' and not usuario:
            mensaje_error = "El usuario es obligatorio para cambiar el usuario."

        if tipo == 'g' and not grupo:
            mensaje_error = "El grupo es obligatorio para cambiar el grupo."

        if tipo not in ['u', 'g']:
            mensaje_error = "El tipo de cambio es inválido."

        # Si hay algún error, renderizar el formulario con el mensaje de error
        if mensaje_error:
            return render(request, 'usuarios/configurar_permisos.html', {'mensaje_error': mensaje_error})

        # Ruta al script de Bash para cambiar usuario/grupo
        ruta_script = 'usuarios/bash/cambiar_usuario_grupo.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Reemplazar los marcadores de posición con los datos del formulario
        contenido_script = contenido_script.replace('{directorio}', directorio)
        contenido_script = contenido_script.replace('{usuario}', usuario or '')
        contenido_script = contenido_script.replace('{grupo}', grupo or '')
        contenido_script = contenido_script.replace('{tipo}', tipo)

        # Devolver el script de Bash como una descarga de archivo
        response = HttpResponse(contenido_script, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="cambiar_usuario_grupo.sh"'
        return response
    else:
        return render(request, 'usuarios/configurar_permisos.html')
