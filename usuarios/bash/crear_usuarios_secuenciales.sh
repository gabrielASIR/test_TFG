#!/bin/bash
# Recoger parámetros del formulario
prefijo="{prefijo}"
inicio={inicio}
fin={fin}

echo "Los usuarios empezarán por $prefijo$inicio y acabarán en $prefijo$fin"

read -p "Esta seguro de crear todos estos usuarios: (s/n)" confirmacion
if [ "confirmacion" != "s" ]
then
    echo "Operacion cancelada"
else
    # Crear usuarios secuenciales
    for (i=$inicio; i<=$fin; i++)
    do
        nombre_usuario="$prefijo$i"
        useradd "$nombre_usuario"
        echo "Usuario $nombre_usuario creado"
    done
fi
echo "Usuarios creados con exito"
