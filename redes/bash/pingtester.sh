#!/bin/bash
# Script para realizar pruebas de conexión ping y registrar un histórico
# Recogida de variables
direccion_ip="{direccion_ip}"
num_intentos="{num_intentos}"
fecha=$(date +"%Y-%m-%d %H:%M:%S")
historico="{historico}/historial_ping.txt"

# Realizar la prueba de conexión ping y capturar el resultado
ping_output=$(ping -c "$num_intentos" "$direccion_ip")

# Extraer el número de pings correctos e incorrectos del resultado
pings_correctos=$(echo "$ping_output" | grep -oP '\d+ received' | cut -d' ' -f1)
pings_perdidos=$((num_intentos - pings_correctos))

# Guardar los detalles de la prueba en el archivo de historial
echo "Fecha: $fecha" >> "$historico"
echo "Dirección de salida: $(hostname -I)" >> "$historico"
echo "Dirección de entrada: $direccion_ip" >> "$historico"
echo "Pings correctos: $pings_correctos" >> "$historico"
echo "Pings perdidos: $pings_perdidos" >> "$historico"
echo "" >> "$historico"

# Imprimir el resultado de la prueba al usuario
echo "Resultado de la prueba de ping:"
echo "$ping_output"
