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
        # Recopila los datos del formulario
        acl_list = request.POST.getlist('acl[]')
        tipo_acl_list = request.POST.getlist('tipo_acl[]')
        direccion_ip_list = request.POST.getlist('direccion_ip[]')
        mascara_subred_list = request.POST.getlist('mascara_subred[]')
        detalle_acl_list = request.POST.getlist('detalle_acl[]')
        permitir_denegar_list = request.POST.getlist('permitir_denegar[]')
        ruta_configuracion = request.POST.get('ruta_configuracion')

        # Leer el contenido del script de Bash
        with open('seguridad/bash/proxy.sh', 'r') as script_file:
            script_content = script_file.read()

        # Configuración de las reglas de Squid
        for i in range(len(acl_list)):
            script_content += f"\n# Regla {i+1}\n"
            script_content += f"acl {acl_list[i]} {tipo_acl_list[i]} {direccion_ip_list[i]}/{mascara_subred_list[i]}\n"
            script_content += f"http_access {permitir_denegar_list[i]} {detalle_acl_list[i]} {acl_list[i]}\n"

        # Reemplazar los marcadores de posición con los valores proporcionados por el usuario
        script_content = script_content.replace('{ruta_configuracion}', ruta_configuracion)

        # Generar el archivo de descarga
        response = HttpResponse(script_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="proxy.sh"'
        return response

    # Renderiza el formulario vacío si no se envió un POST
    return render(request, 'seguridad/proxy.html')

def certificados(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_certificado = request.POST.get('nombre_certificado')
        clave = request.POST.get('clave')
        repeticion_clave = request.POST.get('repeticion_clave')
        directorio_salida = request.POST.get('directorio_salida')

        # Validaciones de campos
        if not nombre_certificado or not clave or not repeticion_clave:
            return HttpResponse("Error: Nombre del certificado y clave son campos requeridos.")

        if clave != repeticion_clave:
            return HttpResponse("Error: Las claves no coinciden.")

        if not directorio_salida:
            return HttpResponse("Error: Debe especificar un directorio donde guardar los certificados")

        # Ruta al script de Bash para generar certificados
        script_path = 'seguridad/bash/generar_certificado.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configurar los parámetros del script de Bash
        script_content = script_content.replace('{nombre_certificado}', nombre_certificado)
        script_content = script_content.replace('{clave}', clave)
        script_content = script_content.replace('{repeticion_clave}', repeticion_clave)
        script_content = script_content.replace('{directorio_salida}', directorio_salida)

        # Generar el archivo de descarga
        response = HttpResponse(script_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="generar_certificado.sh"'
        return response
    else:
        # Renderiza el formulario vacío si no se envió un POST
        return render(request, 'seguridad/certificados.html')
