#!/bin/bash
# Recogemos los argumentos pasados desde Django
nombre_nas="{nombre_nas}"
direccion_nas="{direccion_nas}"
usuario_nas="{usuario_nas}"
contrasena_nas="{contrasena_nas}"
protocolo="{protocolo}"
ruta_montaje="{ruta_montaje}"
permisos="{permisos}"
modo_subida="{modo_subida}"

# Comprobamos si algún campo está vacío
if [ -z "$nombre_nas" ] || [ -z "$direccion_nas" ] || [ -z "$usuario_nas" ] || [ -z "$contrasena_nas" ]; then
    echo "Por favor, complete todos los campos del formulario de configuración del NAS."
    exit 1
fi

# Creamos el directorio para el montaje
sudo mkdir -p "$ruta_montaje"

# Montamos el recurso compartido en el directorio local
if [ "$protocolo" = "cifs" ]; then
    sudo mount -t cifs "$direccion_nas" "$ruta_montaje" -o username="$usuario_nas",password="$contrasena_nas"
elif [ "$protocolo" = "nfs" ]; then
    sudo mount -t nfs "$direccion_nas" "$ruta_montaje"
else
    echo "Protocolo de montaje no válido."
    exit 1
fi

# Agregamos la configuración de montaje para que sea persistente
echo "$direccion_nas $ruta_montaje $protocolo username=$usuario_nas,password=$contrasena_nas 0 0" | sudo tee -a /etc/fstab
sudo mount -a

# Configuramos los permisos de acceso a los archivos y directorios
sudo chown -R "$usuario_nas":"$usuario_nas" "$ruta_montaje"
sudo chmod -R "$permisos" "$ruta_montaje"

echo "Configuración del NAS completada correctamente."
