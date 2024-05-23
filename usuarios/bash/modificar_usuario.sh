#!/bin/bash
# Script para la modificación de usuarios

# Recoger parámetros del formulario
nombre_usuario="{nombre_usuario}"
contrasena="{contrasena}"
grupo_principal="{grupo_principal}"
otros_grupos="{otros_grupos}"
nombre_completo="{nombre_completo}"
skel="{skel}"
directorio_home="{directorio_home}"
shell="{shell}"
expire="{expire}"
uid="{uid}"
gid="{gid}"
inactive="{inactive}"
crear_home="{crear_home}"
copiar_skel="{copiar_skel}"

# Generamos la contraseña formateada
contrasena_formateada=$(mkpasswd -m sha-512 "$contrasena")

# Mostramos los datos comprobando si existen
echo "Nombre de usuario: $nombre_usuario"
[ -n "$contrasena" ] && echo "Contraseña: $contrasena_formateada"
echo "Grupo principal: $grupo_principal"
[ -n "$otros_grupos" ] && echo "Otros grupos: $otros_grupos"
echo "Nombre completo: $nombre_completo"
[ -n "$skel" ] && echo "Directorio skel: $skel"
[ -n "$directorio_home" ] && echo "Directorio home: $directorio_home"
echo "Shell: $shell"
[ -n "$expire" ] && echo "Fecha de expiración: $expire"
[ -n "$uid" ] && echo "UID: $uid"
[ -n "$gid" ] && echo "GID: $gid"
[ -n "$inactive" ] && echo "Días de inactividad: $inactive"
[ -n "$crear_home" ] && echo "Crear directorio home: $crear_home"
[ -n "$copiar_skel" ] && echo "Copiar archivos de skel: $copiar_skel"

# Preguntamos al usuario final si desea confirmar la operación
read -p "¿Desea modificar el usuario? (S/N): " confirmacion

# Si la confirmación es "S", montamos el comando con los datos introducidos
if [ "$confirmacion" = "S" ]
then
    # Montaje de comando
    comando_usermod="usermod"
    [ -n "$contrasena" ] && comando_usermod+=" -p $contrasena_formateada"
    [ -n "$grupo_principal" ] && comando_usermod+=" -g $grupo_principal"
    [ -n "$otros_grupos" ] && comando_usermod+=" -G $otros_grupos"
    [ -n "$nombre_completo" ] && comando_usermod+=" -c '$nombre_completo'"
    [ -n "$skel" ] && comando_usermod+=" -k $skel"
    [ -n "$directorio_home" ] && comando_usermod+=" -d $directorio_home"
    [ -n "$shell" ] && comando_usermod+=" -s $shell"
    [ -n "$expire" ] && comando_usermod+=" -e $expire"
    [ -n "$uid" ] && comando_usermod+=" -u $uid"
    [ -n "$gid" ] && comando_usermod+=" -g $gid"
    [ -n "$inactive" ] && comando_usermod+=" -f $inactive"
    comando_usermod+=" $nombre_usuario"
    
    # Ejecución del comando completo
    $comando_usermod

    echo "Usuario $nombre_usuario modificado correctamente."
else
    echo "Operación cancelada."
fi
