#!/bin/bash
nombre_cliente="{nombre_cliente}"
direccion_ip="{direccion_ip}"
mac_address="{mac_address}"
interfaz="{interfaz}"
direccion_servidor="{direccion_servidor}"

echo "Configuración interfaz: DHCP"
echo "Nombre del cliente: $nombre_cliente"
echo "Dirección IP deseada: $direccion_ip"
echo "Dirección MAC: $mac_address"
echo "Interfaz: $interfaz"
echo "Dirección del servidor DHCP: $direccion_servidor"

read -p "¿Desea aplicar las configuraciones? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]
then
    # Cambiar la configuración de Netplan para DHCP
    cat <<EOF > /etc/netplan/00-installer-config.yaml
network:
  ethernets:
    $interfaz:
      dhcp4: true
  version: 2
EOF

    # Aplicar la nueva configuración de Netplan
    netplan apply

    # Solicitar una dirección IP al servidor DHCP con dhclient
    dhclient -v -r $interfaz && dhclient -v $interfaz -s $direccion_servidor

    echo "Configuración DHCP aplicada correctamente."
else
    echo "La configuración no se ha podido aplicar correctamente."
fi
