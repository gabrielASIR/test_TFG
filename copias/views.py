from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator
from django.forms import ValidationError
import os

validador_ipv4 = RegexValidator(
    regex=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    message='Introduce una dirección IPv4 válida.',
    code='invalid_ipv4'
)

def configuracion_backups(request):
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre_copia = request.POST.get('nombre_backup')
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
        hora = request.POST.get('hora')
        minutos = request.POST.get('minutos')

        # Validación de campos obligatorios
        if not nombre_copia:
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'El nombre de la copia es obligatorio.'})
        if not dias_semana:
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'Seleccione al menos un día de la semana.'})
        if not hora:
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'La hora de ejecución es obligatoria.'})
        if not minutos:
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'Los minutos de ejecucion son obligatorios'})

        # Validación de formato de hora y minutos
        try:
            hora = int(hora)
            minutos = int(minutos)
            if not (0 <= hora < 24) or not (0 <= minutos < 60):
                raise ValueError
        except ValueError:
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'Introduzca un tiempo valido. Hora de 0-24, minutos de 0-60.'})

        # Procesar los días seleccionados para formar una cadena de días
        dias_validos = ['1', '2', '3', '4', '5', '6', '0']
        if any(dia not in dias_validos for dia in dias_semana):
            return render(request, 'copias/programacion_copias.html', {'mensaje_error': 'Días de la semana no válidos.'})

        dias_semana_str = ','.join(dias_semana)

        # Ruta al script de Bash existente
        ruta_script = 'copias/bash/copia_programada.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configurar el script con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_copia}', nombre_copia)
        contenido_script = contenido_script.replace('{dias_semana}', dias_semana_str)
        contenido_script = contenido_script.replace('{hora}', str(hora))
        contenido_script = contenido_script.replace('{minutos}', str(minutos))

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="copia_programada.sh"'
        return respuesta

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

        # Validación de campos obligatorios
        if not nombre_nas.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'El nombre del NAS es obligatorio.'})
        if not direccion_nas.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'La dirección del NAS es obligatoria.'})
        if not usuario_nas.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'El usuario del NAS es obligatorio.'})
        if not contrasena_nas.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'La contraseña del NAS es obligatoria.'})
        if not protocolo:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'El protocolo de montaje es obligatorio.'})
        if not ruta_montaje.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'La ruta de montaje es obligatoria.'})
        if not permisos.strip():
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'Los permisos de montaje son obligatorios.'})
        if not modo_subida:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'El modo de subida es obligatorio.'})

	# Validacion de la direccion
        try:
            validador_ipv4(direccion_nas)
        except ValidationError:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'Introduce una dirección IPv4 válida.'})

        # Verificar si la contraseña del NAS contiene al menos 8 caracteres
        if len(contrasena_nas) < 8:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'La contraseña del NAS debe tener al menos 8 caracteres.'})
	    
        # Validación del protocolo
        if protocolo not in ['cifs', 'nfs']:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'Protocolo no válido. Debe ser cifs o nfs.'})

        # Validacion de permisos
        if permisos not in [str(i) for i in range(776)]:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'Permisos no válidos. Establecer de 000 a 775.'})
	    
        # Validación del modo de subida
        if modo_subida not in ['manual', 'automatico']:
            return render(request, 'copias/configuracion_nas.html', {'mensaje_error': 'Modo de subida no válido. Debe ser manual o automatico'})

        # Ruta al script de Bash existente
        script_path = 'copias/bash/configuracion_nas.sh'

	# Leer el contenido del script de Bash
        with open(script_path, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configurar el script con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_nas}', nombre_nas)
        contenido_script = contenido_script.replace('{direccion_nas}', direccion_nas)
        contenido_script = contenido_script.replace('{usuario_nas}', usuario_nas)
        contenido_script = contenido_script.replace('{contrasena_nas}', contrasena_nas)
        contenido_script = contenido_script.replace('{protocolo}', protocolo)
        contenido_script = contenido_script.replace('{ruta_montaje}', ruta_montaje)
        contenido_script = contenido_script.replace('{permisos}', permisos)
        contenido_script = contenido_script.replace('{modo_subida}', modo_subida)

        # Devolver el script de configuración del NAS como una descarga de archivo
        response = HttpResponse(contenido_script, content_type='application/x-shellscript')
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

        # Verificar que todos los campos obligatorios estén completos
        if not nombre_nas or not ruta_montaje or not archivos or not usuario_nas or not contrasena_nas:
            return render(request, 'copias/subida_archivos_nas.html', {'mensaje_error': 'Por favor, complete todos los campos obligatorios del formulario.'})

        # Verificar si se proporcionaron rutas de archivo
        if not archivos.strip():
            return render(request, 'copias/subida_archivos_nas.html', {'mensaje_error': 'Por favor, especifique al menos una ruta de archivo.'})

        # Verificar si el nombre del NAS y el usuario contienen caracteres alfanuméricos y guiones bajos
        if not nombre_nas.isalnum() or not usuario_nas.isalnum():
            return render(request, 'copias/subida_archivos_nas.html', {'mensaje_error': 'El nombre del NAS y el usuario deben contener solo caracteres alfanuméricos y guiones bajos.'})

        # Verificar si la contraseña del NAS contiene al menos 8 caracteres
        if len(contrasena_nas) < 8:
            return render(request, 'copias/subida_archivos_nas.html', {'mensaje_error': 'La contraseña del NAS debe tener al menos 8 caracteres.'})

        # Ruta al script de Bash existente
        ruta_script = 'copias/bash/subida_archivos_nas.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configurar el script con los datos del formulario
        contenido_script = contenido_script.replace('{nombre_nas}', nombre_nas)
        contenido_script = contenido_script.replace('{ruta_montaje}', ruta_montaje)
        contenido_script = contenido_script.replace('{usuario_nas}', usuario_nas)
        contenido_script = contenido_script.replace('{contrasena_nas}', contrasena_nas)
        contenido_script = contenido_script.replace('{sobrescribir}', '--sobrescribir' if sobrescribir else '')
        contenido_script = contenido_script.replace('{compresion}', '--compresion=' + compresion if compresion != 'none' else '')

        # Añadir las rutas de archivos al script de Bash
        contenido_script += '\n'.join(f'"{ruta.strip()}"' for ruta in archivos.split('\n'))

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="subida_archivos_nas.sh"'
        return respuesta

    else:
        return render(request, 'copias/subida_archivos_nas.html')
