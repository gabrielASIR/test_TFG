from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator
from django.forms import ValidationError
import os

def configuracion_backups(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_copia = request.POST.get('nombre_copia')
        ruta_origen = request.POST.get('ruta_origen')
        ruta_destino = request.POST.get('ruta_destino')
        metodo_copia = request.POST.get('metodo_copia')
        clave_encriptacion = request.POST.get('clave_encriptacion')
        compresion = request.POST.get('compresion')
        exclusiones = request.POST.get('exclusiones')

        # Validación de campos obligatorios
        if not nombre_copia:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'El nombre de la copia es obligatorio.'})
        if not ruta_origen:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'La ruta de origen es obligatoria.'})
        if not ruta_destino:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'La ruta de destino es obligatoria.'})
        
        # Validación adicional de la clave de encriptación si se proporciona
        if clave_encriptacion and len(clave_encriptacion) < 8:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'La clave de encriptación debe tener al menos 8 caracteres.'})
        
        # Validación de método de copia
        if metodo_copia not in ['cp', 'rsync', 'tar']:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'Método de copia no válido.'})

        # Validación de compresión
        if compresion not in ['none', 'gzip', 'bzip2']:
            return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'Método de compresión no válido.'})

        # Validación de exclusiones (si se proporciona)
        if exclusiones:
            exclusiones_lista = exclusiones.split(',')
            for exclusion in exclusiones_lista:
                if not exclusion.strip():
                    return render(request, 'copias/configuracion_backups.html', {'mensaje_error': 'Cada exclusión debe ser una ruta válida.'})

        # Ruta al script de Bash existente
        ruta_script = 'copias/bash/copia_seguridad.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configurar el script con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_backup}', nombre_copia)
        contenido_script = contenido_script.replace('{ruta_origen}', ruta_origen)
        contenido_script = contenido_script.replace('{ruta_destino}', ruta_destino)
        contenido_script = contenido_script.replace('{metodo_copia}', metodo_copia)
        contenido_script = contenido_script.replace('{clave_encriptacion}', clave_encriptacion)
        contenido_script = contenido_script.replace('{compresion}', compresion)
        contenido_script = contenido_script.replace('{exclusiones}', exclusiones)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="copia_seguridad.sh"'
        return respuesta
    
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
