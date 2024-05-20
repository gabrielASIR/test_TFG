#!/bin/bash
# Recogemos los parámetros
nombre_backup="{nombre_backup}"
ruta_origen="{ruta_origen}"
ruta_destino="{ruta_destino}"
metodo_copia="{metodo_copia}"
clave_encriptacion="{clave_encriptacion}"
compresion="{compresion}"
exclusiones="{exclusiones}"

# Mostramos valores por pantalla
echo "Nombre del backup: $nombre_backup"
echo "Ruta de origen: $ruta_origen"
echo "Ruta de destino: $ruta_destino"
echo "Método de copia: $metodo_copia"
echo "Clave de encriptación: $clave_encriptacion"
echo "Compresión: $compresion"
echo "Exclusiones: $exclusiones"

# Confirmamos antes de proceder
read -p "¿Desea proceder con la copia de seguridad usando los valores anteriores? (s/n): " confirmacion
if [ "$confirmacion" != "s" ]
then
    echo "Operación cancelada"
fi

# Realizamos la copia de seguridad según el método seleccionado
read -p "¿Desea proceder con la copia usando el método $metodo_copia? (s/n): " confirmacion
if [ "$confirmacion" != "s" ]
then
    echo "Operación cancelada"
fi

case "$metodo_copia" in
    cp)
        cp -r "$ruta_origen" "$ruta_destino"
        ;;
    rsync)
        rsync -av --exclude="$exclusiones" "$ruta_origen" "$ruta_destino"
        ;;
    tar)
        tar -czf "$ruta_destino/$nombre_backup.tar.gz" "$ruta_origen"
        ;;
    *)
        echo "Método de copia no válido"
        exit 1
        ;;
esac

# Encriptar si se especifica clave de encriptación
if [ -n "$clave_encriptacion" ]
then
    read -p "¿Desea encriptar el archivo de backup? (s/n): " confirmacion
    if [ "$confirmacion" = "s" ]
    then
        gpg --output "$ruta_destino/$nombre_backup.tar.gz.gpg" --encrypt --recipient "$clave_encriptacion" "$ruta_destino/$nombre_backup.tar.gz"
        rm "$ruta_destino/$nombre_backup.tar.gz"
    else
        echo "Encriptación omitida"
    fi
fi

# Comprimir si se especifica compresión
if [ "$compresion" != "none" ]; then
    read -p "¿Desea comprimir el archivo de backup usando $compresion? (s/n): " confirmacion
    if [ "$confirmacion" = "s" ]
    then
        case "$compresion" in
            gzip)
                gzip "$ruta_destino/$nombre_backup.tar.gz"
                ;;
            bzip2)
                bzip2 "$ruta_destino/$nombre_backup.tar.gz"
                ;;
        esac
    else
        echo "Compresión omitida"
    fi
fi

echo "Copia de seguridad \"$nombre_backup\" realizada correctamente."
