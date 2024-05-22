#!/bin/bash
# Script para realizar pruebas de conexión ping y registrar un histórico
# Recogida de variables
direccion_ip="{direccion_ip}"
num_intentos="{num_intentos}"
fecha=$(date +"%Y-%m-%d %H:%M:%S")
historico="{historico}"

# Mostrar los datos por pantalla
echo "Dirección IP: $direccion_ip"
echo "Número de intentos: $num_intentos"
echo "Directorio de historial: $historico"
echo ""

# Pedir confirmación antes de continuar
read -p "¿Desea continuar con la prueba de ping? (s/n): " confirmacion
if [ "$confirmacion" != "s" ]
then
    echo "Prueba de ping cancelada."
else
	# Archivo de historial
	historial="$historico/historial_ping.txt"

	# Realizar la prueba de conexión ping y capturar el resultado
	ping_output=$(ping -c "$num_intentos" "$direccion_ip")

	# Extraer el número de pings correctos e incorrectos del resultado
	pings_correctos=$(echo "$ping_output" | grep -oP '\d+ received' | cut -d' ' -f1)
	pings_perdidos=$((num_intentos - pings_correctos))

	# Guardar los detalles de la prueba en el archivo de historial
	echo "Fecha: $fecha" >> "$historial"
	echo "Dirección de salida: $(hostname -I)" >> "$historial"
	echo "Dirección de entrada: $direccion_ip" >> "$historial"
	echo "Pings correctos: $pings_correctos" >> "$historial"
	echo "Pings perdidos: $pings_perdidos" >> "$historial"
	echo "" >> "$historial"

	# Imprimir el resultado de la prueba al usuario
	echo "Resultado de la prueba de ping:"
	echo "$ping_output"
fi
