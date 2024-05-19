#!/bin/bash
# Recoge los argumentos pasados desde Django
nombre_nas="{nombre_nas}"
ruta_montaje="{ruta_montaje}"
archivos="{archivos}"
usuario_nas="{usuario_nas}"
contrasena_nas="{contrasena_nas}"
sobrescribir="{sobrescribir}"
compresion="{compresion}"

# Verifica si se deben sobrescribir archivos existentes
opciones=""
if [ "$sobrescribir" = "True" ]; then
    opciones="--sobrescribir"
fi

# Verifica si se debe aplicar compresión
if [ "$compresion" != "none" ]; then
    opciones="$opciones --compresion=$compresion"
fi

# Nos movemos al directorio de montaje del NAS
cd "$ruta_montaje"

# Recorre todas las rutas de archivos especificadas y las copia al NAS
archivos="{archivos}"
for archivo in $archivos; do
    # Copia el archivo al NAS
    cp $opciones "$archivo" .

    # Verifica si la copia fue exitosa
    if [ $? -eq 0 ]; then
        echo "Archivo $archivo copiado correctamente al NAS"
    else
        echo "Error al copiar el archivo $archivo al NAS"
    fi
done

# Mostramos todo que se encuentra ahora en el NAS
ls -l "$ruta_montaje"

# Desmonta el NAS
umount "$ruta_montaje"

# Verifica si se desmontó correctamente
if [ $? -eq 0 ]; then
    echo "NAS desmontado correctamente"
else
    echo "Error al desmontar el NAS. Por favor, cierre cualquier archivo abierto y vuelva a intentarlo."
fi
