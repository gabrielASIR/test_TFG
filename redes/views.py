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

validador_mac = RegexValidator(
    regex=r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
    message='Introduce una dirección MAC válida.',
    code='invalid_mac'
)

def interfaces(request):
    if request.method == 'POST':
        num_interfaces = request.POST.get('num_interfaces')

        # Validación de campos
        if not num_interfaces or not num_interfaces.isdigit():
            return render(request, 'redes/interfaces.html', {'mensaje_error': 'Número de interfaces inválido.'})

        num_interfaces = int(num_interfaces)
        all_scripts = []

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
                return render(request, 'redes/interfaces.html', {'mensaje_error': 'Todos los campos son obligatorios.'})

            # Validación de dirección IP
            try:
                validador_ipv4(direccion_ip)
            except ValidationError:
                return render(request, 'redes/interfaces.html', {'mensaje_error': 'Introduce una dirección IPv4 válida.', 'num_interfaces': num_interfaces})

            # Validación de máscara de subred
            if not mascara_subred.isdigit() or not 0 <= int(mascara_subred) <= 32:
                return render(request, 'redes/interfaces.html', {'mensaje_error': 'La máscara de subred debe ser un número entre 0 y 32.', 'num_interfaces': num_interfaces})

            # Validación de puerta de enlace y DNS
            try:
                validador_ipv4(puerta_enlace)
                validador_ipv4(dns_primario)
                validador_ipv4(dns_secundario)
            except ValidationError:
                return render(request, 'redes/interfaces.html', {'mensaje_error': 'Introduce una dirección IPv4 válida para la puerta de enlace y los DNS.', 'num_interfaces': num_interfaces})

            # Ruta al script de Bash existente
            ruta_script = 'redes/bash/interfaces.sh'

            # Función para leer el contenido del script de Bash
            with open(ruta_script, 'r') as archivo_script:
                contenido_script = archivo_script.read()

            # Envío de datos al script bash
            contenido_script = contenido_script.replace('{nombre}', nombre)
            contenido_script = contenido_script.replace('{direccion_ip}', direccion_ip)
            contenido_script = contenido_script.replace('{mascara_subred}', mascara_subred)
            contenido_script = contenido_script.replace('{puerta_enlace}', puerta_enlace)
            contenido_script = contenido_script.replace('{dns_primario}', dns_primario)
            contenido_script = contenido_script.replace('{dns_secundario}', dns_secundario)
            contenido_script = contenido_script.replace('{tipo_conexion}', tipo_conexion)
            contenido_script = contenido_script.replace('{estado}', estado)

            all_scripts.append(contenido_script)

        # Concatenar todos los scripts en uno solo
        script_completo = "\n".join(all_scripts)

        # Función para devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(script_completo, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="interfaces.sh"'
        return respuesta

    else:
        return render(request, 'redes/interfaces.html', {'num_interfaces': 1})

def dhcp(request):
    if request.method == 'POST':
        num_clientes = request.POST.get('num_clientes')

        # Validación de campos
        if not num_clientes or not num_clientes.isdigit():
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'Número de clientes inválido.'})

        num_clientes = int(num_clientes)
        all_scripts = []

        # Recoge los datos del formulario
        for i in range(1, num_clientes + 1):
            nombre_cliente = request.POST.get(f'nombre_cliente_{i}')
            direccion_ip = request.POST.get(f'direccion_ip_{i}')
            mac_address = request.POST.get(f'mac_address_{i}')
            interfaz = request.POST.get(f'interfaz_{i}')
            direccion_servidor = request.POST.get(f'direccion_servidor_{i}')

            # Validacion de campos
            if not nombre_cliente:
                return render(request, 'redes/dhcp.html', {'mensaje_error': 'El nombre del cliente DHCP es obligatorio.'})
            if not direccion_servidor:
                return render(request, 'redes/dhcp.html', {'mensaje_error': 'La dirección del servidor DHCP es obligatoria.'})

            try:
                validador_ipv4(direccion_ip)
            except ValidationError:
                return render(request, 'redes/dhcp.html', {'mensaje_error': 'Introduce una dirección IPv4 válida para su dirección'})

            try:
                validador_mac(mac_address)
            except ValidationError:
                return render(request, 'redes/dhcp.html', {'mensaje_error': 'Introduce una dirección MAC válida. Ej: ee:aa:bb:cc:dd:ee'})

            try:
                validador_ipv4(direccion_servidor)
            except ValidationError:
                return render(request, 'redes/dhcp.html', {'mensaje_error': 'Introduce una dirección IPv4 válida para el servidor DHCP.'})

            # Ruta al script de Bash existente
            ruta_script = 'redes/bash/dhcp_client.sh'

            # Leer el contenido del script de Bash
            with open(ruta_script, 'r') as archivo_script:
                contenido_script = archivo_script.read()

            # Configuración del cliente DHCP
            contenido_script = contenido_script.replace('{nombre_cliente}', nombre_cliente)
            contenido_script = contenido_script.replace('{direccion_ip}', direccion_ip)
            contenido_script = contenido_script.replace('{mac_address}', mac_address)
            contenido_script = contenido_script.replace('{interfaz}', interfaz)
            contenido_script = contenido_script.replace('{direccion_servidor}', direccion_servidor)

            all_scripts.append(contenido_script)

        # Concatenar todos los scripts en uno solo
        script_completo = "\n".join(all_scripts)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(script_completo, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="dhcp_client.sh"'
        return respuesta

    else:
        return render(request, 'redes/dhcp.html', {'num_clientes': 1})

def reserva_ip(request):
    if request.method == 'POST':
        # Recoge los datos del formulario de reserva de IP
        nombre_cliente_reserva = request.POST.get('nombre_cliente_reserva')
        direccion_ip_reserva = request.POST.get('direccion_ip_reserva')
        mac_address_reserva = request.POST.get('mac_address_reserva')
        direccion_servidor_reserva = request.POST.get('direccion_servidor_reserva')
        nombre_usuario_reserva = request.POST.get('nombre_usuario')
        carpeta_destino_reserva = request.POST.get('carpeta_destino')

        # Validación de campos
        if not nombre_cliente_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'El nombre del cliente es obligatorio.'})
        if not direccion_ip_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'La dirección IP es obligatoria.'})
        if not mac_address_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'La dirección MAC es obligatoria.'})
        if not direccion_servidor_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'La dirección del servidor es obligatoria.'})
        if not nombre_usuario_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'El nombre de usuario es obligatorio.'})
        if not carpeta_destino_reserva:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'La carpeta de destino es obligatoria.'})

        try:
            validador_ipv4(direccion_ip_reserva)
            validador_mac(mac_address_reserva)
            validador_ipv4(direccion_servidor_reserva)
        except ValidationError:
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'Alguno de los campos contiene un valor no válido.'})

        # Validación de carpeta de destino
        if not os.path.exists(carpeta_destino_reserva):
            return render(request, 'redes/dhcp.html', {'mensaje_error': 'La carpeta de destino no existe.'})

        # Ruta al script de Bash para la reserva de IP
        ruta_script = 'redes/bash/reserva_ip.sh'

        # Leer el contenido del script de reserva de IP
        with open(ruta_script, 'r') as archivo_script:
            contenido_script = archivo_script.read()

        # Configuración para la reserva de IP
        contenido_script = contenido_script.replace('{nombre_cliente}', nombre_cliente_reserva)
        contenido_script = contenido_script.replace('{direccion_ip}', direccion_ip_reserva)
        contenido_script = contenido_script.replace('{mac_address}', mac_address_reserva)
        contenido_script = contenido_script.replace('{direccion_servidor}', direccion_servidor_reserva)
        contenido_script = contenido_script.replace('{nombre_usuario}', nombre_usuario_reserva)
        contenido_script = contenido_script.replace('{carpeta_destino}', carpeta_destino_reserva)

        # Devolver el script de reserva de IP con las configuraciones aplicadas como una descarga de archivo
        respuesta = HttpResponse(contenido_script, content_type='application/x-shellscript')
        respuesta['Content-Disposition'] = 'attachment; filename="reserva_ip.sh"'
        return respuesta
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
