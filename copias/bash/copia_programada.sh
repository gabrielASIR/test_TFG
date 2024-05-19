#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_copia="{nombre_copia}"
dias_semana="{dias_semana}"
hora_ejecucion="{hora_ejecucion}"
frecuencia="{frecuencia}"
numero_ejecuciones="{numero_ejecuciones}"

# Verificamos si algún campo está vacío y lo añadimos a los parámetros según corresponda
comando_programacion=""
if [ -n "$nombre_copia" ]; then
    comando_programacion="$comando_programacion --nombre-copia=\"$nombre_copia\""
fi
if [ -n "$dias_semana" ]; then
    comando_programacion="$comando_programacion --dias-semana=\"$dias_semana\""
fi
if [ -n "$hora_ejecucion" ]; then
    comando_programacion="$comando_programacion --hora-ejecucion=\"$hora_ejecucion\""
fi
if [ -n "$frecuencia" ]; then
    comando_programacion="$comando_programacion --frecuencia=\"$frecuencia\""
fi
if [ -n "$numero_ejecuciones" ]; then
    comando_programacion="$comando_programacion --numero-ejecuciones=\"$numero_ejecuciones\""
fi

# Añadir la programación de la copia al cron
echo "$hora_ejecucion * * $dias_semana $comando_programacion" >> /etc/crontab

echo "Programación de copia \"$nombre_copia\" realizada correctamente."
