#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre="{nombre}"
direccion_ip="{direccion_ip}"
mascara_subred="{mascara_subred}"
puerta_enlace="{puerta_enlace}"
dns_primario="{dns_primario}"
dns_secundario="{dns_secundario}"
tipo_conexion="{tipo_conexion}"
estado="{estado}"

echo "Nombre: $nombre"
echo "Dirección IP: $direccion_ip"
echo "Máscara: $mascara_subred"
echo "Puerta de enlace: $puerta_enlace"
echo "DNS Primario: $dns_primario"
echo "DNS Secundario: $dns_secundario"
echo "Tipo de conexión: $tipo_conexion"
echo "Estado: $estado"

# Preguntamos al usuario si desea aplicar las configuraciones
read -p "¿Desea aplicar las configuraciones? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]
then
    # Configuración de la interfaz de red
    cat <<EOF >"/etc/netplan/00-installer-config.yaml"
network:
  ethernets:
    $nombre:
      addresses: [$direccion_ip/$mascara_subred]
      routes:
        - to: default
          via: $puerta_enlace
      nameservers:
        addresses: [$dns_primario, $dns_secundario]
  version: 2
EOF

    # Aplicamos la configuración de Netplan
    netplan apply

    # Verificamos el estado y activa o desactiva la interfaz según corresponda
    if [ "$estado" = "A" ]
    then
        ip link set $nombre up
    elif [ "$estado" = "I" ]
    then
        ip link set $nombre down
    else
        echo "Estado desconocido. No se realizó ninguna acción."
    fi

    echo "Configuraciones aplicadas correctamente."
else
    echo "Las configuraciones no fueron aplicadas."
fi
