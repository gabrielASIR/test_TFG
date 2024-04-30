#!/bin/bash
# Recoge los argumentos pasados desde Django
nom="{nombre}"
dir_ip="{direccion_ip}"
mas_sub="{mascara_subred}"
pu_en="{puerta_enlace}"
dns_p="{dns_primario}"
dns_s="{dns_secundario}"
est="{estado}"

echo "Nombre: $nom"
echo "Direccion IP: $dir_ip"
echo "Mascara: $mas_sub"
echo "Puerta enlace: $pu_en"
echo "DNS Primario: $dns_p"
echo "DNS Secundario: $dns_s"
echo "Estado: $est"

# Pregunta al usuario si desea aplicar las configuraciones
read -p "¿Desea aplicar las configuraciones? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]; then
    # Configuración de la interfaz de red
echo "network:
  ethernets:
    $nom:
      addresses: [$dir_ip/$mas_sub]
      routes:
        - to: default
          via: $pu_en
      nameservers:
        addresses: [$dns_p, $dns_s]
  version: 2
" > /etc/netplan/00-installer-config.yaml

    # Aplicar la configuración de Netplan
    netplan apply

    # Verifica el estado y activa o desactiva la interfaz según corresponda
    if [ "$est" = "A" ]; then
        ip link set $nom up
    elif [ "$est" = "I" ]; then
        ip link set $nom down
    else
        echo "Estado desconocido. No se realizó ninguna acción."
    fi

    echo "Configuraciones aplicadas correctamente."
else
    echo "Las configuraciones no fueron aplicadas."
fi
