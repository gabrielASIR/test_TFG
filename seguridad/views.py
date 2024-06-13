from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator, validate_email
from django.forms import ValidationError
import os

validador_ipv4 = RegexValidator(
    regex=r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    message='Introduce una dirección IPv4 válida.',
    code='invalid_ipv4'
)

validador_pais = RegexValidator(
    regex=r'^[A-Z]{2}$',
    message='Introduce un código de país válido de 2 letras (ISO 3166-1 alfa-2).',
    code='codigo_pais_invalido'
)

def firewall(request):
    if request.method == 'POST':
        politica_por_defecto = request.POST.get('politica_por_defecto')
        borrar_configuraciones = request.POST.get('borrar_configuraciones')
        num_reglas = request.POST.get('num_reglas')

        if not num_reglas or not num_reglas.isdigit():
            return render(request, 'seguridad/firewall.html', {'mensaje_error': 'Número de reglas inválido.'})

        num_reglas = int(num_reglas)
        all_scripts = []

        if borrar_configuraciones:
            all_scripts.append("iptables -F")

        for i in range(1, num_reglas + 1):
            tabla = request.POST.get(f'tabla_{i}')
            opcion = request.POST.get(f'opcion_{i}')
            cadena = request.POST.get(f'cadena_{i}')
            direccion_origen = request.POST.get(f'direccion_origen_{i}')
            puerto_origen = request.POST.get(f'puerto_origen_{i}')
            direccion_destino = request.POST.get(f'direccion_destino_{i}')
            puerto_destino = request.POST.get(f'puerto_destino_{i}')
            protocolo = request.POST.get(f'protocolo_{i}')
            accion = request.POST.get(f'accion_{i}')

            if not tabla or not opcion or not cadena or not accion:
                return render(request, 'seguridad/firewall.html', {'mensaje_error': 'Todos los campos son obligatorios.', 'num_reglas': num_reglas})

            if direccion_origen:
                try:
                    validador_ipv4(direccion_origen)
                except ValidationError:
                    return render(request, 'seguridad/firewall.html', {'mensaje_error': f'Dirección de origen inválida en la regla {i}.', 'num_reglas': num_reglas})

            if direccion_destino:
                try:
                    validador_ipv4(direccion_destino)
                except ValidationError:
                    return render(request, 'seguridad/firewall.html', {'mensaje_error': f'Dirección de destino inválida en la regla {i}.', 'num_reglas': num_reglas})

            if puerto_origen and (not puerto_origen.isdigit() or not 0 < int(puerto_origen) <= 65535):
                return render(request, 'seguridad/firewall.html', {'mensaje_error': f'Puerto de origen inválido en la regla {i}.', 'num_reglas': num_reglas})

            if puerto_destino and (not puerto_destino.isdigit() or not 0 < int(puerto_destino) <= 65535):
                return render(request, 'seguridad/firewall.html', {'mensaje_error': f'Puerto de destino inválido en la regla {i}.', 'num_reglas': num_reglas})

            # Ruta al script de Bash existente
            ruta_script = 'seguridad/bash/firewall.sh'

            # Función para leer el contenido del script de Bash
            with open(ruta_script, 'r') as archivo_script:
                contenido_script = archivo_script.read()

            # Reemplazar placeholders con los valores de las variables
            contenido_script = contenido_script.replace('{politica_por_defecto}', politica_por_defecto)
            contenido_script = contenido_script.replace('{borrar_configuraciones}', borrar_configuraciones or '')
            contenido_script = contenido_script.replace('{tabla}', tabla)
            contenido_script = contenido_script.replace('{opcion}', opcion)
            contenido_script = contenido_script.replace('{cadena}', cadena)
            contenido_script = contenido_script.replace('{direccion_origen}', direccion_origen or '')
            contenido_script = contenido_script.replace('{puerto_origen}', puerto_origen or '')
            contenido_script = contenido_script.replace('{direccion_destino}', direccion_destino or '')
            contenido_script = contenido_script.replace('{puerto_destino}', puerto_destino or '')
            contenido_script = contenido_script.replace('{protocolo}', protocolo or '')
            contenido_script = contenido_script.replace('{accion}', accion)

            all_scripts.append(contenido_script)

        script_completo = "\n".join(all_scripts)

        # Devolver una respuesta al usuario
        respuesta = HttpResponse(script_completo, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="firewall.sh"'
        return respuesta

    else:
        return render(request, 'seguridad/firewall.html', {'num_reglas': 1})

def proxy(request):
    if request.method == 'POST':
        num_reglas = request.POST.get('num_reglas')
        ruta_configuracion = request.POST.get('ruta_configuracion')

        if not num_reglas or not num_reglas.isdigit():
            return render(request, 'seguridad/proxy.html', {'mensaje_error': 'Número de reglas inválido.'})

        num_reglas = int(num_reglas)
        all_scripts = []

        for i in range(1, num_reglas + 1):
            tipo_regla = request.POST.get(f'tipo_regla_{i}')
            acl = request.POST.get(f'acl_{i}')
            tipo_acl = request.POST.get(f'tipo_acl_{i}')
            http_access = request.POST.get(f'http_access_{i}')
            accion_http_access = request.POST.get(f'accion_http_access_{i}')

            if not acl or not http_access:
                return render(request, 'seguridad/proxy.html', {'mensaje_error': 'Se debe especificar una configuracion.', 'num_reglas': num_reglas})

            # Ruta al script de Bash existente
            ruta_script = 'seguridad/bash/proxy.sh'

            # Función para leer el contenido del script de Bash
            with open(ruta_script, 'r') as archivo_script:
                contenido_script = archivo_script.read()

            # Reemplazar placeholders con los valores de las variables
            contenido_script = contenido_script.replace('{acl}', acl)
            contenido_script = contenido_script.replace('{tipo_acl}', tipo_acl)
            contenido_script = contenido_script.replace('{http_access}', http_access)
            contenido_script = contenido_script.replace('{accion_http_access}', accion_http_access)

            all_scripts.append(contenido_script)

        script_completo = "\n".join(all_scripts)

        # Reemplazar los marcadores de posición con los valores proporcionados por el usuario
        script_completo = script_completo.replace('{ruta_configuracion}', ruta_configuracion)

        # Devolver una respuesta al usuario
        respuesta = HttpResponse(script_completo, content_type='text/plain')
        respuesta['Content-Disposition'] = 'attachment; filename="proxy.sh"'
        return respuesta

    else:
        return render(request, 'seguridad/proxy.html', {'num_reglas': 1})

def certificados(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_certificado = request.POST.get('nombre_certificado')
        organizacion = request.POST.get('organizacion')
        unidad_organizacional = request.POST.get('unidad_organizacional')
        localidad = request.POST.get('localidad')
        provincia = request.POST.get('provincia')
        pais = request.POST.get('pais')
        correo_electronico = request.POST.get('correo_electronico')
        departamento = request.POST.get('departamento')
        clave = request.POST.get('clave')
        repeticion_clave = request.POST.get('repeticion_clave')
        comentarios = request.POST.get('comentarios')
        directorio_salida = request.POST.get('directorio_salida')

        # Validaciones de campos
        if not nombre_certificado or not clave or not repeticion_clave or not directorio_salida:
            return render(request, 'seguridad/certificados.html', {'mensaje_error': 'Nombre del certificado, clave, repetir clave y directorio de salida son campos requeridos.'})

        if clave != repeticion_clave:
            return render(request, 'seguridad/certificados.html', {'mensaje_error': 'Las claves no coinciden.'})

        if pais:
            try:
                validador_pais(pais)
            except ValidationError:
                return render(request, 'seguridad/certificados.html', {'mensaje_error': 'Código de país inválido.'})

        if correo_electronico:
            try:
                validate_email(correo_electronico)
            except ValidationError:
                return render(request, 'seguridad/certificados.html', {'mensaje_error': 'Correo electrónico inválido.'})

        # Ruta al script de Bash para generar certificados
        ruta_script = 'seguridad/bash/generar_certificado.sh'

        # Leer el contenido del script de Bash
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configurar los parámetros del script de Bash
        contenido_script = contenido_script.replace('{nombre_certificado}', nombre_certificado)
        contenido_script = contenido_script.replace('{organizacion}', organizacion or '')
        contenido_script = contenido_script.replace('{unidad_organizacional}', unidad_organizacional or '')
        contenido_script = contenido_script.replace('{localidad}', localidad or '')
        contenido_script = contenido_script.replace('{provincia}', provincia or '')
        contenido_script = contenido_script.replace('{pais}', pais or '')
        contenido_script = contenido_script.replace('{correo_electronico}', correo_electronico or '')
        contenido_script = contenido_script.replace('{departamento}', departamento or '')
        contenido_script = contenido_script.replace('{clave}', clave)
        contenido_script = contenido_script.replace('{comentarios}', comentarios or '')
        contenido_script = contenido_script.replace('{directorio_salida}', directorio_salida)

        # Generar el archivo de descarga
        respuesta = HttpResponse(contenido_script, content_type='text/plain')
        respuesta['Content-Disposition'] = 'attachment; filename="generar_certificado.sh"'
        return respuesta
    else:
        # Renderiza el formulario vacío si no se envió un POST
        return render(request, 'seguridad/certificados.html')
