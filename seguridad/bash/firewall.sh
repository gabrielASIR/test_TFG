#!/bin/bash
# Establecer la política por defecto
politica_por_defecto="{politica_por_defecto}"
echo "Política por defecto: $politica_por_defecto"

read -p "¿Aplicar esta política por defecto? (s/n): " confirmacion_politica
if [ "$confirmacion_politica" = "s" ]; then
    echo "Aplicando política por defecto..."
    # Montar el comando para establecer la política por defecto
    if [ "$politica_por_defecto" = "ACCEPT" ]; then
        iptables -P INPUT ACCEPT
        iptables -P FORWARD ACCEPT
        iptables -P OUTPUT ACCEPT
    elif [ "$politica_por_defecto" = "DROP" ]; then
        iptables -P INPUT DROP
        iptables -P FORWARD DROP
        iptables -P OUTPUT DROP
    else
        echo "Error: Política por defecto no válida."
    fi
else
    echo "Política por defecto no aplicada."
fi

borrar_configuraciones="{borrar_configuraciones}"
# Borrar configuraciones existentes si se especifica
if [ "$borrar_configuraciones" = "on" ]; then
    read -p "¿Desea borrar las configuraciones existentes? (y/n): " confirmacion_borrar
    if [ "$confirmacion_borrar" = "y" ]; then
        echo "Borrando configuraciones existentes..."
        iptables -F
        iptables -X
    else
        echo "No se borraron configuraciones existentes."
    fi
fi

# Insertar las reglas generadas aquí
{rules_content}
