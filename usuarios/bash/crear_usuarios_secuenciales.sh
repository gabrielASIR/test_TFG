#!/bin/bash
# Script para la creación de usuarios secuenciales
# Recoger parámetros del formulario
prefijo="{prefijo}"
inicio="{inicio}"
fin="{fin}"

# Crear usuarios secuenciales
for ((i=$inicio; i<=$fin; i++)); do
    nombre_usuario="$prefijo$i"
    useradd "$nombre_usuario"
    echo "Usuario $nombre_usuario creado"
done

echo "Usuarios creados con exito"
