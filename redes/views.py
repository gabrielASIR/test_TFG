from django.shortcuts import render
from django.http import HttpResponse

def interfaces(request):
    if request.method == 'POST':
        num_interfaces = request.POST.get('num_interfaces')

        # Validación de campos
        if not num_interfaces or not num_interfaces.isdigit():
            return render(request, 'redes/interfaces.html')

        num_interfaces = int(num_interfaces)

        for i in range(1, num_interfaces + 1):
            nombre = request.POST.get(f'nombre_{i}')
            direccion_ip = request.POST.get(f'direccion_ip_{i}')
            mascara_subred = request.POST.get(f'mascara_subred_{i}')
            puerta_enlace = request.POST.get(f'puerta_enlace_{i}')
            dns_primario = request.POST.get(f'dns_primario_{i}')
            dns_secundario = request.POST.get(f'dns_secundario_{i}')
            tipo_conexion = request.POST.get(f'tipo_conexion_{i}')
            estado = request.POST.get(f'estado_{i}')

            # Validación de campos
            if not nombre or not direccion_ip or not mascara_subred or not puerta_enlace:
                return render(request, 'redes/interfaces.html')

            # Ruta al script de Bash existente
            script_path = 'redes/bash/interfaces.sh'

            # Funcion para leer el contenido del script de Bash
            with open(script_path, 'r') as script_file:
                script_content = script_file.read()

            # Envío de datos al script bash
            script_content = script_content.replace('{nombre}', nombre)
            script_content = script_content.replace('{direccion_ip}', direccion_ip)
            script_content = script_content.replace('{mascara_subred}', mascara_subred)
            script_content = script_content.replace('{puerta_enlace}', puerta_enlace)
            script_content = script_content.replace('{dns_primario}', dns_primario)
            script_content = script_content.replace('{dns_secundario}', dns_secundario)
            script_content = script_content.replace('{tipo_conexion}', tipo_conexion)
            script_content = script_content.replace('{estado}', estado)

            # Funcion para devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
            response = HttpResponse(script_content, content_type='application/x-shellscript')
            response['Content-Disposition'] = f'attachment; filename="interfaces_{i}.sh"'
            return response
    else:
        return render(request, 'redes/interfaces.html')

def dhcp(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_cliente = request.POST.get('nombre_cliente')
        direccion_ip = request.POST.get('direccion_ip')
        mac_address = request.POST.get('mac_address')
        interfaz = request.POST.get('interfaz')
        direccion_servidor = request.POST.get('direccion_servidor')

        # Ruta al script de Bash existente
        script_path = 'redes/bash/dhcp_client.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configuración del cliente DHCP
        script_content = script_content.replace('{nombre_cliente}', nombre_cliente)
        script_content = script_content.replace('{direccion_ip}', direccion_ip)
        script_content = script_content.replace('{mac_address}', mac_address)
        script_content = script_content.replace('{interfaz}', interfaz)
        script_content = script_content.replace('{direccion_servidor}', direccion_servidor)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="dhcp_client.sh"'
        return response
    else:
        return render(request, 'redes/dhcp.html')

def reserva_ip(request):
    if request.method == 'POST':
        # Recoge los datos del formulario de reserva de IP
        nombre_cliente_reserva = request.POST.get('nombre_cliente_reserva')
        direccion_ip_reserva = request.POST.get('direccion_ip_reserva')
        mac_address_reserva = request.POST.get('mac_address_reserva')
        direccion_servidor_reserva = request.POST.get('direccion_servidor_reserva')
        nombre_usuario_reserva = request.POST.get('nombre_usuario')
        carpeta_destino_reserva = request.POST.get('carpeta_destino')

        # Ruta al script de Bash para la reserva de IP
        script_path = 'redes/bash/reserva_ip.sh'

        # Leer el contenido del script de reserva de IP
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configuración para la reserva de IP
        script_content = script_content.replace('{nombre_cliente}', nombre_cliente_reserva)
        script_content = script_content.replace('{direccion_ip}', direccion_ip_reserva)
        script_content = script_content.replace('{mac_address}', mac_address_reserva)
        script_content = script_content.replace('{direccion_servidor}', direccion_servidor_reserva)
        script_content = script_content.replace('{nombre_usuario}', nombre_usuario_reserva)
        script_content = script_content.replace('{carpeta_destino}', carpeta_destino_reserva)

        # Devolver el script de reserva de IP con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="reserva_ip.sh"'
        return response
    else:
        return render(request, 'redes/dhcp.html')

def enrutamiento(request):
    if request.method == 'POST':
        red_origen = request.POST.get('red_origen')
        rutas_destino = request.POST.getlist('red_destino[]')
        mascaras_destino = request.POST.getlist('mascara_destino[]')
        gateways = request.POST.getlist('gateway[]')

        # Generar configuraciones de enrutamiento para cada ruta
        configuraciones = ''
        for red_destino, mascara, gateway in zip(rutas_destino, mascaras_destino, gateways):
            configuraciones += f"ip route add {red_destino}/{mascara} via {gateway}\n"

        # Ruta al script de Bash existente para enrutamiento
        script_path = 'redes/bash/enrutamiento.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Reemplazar marcadores de posición en el script de Bash con las configuraciones de enrutamiento
        script_content = script_content.replace('{red_origen}', red_origen)
        script_content = script_content.replace('{configuraciones}', configuraciones)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="enrutamiento.sh"'
        return response
    else:
    	return render(request, 'redes/enrutamiento.html')

def pingtester(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre_equipo = request.POST.get('nombre_equipo')
        direccion_ip = request.POST.get('direccion_ip')
        num_intentos = request.POST.get('num_intentos', 4)  # Valor por defecto: 4
        historico = request.POST.get('historico')

        # Ruta al script de Bash existente
        script_path = 'redes/bash/pingtester.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configurar el script de Bash con los datos del formulario
        script_content = script_content.replace('{direccion_ip}', direccion_ip)
        script_content = script_content.replace('{num_intentos}', num_intentos)
        script_content = script_content.replace('{historico}', historico)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="pingtester.sh"'
        return response
    else:
        return render(request, 'redes/pingtester.html')
