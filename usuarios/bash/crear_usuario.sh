#!/bin/bash
# Recogida de parámetros
nombre_usuario="{nombre_usuario}"
contrasena="{contrasena}"
grupo_principal="{grupo_principal}"
otros_grupos="{otros_grupos}"
nombre_completo="{nombre_completo}"
directorios="{directorios}"
skel="{skel}"
directorio_home="{directorio_home}"
shell="{shell}"
expire="{expire}"
uid="{uid}"
gid="{gid}"
inactive="{inactive}"
crear_home="{crear_home}"
copiar_skel="{copiar_skel}"

# Mostrar los datos si existen
echo "Nombre de usuario: $nombre_usuario"
[ -n "$contrasena" ] && echo "Contraseña: $contrasena"
echo "Grupo principal: $grupo_principal"
[ -n "$otros_grupos" ] && echo "Otros grupos: $otros_grupos"
echo "Nombre completo: $nombre_completo"
[ -n "$directorios" ] && echo "Directorios a crear: $directorios"
[ -n "$skel" ] && echo "Directorio skel: $skel"
[ -n "$directorio_home" ] && echo "Directorio home: $directorio_home"
echo "Shell: $shell"
[ -n "$expire" ] && echo "Fecha de expiración: $expire"
[ -n "$uid" ] && echo "UID: $uid"
[ -n "$gid" ] && echo "GID: $gid"
[ -n "$inactive" ] && echo "Días de inactividad: $inactive"
[ -n "$crear_home" ] && echo "Crear directorio home: $crear_home"
[ -n "$copiar_skel" ] && echo "Copiar archivos de skel: $copiar_skel"

# Preguntar al usuario si desea confirmar la operación
read -p "¿Desea crear el usuario? (S/N): " confirmacion

# Si la confirmación es "S", montar el comando con los datos introducidos
if [ "$confirmacion" = "S" ]; then
    # Montaje de comando
    comando_useradd="useradd"
    [ -n "$crear_home" ] && comando_useradd+=" $crear_home"
    [ -n "$copiar_skel" ] && comando_useradd+=" $copiar_skel"
    comando_useradd+=" -s $shell -c '$nombre_completo'"
    [ -n "$expire" ] && comando_useradd+=" -e $expire"
    [ -n "$uid" ] && comando_useradd+=" -u $uid"
    [ -n "$gid" ] && comando_useradd+=" -g $gid"
    [ -n "$inactive" ] && comando_useradd+=" -f $inactive"
    comando_useradd+=" $nombre_usuario"
    
    # Ejecución del comando completo
    $comando_useradd

    # Establecer contraseña si se proporcionó
    if [ -n "$contrasena" ]; then
        echo "$nombre_usuario:$contrasena" | chpasswd
    fi

    echo "Usuario $nombre_usuario creado correctamente."
else
    echo "Operación cancelada."
fi
