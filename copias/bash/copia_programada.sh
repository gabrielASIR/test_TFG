#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_copia="{nombre_copia}"
dias_semana="{dias_semana}"
hora_ejecucion="{hora_ejecucion}"
frecuencia="{frecuencia}"
numero_ejecuciones="{numero_ejecuciones}"

# Mostramos los datos por pantalla
echo "Ruta de la copia: $nombre_copia"
echo "Días de la semana: $dias_semana"
echo "Hora de ejecución: $hora_ejecucion"
echo "Frecuencia: $frecuencia"
echo "Número de ejecuciones: $numero_ejecuciones"

# Pedimos confirmación al usuario
read -p "¿Desea programar la copia de seguridad? (s/n): " confirmacion
if [ "$confirmacion" != "s" ]
then
    echo "Programación cancelada."
fi

# Añadimos la programación de la copia al cron
echo "$hora_ejecucion * * $dias_semana $nombre_copia $frecuencia $numero_ejecuciones" >> /etc/crontab

echo "Programación de copia \"$nombre_copia\" realizada correctamente."
