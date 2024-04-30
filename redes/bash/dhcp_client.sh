#!/bin/bash
# Recoge los argumentos pasados desde Django
nombre_cliente="{nombre_cliente}"
direccion_ip="{direccion_ip}"
mac_address="{mac_address}"
interfaz="{interfaz}"
direccion_servidor="{direccion_servidor}"

echo "Nombre del cliente: $nombre_cliente"
echo "Dirección IP deseada: $direccion_ip"
echo "Dirección MAC: $mac_address"
echo "Interfaz: $interfaz"
echo "Dirección del servidor DHCP: $direccion_servidor"

read -p "¿Desea aplicar las configuraciones? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]; then
	# Configuración del cliente DHCP usando dhclient
	dhclient -v -r $interfaz && dhclient -v $interfaz -s $direccion_servidor

	echo "Configuración DHCP aplicada correctamente."
else
	echo "La configuración no se ha podido aplicar bien."
fi
