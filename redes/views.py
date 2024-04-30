from django.shortcuts import render
from django.http import HttpResponse

def interfaces(request):
    if request.method == 'POST':
        # Recoge los datos del formulario
        nombre = request.POST.get('nombre')
        direccion_ip = request.POST.get('direccion_ip')
        mascara_subred = request.POST.get('mascara_subred')
        puerta_enlace = request.POST.get('puerta_enlace')
        dns_primario = request.POST.get('dns_primario')
        dns_secundario = request.POST.get('dns_secundario')
        tipo_conexion = request.POST.get('tipo_conexion')
        estado = request.POST.get('estado')

        # Ruta al script de Bash existente
        script_path = 'redes/bash/interfaces.sh'

        # Leer el contenido del script de Bash
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        # Configuración de la interfaz de red
        script_content = script_content.replace('{nombre}', nombre)
        script_content = script_content.replace('{direccion_ip}', direccion_ip)
        script_content = script_content.replace('{mascara_subred}', mascara_subred)
        script_content = script_content.replace('{puerta_enlace}', puerta_enlace)
        script_content = script_content.replace('{dns_primario}', dns_primario)
        script_content = script_content.replace('{dns_secundario}', dns_secundario)
        script_content = script_content.replace('{tipo_conexion}', tipo_conexion)
        script_content = script_content.replace('{estado}', estado)

        # Devolver el script de Bash con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="interfaces.sh"'
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

        # Devolver el script de reserva de IP con las configuraciones aplicadas como una descarga de archivo
        response = HttpResponse(script_content, content_type='application/x-shellscript')
        response['Content-Disposition'] = 'attachment; filename="reserva_ip.sh"'
        return response
    else:
        return render(request, 'redes/dhcp.html')

def dns(request):
    return render(request, 'redes/dns.html')

def enrutamiento(request):
    return render(request, 'redes/enrutamiento.html')
