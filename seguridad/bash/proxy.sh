#!/bin/bash
# Configuración de las reglas de Squid
# Recoger parámetro
ruta_configuracion="{ruta_configuracion}"

# Comprobar si la ruta está creada. Si no lo está, la creamos.
if [ ! -d "$ruta_configuracion" ]
then
    mkdir -p "/etc/squid/conf.d/$ruta_configuracion"
fi

# Iterar sobre cada regla y configurar Squid
for ((i=1; i<=$num_reglas; i++))
do
    tipo_regla="${tipo_regla_$i}"
    acl="${acl_$i}"
    tipo_acl="${tipo_acl_$i}"
    http_access="${http_access_$i}"
    accion_http_access="${accion_http_access_$i}"

    # Verificar si algún dato está vacío
    if [ -z "$tipo_regla" ] || [ -z "$acl" ] || [ -z "$tipo_acl" ] || [ -z "$http_access" ] || [ -z "$accion_http_access" ]
    then
        echo "Alguno de los campos de la regla $i está vacío. Por favor, completa todos los campos."
        exit 1
    fi

    # Mostrar los datos de la regla
    echo "Configurando regla $i:"
    echo "Tipo de Regla: $tipo_regla"
    echo "ACL: $acl"
    echo "Tipo de ACL: $tipo_acl"
    echo "HTTP Access: $http_access"
    echo "Acción HTTP Access: $accion_http_access"

    # Solicitar confirmación para continuar
    read -p "¿Deseas continuar con la configuración de esta regla? (S/n): " confirmacion
    if [ "$confirmacion" != "S" ]
    then
        echo "Abortando configuración."
        exit 1
    fi

    # Configurar la regla según su tipo
    if [ "$tipo_regla" = "acl" ]
    then
        echo "acl $acl $tipo_acl" >> "/etc/squid/conf.d/$ruta_configuracion/squid-custom.conf"
    elif [ "$tipo_regla" = "http_access" ]
    then
        echo "http_access $http_access $accion_http_access $acl" >> "/etc/squid/conf.d/$ruta_configuracion/squid-custom.conf"
    fi
done

echo "Configuración completada."
