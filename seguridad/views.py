from django.shortcuts import render
from django.http import HttpResponse
import os

def firewall(request):
    if request.method == 'POST':
        politica_por_defecto = request.POST.get('politica_por_defecto')
        borrar_configuraciones = request.POST.get('borrar_configuraciones', False)
        tablas = request.POST.getlist('tabla')
        opciones = request.POST.getlist('opcion')
        cadenas = request.POST.getlist('cadena')
        direcciones_origen = request.POST.getlist('direccion_origen')
        puertos_origen = request.POST.getlist('puerto_origen')
        direcciones_destino = request.POST.getlist('direccion_destino')
        puertos_destino = request.POST.getlist('puerto_destino')
        protocolos = request.POST.getlist('protocolo')
        acciones = request.POST.getlist('accion')

        num_reglas = len(tablas)

        # Leer el contenido del script de Bash
        script_path = os.path.join('seguridad', 'bash', 'firewall.sh')
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configuración de la política por defecto
        script_content = script_content.replace('{politica_por_defecto}', politica_por_defecto)

        # Comprueba si se debe borrar las configuraciones existentes
        if borrar_configuraciones:
            script_content = script_content.replace('{borrar_configuraciones}', 'on')
        else:
            script_content = script_content.replace('{borrar_configuraciones}', '')

        # Generar el contenido del script con las reglas
        rules_content = ""
        for i in range(num_reglas):
            rules_content += f"""
            tabla="{tablas[i]}"
            opcion="{opciones[i]}"
            cadena="{cadenas[i]}"
            direccion_origen="{direcciones_origen[i]}"
            puerto_origen="{puertos_origen[i]}"
            direccion_destino="{direcciones_destino[i]}"
            puerto_destino="{puertos_destino[i]}"
            protocolo="{protocolos[i]}"
            accion="{acciones[i]}"

            # Validar que los campos necesarios no estén vacíos
            if [ -n "$tabla" ] && [ -n "$opcion" ] && [ -n "$accion" ]; then
                # Montar el comando de iptables y ejecutarlo
                comando_iptables="iptables -t $tabla $opcion $cadena"

                if [ -n "$direccion_origen" ]; then
                    comando_iptables+=" -s $direccion_origen"
                fi
                if [ -n "$puerto_origen" ]; then
                    comando_iptables+=" --sport $puerto_origen"
                fi
                if [ -n "$direccion_destino" ]; then
                    comando_iptables+=" -d $direccion_destino"
                fi
                if [ -n "$puerto_destino" ]; then
                    comando_iptables+=" --dport $puerto_destino"
                fi
                if [ -n "$protocolo" ] && [ "$protocolo" != "all" ]; then
                    comando_iptables+=" -p $protocolo"
                fi
                comando_iptables+=" -j $accion"

                # Ejecutar el comando de iptables
                $comando_iptables

                echo "Configuraciones aplicadas correctamente"
            else
                echo "Error: algunos campos necesarios están vacíos. La regla no se aplicará."
            fi
            """

        # Insertar las reglas generadas en el script
        script_content = script_content.replace('{rules_content}', rules_content)

        # Generar la respuesta como un archivo para descarga
        response = HttpResponse(script_content, content_type='application/x-sh')
        response['Content-Disposition'] = f'attachment; filename=firewall_{politica_por_defecto}.sh'
        return response
    else:
        return render(request, 'seguridad/firewall.html')

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
