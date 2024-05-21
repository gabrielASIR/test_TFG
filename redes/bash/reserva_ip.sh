#!/bin/bash
# Recoge los argumentos pasados desde Django
nombre_cliente="{nombre_cliente}"
direccion_ip="{direccion_ip}"
mac_address="{mac_address}"
direccion_servidor="{direccion_servidor}"
nombre_usuario="{nombre_usuario}"
carpeta_destino="{carpeta_destino}"

echo "Nombre del cliente: $nombre_cliente"
echo "Dirección IP a reservar: $direccion_ip"
echo "Dirección MAC: $mac_address"
echo "Dirección del servidor DHCP: $direccion_servidor"

# Pregunta al usuario si desea aplicar las configuraciones
read -p "¿Desea aplicar las configuraciones? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]
then
	# Generar el script de reserva de IP
echo "#!/bin/bash" > "reserva_{nombre_cliente}.sh"
echo "echo 'host $nombre_cliente {
  hardware ethernet $mac_address;
  fixed-address $direccion_ip;
}' >> /etc/dhcp/dhcpd.conf
	systemctl restart isc-dhcp-server" >> "reserva_{nombre_cliente}.sh"

	# Enviar el script de reserva de IP al servidor DHCP
	scp reserva_{nombre_cliente}.sh $nombre_usuario@$direccion_servidor:$carpeta_destino

	echo "Script de reserva de dirección IP generado y enviado al servidor DHCP."
else
	echo "ERROR. El script no se ha enviado bien."
fi
