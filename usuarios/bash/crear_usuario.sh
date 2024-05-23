#!/bin/bash
# Recogida de parámetros
nombre_usuario="{nombre_usuario}"
contrasena="{contrasena}"
grupo_principal="{grupo_principal}"
otros_grupos="{otros_grupos}"
nombre_completo="{nombre_completo}"
skel="{skel}"
directorio_home="{directorio_principal}"
shell="{shell}"
expire="{expire}"
uid="{uid}"
gid="{gid}"
inactive="{inactivo}"

# Mostrar los datos si existen
echo "Nombre de usuario: $nombre_usuario"
[ -n "$contrasena" ] && echo "Contraseña: [PROPORCIONADA]"
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

# Preguntar al usuario si desea confirmar la operación
read -p "¿Desea crear el usuario? (S/N): " confirmacion

# Instalar el paquete esencial para generar contraseñas encriptadas.
sudo apt-get install whois

# Si la confirmación es "S", montar el comando con los datos introducidos
if [ "$confirmacion" = "S" ]
then
    # Generar la contraseña encriptada usando mkpasswd
    contrasena_encriptada=$(mkpasswd -m sha-512 "$contrasena")

    # Montaje de comando
    comando_useradd="useradd"
    comando_useradd+=" -m -d $directorio_home"
    [ -n "$skel" ] && comando_useradd+=" -k $skel"
    comando_useradd+=" -s $shell -c '$nombre_completo'"
    [ -n "$expire" ] && comando_useradd+=" -e $expire"
    [ -n "$uid" ] && comando_useradd+=" -u $uid"
    [ -n "$gid" ] && comando_useradd+=" -g $gid"
    [ -n "$inactive" ] && comando_useradd+=" -f $inactive"
    comando_useradd+=" -g $grupo_principal -p $contrasena_encriptada $nombre_usuario"

    # Ejecución del comando completo
    $comando_useradd

    # Añadir otros grupos si se proporcionaron
    if [ -n "$otros_grupos" ]
    then
        usermod -aG $otros_grupos $nombre_usuario
    fi

    echo "Usuario $nombre_usuario creado correctamente."
else
    echo "Operación cancelada."
fi
