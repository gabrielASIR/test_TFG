#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_copia="{nombre_copia}"
dias_semana="{dias_semana}"
hora="{hora}"
minutos="{minutos}"

# Mostramos los datos por pantalla
echo "Ruta de la copia: $nombre_copia"
echo "Días de la semana: $dias_semana"
echo "Hora de ejecución: $hora:$minutos"

# Pedimos confirmación al usuario
read -p "¿Desea programar la copia de seguridad? (s/n): " confirmacion
if [ "$confirmacion" != "s" ]
then
    echo "Programación cancelada."
fi

# Añadimos la programación de la copia al cron
echo "$minutos $hora * * $dias_semana root $nombre_copia" >> /etc/crontab

echo "Programación de copia \"$nombre_copia\" realizada correctamente."
