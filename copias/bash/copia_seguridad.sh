#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_backup="{nombre_backup}"
ruta_origen="{ruta_origen}"
ruta_destino="{ruta_destino}"
metodo_copia="{metodo_copia}"
clave_encriptacion="{clave_encriptacion}"
compresion="{compresion}"
exclusiones="{exclusiones}"

# Verificamos si algún campo está vacío y lo añadimos a los parámetros según corresponda
comando_copia=""
if [ -n "$nombre_backup" ]; then
    comando_copia="$comando_copia --nombre-backup=\"$nombre_backup\""
fi
if [ -n "$ruta_origen" ]; then
    comando_copia="$comando_copia --ruta-origen=\"$ruta_origen\""
fi
if [ -n "$ruta_destino" ]; then
    comando_copia="$comando_copia --ruta-destino=\"$ruta_destino\""
fi
if [ -n "$metodo_copia" ]; then
    comando_copia="$comando_copia --metodo-copia=\"$metodo_copia\""
fi
if [ -n "$clave_encriptacion" ]; then
    comando_copia="$comando_copia --clave-encriptacion=\"$clave_encriptacion\""
fi
if [ -n "$compresion" ]; then
    comando_copia="$comando_copia --compresion=\"$compresion\""
fi
if [ -n "$exclusiones" ]; then
    comando_copia="$comando_copia --exclusiones=\"$exclusiones\""
fi

# Realizamos la copia de seguridad según el método seleccionado
if [ "$metodo_copia" = "cp" ]; then
    cp -r $comando_copia
elif [ "$metodo_copia" = "rsync" ]; then
    rsync -avz $comando_copia
elif [ "$metodo_copia" = "tar" ]; then
    tar -czf "$ruta_destino/$nombre_backup.tar.gz" $comando_copia
else
    echo "Método de copia no válido"
    exit 1
fi

# Añadimos las configuraciones faltantes
# Si se especifica clave encriptamos el archivo
if [ -n "$clave_encriptacion" ]; then
    gpg --output "$ruta_destino/$nombre_backup.tar.gz.gpg" --encrypt --recipient "$clave_encriptacion" "$ruta_destino/$nombre_backup.tar.gz"
    rm "$ruta_destino/$nombre_backup.tar.gz"
fi

# Si se especifica compresión, podemos comprimir el archivo de copia adicionalmente
if [ "$compresion" = "gzip" ]; then
    gzip "$ruta_destino/$nombre_backup.tar.gz"
elif [ "$compresion" = "bzip2" ]; then
    bzip2 "$ruta_destino/$nombre_backup.tar.gz"
fi

echo "Copia de seguridad \"$nombre_backup\" realizada correctamente."
