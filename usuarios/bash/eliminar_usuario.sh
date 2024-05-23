#!/bin/bash
# Script para la eliminación completa de usuarios
# Recoger parámetros del formulario
nombre_usuario="{nombre_usuario}"
realizar_copia="{realizar_copia}"
directorio_copia="{directorio_copia}"
eliminar_correo="{eliminar_correo}"
eliminar_crontab="{eliminar_crontab}"
forzar_eliminacion="{forzar_eliminacion}"
eliminar_grupos="{eliminar_grupos}"
eliminar_home="{eliminar_home}"

# Mostrar los datos si existen
echo "Nombre de usuario: $nombre_usuario"
[ -n "$realizar_copia" ] && echo "Realizar copia de seguridad: $realizar_copia"
[ -n "$directorio_copia" ] && echo "Directorio de copia de seguridad: $directorio_copia"
[ -n "$eliminar_correo" ] && echo "Eliminar correo: $eliminar_correo"
[ -n "$eliminar_crontab" ] && echo "Eliminar crontab: $eliminar_crontab"
[ -n "$forzar_eliminacion" ] && echo "Forzar eliminación: $forzar_eliminacion"
[ -n "$eliminar_grupos" ] && echo "Eliminar de todos los grupos secundarios: $eliminar_grupos"
[ -n "$eliminar_home" ] && echo "Eliminar directorio de inicio y correo del sistema: $eliminar_home"

# Preguntar al usuario si desea confirmar la operación
read -p "¿Desea eliminar el usuario y todos sus archivos? (S/N): " confirmacion

# Si la confirmación es "S", montar el comando con los datos introducidos
if [ "$confirmacion" = "S" ]
then
    # Montaje de comando
    comando_userdel="userdel"

    # Realizar copia de seguridad si se especificó
    if [ "$realizar_copia" = "S" ]
    then
        comando_backup="tar -czf ${directorio_copia}/${nombre_usuario}_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/$nombre_usuario"
        echo "Realizando copia de seguridad de los archivos del usuario..."
        $comando_backup
    fi

    # Añadir opciones adicionales para eliminar completamente al usuario
    [ "$eliminar_correo" = "S" ] && comando_userdel+=" --remove-mail"
    [ "$eliminar_crontab" = "S" ] && comando_userdel+=" --remove-all-files"
    [ "$forzar_eliminacion" = "S" ] && comando_userdel+=" --force"
    [ "$eliminar_grupos" = "S" ] && comando_userdel+=" --remove-groups"
    [ "$eliminar_home" = "S" ] && comando_userdel+=" --remove-home"

    # Añadir el nombre de usuario al comando
    comando_userdel+=" $nombre_usuario"

    # Ejecutar el comando userdel
    $comando_userdel

    echo "Usuario $nombre_usuario y todos sus archivos eliminados correctamente."
else
    echo "Operación cancelada."
fi
