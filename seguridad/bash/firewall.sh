#!/bin/bash
# Establecer la política por defecto
politica_por_defecto="{politica_por_defecto}"
echo "Política por defecto: $politica_por_defecto"

read -p "¿Aplicar esta política por defecto? (s/n): " confirmacion_politica
if [ "$confirmacion_politica" = "s" ]
then
    echo "Aplicando política por defecto..."
    # Montar el comando para establecer la política por defecto
    if [ "$politica_por_defecto" = "ACCEPT" ]
    then
        iptables -P INPUT ACCEPT
        iptables -P FORWARD ACCEPT
        iptables -P OUTPUT ACCEPT
    elif [ "$politica_por_defecto" = "DROP" ]
    then
        iptables -P INPUT DROP
        iptables -P FORWARD DROP
        iptables -P OUTPUT DROP
    else
        echo "Error: Política por defecto no válida."
    fi
else
    echo "Política por defecto no aplicada."
fi

# Borrar configuraciones existentes si se especifica
borrar_configuraciones="{borrar_configuraciones}"
if [ "$borrar_configuraciones" = "on" ]
then
    read -p "¿Desea borrar las configuraciones existentes? (s/n): " confirmacion_borrar
    if [ "$confirmacion_borrar" = "s" ]
    then
        echo "Borrando configuraciones existentes..."
        iptables -F
        iptables -X
    else
        echo "No se borraron configuraciones existentes."
    fi
fi

# Recogemos los datos de las reglas
tabla = {tabla}
opcion = {opcion}
cadena = {cadena}
direccion_origen = {direccion_origen}
puerto_origen = {puerto_origen}
direccion_destino = {direccion_destino}
puerto_destino = {puerto_destino}
protocolo = {protocolo}
accion = {accion}

echo "Tabla: $tabla"
echo "Opcion: $opcion"
echo "Cadena: $cadena"
[ -n "$direccion_origen" ] && echo "Direccion de origen: $direccion_origen"
[ -n "$puerto_origen" ] && echo "Puerto de origen: $puerto_origen"
[ -n "$direccion_destino" ] && echo "Dirección de destino: $direccion_destino"
[ -n "$puerto_destino" ] && echo "Puerto de destino: $puerto_destino"
[ -n "$protocolo" ] && echo "Protocolo: $protocolo"
echo "Accion: $accion"

read -p "¿Desea aplicar esta nueva regla? (s/n): " confirmacion_regla
if [ "$confirmacion_borrar" = "s" ]
    # Montar el comando de iptables y ejecutarlo
    comando_iptables="iptables -t $tabla $opcion $cadena"

    if [ -n "$direccion_origen" ]
    then
        comando_iptables+=" -s $direccion_origen"
    fi
    if [ -n "$puerto_origen" ]
    then
        comando_iptables+=" --sport $puerto_origen"
    fi
    if [ -n "$direccion_destino" ]
    then
        comando_iptables+=" -d $direccion_destino"
    fi
    if [ -n "$puerto_destino" ]
    then
        comando_iptables+=" --dport $puerto_destino"
    fi
    if [ -n "$protocolo" ] && [ "$protocolo" != "all" ]
    then
        comando_iptables+=" -p $protocolo"
    fi
    comando_iptables+=" -j $accion"

    # Ejecutar el comando de iptables
    $comando_iptables

    echo "Configuraciones aplicadas correctamente"
else
    echo "Error: algunos campos necesarios están vacíos. La regla no se aplicará."
fi
