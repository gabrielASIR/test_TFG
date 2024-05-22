#!/bin/bash
# Recoge los argumentos pasados desde Django
red_origen="{red_origen}"
red_destino="{red_destino}"
mascara="{mascara}"
gateway="{gateway}"

echo "Red Origen: $red_origen"
echo "Red destino: $red_destino"
echo "Mascara de red: $mascara"
echo "Gateway: $gateway"

read -p "Desea añadir estas nuevas rutas? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]
then
	# Aplicar configuraciones de enrutamiento
	ip route add $red_destino/$mascara via $gateway

	echo "Configuracion aplicada correctamente"
else
	echo "Su configuracion ha sido cancelada"
fi
