#!/bin/bash
# Script para la eliminación de usuarios
# Recoger parámetros del formulario
nombre_usuario="{nombre_usuario}"
realizar_backup="{realizar_backup}"

# Mostrar los datos si existen
echo "Nombre de usuario: $nombre_usuario"
echo "Realizar copia de seguridad: $realizar_backup"

# Preguntar al usuario si desea confirmar la operación
read -p "¿Desea eliminar el usuario? (S/N): " confirmacion

# Si la confirmación es "S", montar el comando con los datos introducidos
if [ "$confirmacion" = "S" ]
then
    # Montaje de comando
    comando_userdel="userdel"

    # Realizar copia de seguridad si se especificó
    if [ "$realizar_backup" = "S" ]; then
        # Comando para realizar copia de seguridad de los archivos del usuario
        comando_backup="tar -czf /home/gabriel/borrados/${nombre_usuario}_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/$nombre_usuario"
        echo "Realizando copia de seguridad de los archivos del usuario..."
        $comando_backup
    fi

    # Eliminar usuario
    $comando_userdel $nombre_usuario

    echo "Usuario $nombre_usuario eliminado correctamente."
else
    echo "Operación cancelada."
fi
