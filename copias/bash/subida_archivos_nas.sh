#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_nas="{nombre_nas}"
ruta_montaje="{ruta_montaje}"
archivos="{archivos}"
usuario_nas="{usuario_nas}"
contrasena_nas="{contrasena_nas}"
sobrescribir="{sobrescribir}"
compresion="{compresion}"

# Mostramos los datos ingresados por el usuario
echo "Nombre del NAS: $nombre_nas"
echo "Ruta de montaje: $ruta_montaje"
echo "Archivos a subir:"
for ruta in $archivos
do
    echo " - $ruta"
done
echo "Usuario del NAS: $usuario_nas"

# Solicitamos confirmación para proceder
read -p "¿Desea proceder con la subida de archivos al NAS? (s/n): " confirmacion

if [ "$confirmacion" != "s" ]
then
    echo "Operación cancelada."
fi

# Verificamos que todos los campos estén completos
if [ -z "$nombre_nas" ] || [ -z "$ruta_montaje" ]
then
    echo "Por favor, complete todos los campos del formulario."
fi

# Verificamos si algún campo está vacío
if [ -z "$archivos" ]
then
    echo "Por favor, especifique al menos una ruta de archivo."
fi

# Verificamos si se proporcionó el usuario y la contraseña del NAS
if [ -z "$usuario_nas" ] || [ -z "$contrasena_nas" ]
then
    echo "Por favor, especifique el usuario y la contraseña del NAS."
fi

# Verificamos si las rutas de archivos existen
archivos=($archivos)
for ruta in "${archivos[@]}"
do
    if [ ! -f "$ruta" ]
    then
        echo "La ruta de archivo \"$ruta\" no existe."
    fi
done

# Construimos la cadena de opciones para subir
opciones=""
if [ "$sobrescribir" = "True" ]
then
    opciones+="--update "
fi

if [ "$compresion" != "none" ]
then
    opciones+="--compress --"$compresion" "
fi

# Realiza la transferencia de archivos con rsync
rsync -av $opciones "${archivos[@]}" "$usuario_nas@$ruta_montaje"

# Verifica si la transferencia fue exitosa
if [ $? -eq 0 ]
then
    echo "Archivos copiados correctamente al NAS."
else
    echo "Error al copiar archivos al NAS."
fi
