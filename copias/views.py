from django.shortcuts import render
from django.http import HttpResponse
import os

def configuracion_backups(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_backup = request.POST.get('nombre_backup')
        ruta_origen = request.POST.get('ruta_origen')
        ruta_destino = request.POST.get('ruta_destino')
        metodo_copia = request.POST.get('metodo_copia')
        clave_encriptacion = request.POST.get('clave_encriptacion')
        compresion = request.POST.get('compresion')
        exclusiones = request.POST.get('exclusiones')

        # Verificar si algún campo está vacío
        if not nombre_backup or not ruta_origen or not ruta_destino:
            return HttpResponse('Por favor, complete todos los campos del formulario.')

        # Verificar si las rutas de origen y destino existen
        if not os.path.exists(ruta_origen):
            return HttpResponse(f'La ruta de origen "{ruta_origen}" no existe.')
        if not os.path.exists(ruta_destino):
            return HttpResponse(f'La ruta de destino "{ruta_destino}" no existe.')

        # Verificar si las rutas de origen y destino contienen archivos (si se especifican)
        if not os.listdir(ruta_origen):
            return HttpResponse(f'La ruta de origen "{ruta_origen}" está vacía.')
        if metodo_copia != 'cp' and not os.listdir(ruta_destino):
            return HttpResponse(f'La ruta de destino "{ruta_destino}" está vacía.')

        # Ruta al script de Bash existente
        script_path = 'copias/bash/copia_seguridad.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configurar el script con los datos del formulario
        script_content = script_content.replace('{nombre_backup}', nombre_backup)
        script_content = script_content.replace('{ruta_origen}', ruta_origen)
        script_content = script_content.replace('{ruta_destino}', ruta_destino)
        script_content = script_content.replace('{metodo_copia}', metodo_copia)
        script_content = script_content.replace('{clave_encriptacion}', clave_encriptacion)
        script_content = script_content.replace('{compresion}', compresion)
        script_content = script_content.replace('{exclusiones}', exclusiones)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="copia_seguridad.sh"'
        return response

    else:
        return render(request, 'copias/configuracion_backups.html')

def programar_copia(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_copia = request.POST.get('nombre_copia')
        dias_semana = request.POST.getlist('dias_semana')  # Obtener lista de días seleccionados
        hora_ejecucion = request.POST.get('hora_ejecucion')
        frecuencia = request.POST.get('frecuencia')
        numero_ejecuciones = int(request.POST.get('numero_ejecuciones'))

        # Verificar si algún campo está vacío
        if not nombre_copia or not dias_semana or not hora_ejecucion or not frecuencia:
            return HttpResponse('Por favor, complete todos los campos del formulario.')

        # Comprobar si se ha seleccionado al menos un día de la semana
        if not dias_semana:
            return HttpResponse('Por favor, seleccione al menos un día de la semana.')

        # Procesar los días seleccionados para formar una cadena de días
        dias_semana_str = ','.join(dias_semana)

        # Ruta al script de Bash existente
        script_path = 'copias/bash/copia_programada.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configurar el script con los datos del formulario
        script_content = script_content.replace('{nombre_copia}', nombre_copia)
        script_content = script_content.replace('{dias_semana}', dias_semana_str)
        script_content = script_content.replace('{hora_ejecucion}', hora_ejecucion)
        script_content = script_content.replace('{frecuencia}', frecuencia)
        script_content = script_content.replace('{numero_ejecuciones}', str(numero_ejecuciones))

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="copia_programada.sh"'
        return response

    else:
        return render(request, 'copias/programacion_copias.html')

def configuracion_nas(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_nas = request.POST.get('nombre_nas')
        direccion_nas = request.POST.get('direccion_nas')
        usuario_nas = request.POST.get('usuario_nas')
        contrasena_nas = request.POST.get('contrasena_nas')
        protocolo = request.POST.get('protocolo')
        ruta_montaje = request.POST.get('ruta_montaje')
        permisos = request.POST.get('permisos')
        modo_subida = request.POST.get('modo_subida')

        # Verificar que todos los campos estén completos
        if not nombre_nas or not direccion_nas or not usuario_nas or not contrasena_nas or not protocolo or not ruta_montaje or not permisos or not modo_subida:
            return HttpResponse('Por favor, complete todos los campos del formulario.')

        # Leer el contenido del script de configuración del NAS
        with open('copias/bash/configuracion_nas.sh', 'r') as script_file:
            script_content = script_file.read()

        # Configurar el script con los datos del formulario
        script_content = script_content.replace('{nombre_nas}', nombre_nas)
        script_content = script_content.replace('{direccion_nas}', direccion_nas)
        script_content = script_content.replace('{usuario_nas}', usuario_nas)
        script_content = script_content.replace('{contrasena_nas}', contrasena_nas)
        script_content = script_content.replace('{protocolo}', protocolo)
        script_content = script_content.replace('{ruta_montaje}', ruta_montaje)
        script_content = script_content.replace('{permisos}', permisos)
        script_content = script_content.replace('{modo_subida}', modo_subida)

        # Devolver el script de configuración del NAS como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="configuracion_nas.sh"'
        return response
    else:
        return render(request, 'copias/configuracion_nas.html')

def subida_archivos_nas(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_nas = request.POST.get('nombre_nas')
        ruta_montaje = request.POST.get('ruta_montaje')
        archivos = request.POST.get('archivos')
        usuario_nas = request.POST.get('usuario_nas')
        contrasena_nas = request.POST.get('contrasena_nas')
        sobrescribir = request.POST.get('sobrescribir')
        compresion = request.POST.get('compresion')

	# Verificar que todos los campos estén completos
        if not nombre_nas or not ruta_montaje:
            return HttpResponse('Por favor, complete todos los campos del formulario.')

        # Verificar si algún campo está vacío
        if not archivos:
            return HttpResponse('Por favor, especifique al menos una ruta de archivo.')

        # Verificar si se proporcionó el usuario y la contraseña del NAS
        if not usuario_nas or not contrasena_nas:
            return HttpResponse('Por favor, especifique el usuario y la contraseña del NAS.')

        # Verificar si las rutas de archivos existen
        archivos = archivos.split('\n')
        for ruta in archivos:
            if not os.path.exists(ruta.strip()):
                return HttpResponse(f'La ruta de archivo "{ruta.strip()}" no existe.')

        # Ruta al script de Bash existente
        script_path = 'copias/bash/subida_archivos_nas.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configurar el script con los datos del formulario
        script_content = script_content.replace('{nombre_nas}', nombre_nas)
        script_content = script_content.replace('{ruta_montaje}', ruta_montaje)
        script_content = script_content.replace('{usuario_nas}', usuario_nas)
        script_content = script_content.replace('{contrasena_nas}', contrasena_nas)
        script_content = script_content.replace('{sobrescribir}', '--sobrescribir' if sobrescribir else '')
        script_content = script_content.replace('{compresion}', '--compresion=' + compresion if compresion != 'none' else '')

        # Añadir las rutas de archivos al script de Bash
        script_content += '\n'.join(f'"{ruta.strip()}"' for ruta in archivos)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="subida_archivos_nas.sh"'
        return response

    else:
        return render(request, 'copias/subida_archivos_nas.html')
