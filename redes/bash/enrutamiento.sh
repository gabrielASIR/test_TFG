#!/bin/bash
# Recoge los argumentos pasados desde Django
red_origen="{red_origen}"
configuraciones="{configuraciones}"

echo "Red Origen: $red_origen"
echo "Configuraciones de enrutamiento:"
echo "$configuraciones"

read -p "Desea añadir estas nuevas rutas? (S/N): " confirmacion

if [ "$confirmacion" = "S" ]; then
	# Aplicar configuraciones de enrutamiento
	$configuraciones

	echo "Una vez aplicadas, sus rutas son las siguientes:"
	echo ""
	ip route
else
	echo "Su configuracion ha sido cancelada"
fi
