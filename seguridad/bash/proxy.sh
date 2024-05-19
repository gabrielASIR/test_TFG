#!/bin/bash
# Configuración de las reglas de Squid
# Recoger parámetro
ruta_configuracion="{ruta_configuracion}"

# Comprobar si la ruta está creada. Si no lo está, la creamos.
if [ ! -d "$ruta_configuracion" ]; then
    mkdir -p "/etc/squid/conf.d/$ruta_configuracion"
fi

# Iterar sobre cada ACL y su acción permitir/denegar
for ((i=0; i<${#acl_list[@]}; i++)); do
    acl="${acl_list[i]}"
    tipo_acl="${tipo_acl_list[i]}"
    direccion_ip="${direccion_ip_list[i]}"
    mascara_subred="${mascara_subred_list[i]}"
    detalle_acl="${detalle_acl_list[i]}"
    permitir_denegar="${permitir_denegar_list[i]}"
    
    # Configurar la ACL en Squid
    if [ -n "$acl" ]; then
        echo "acl $acl $tipo_acl $direccion_ip/$mascara_subred" >> "/etc/squid/conf.d/$ruta_configuracion"
    fi

    # Configurar la acción permitir/denegar en Squid
    if [ -n "$permitir_denegar" ]; then
        echo "http_access $permitir_denegar $acl" >> "/etc/squid/conf.d/$ruta_configuracion"
    fi
done
