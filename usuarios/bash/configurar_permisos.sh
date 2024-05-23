#!/bin/bash
# Recoger los argumentos pasados desde Django
directorio="{directorio}"
usuario="{usuario}"
permisos="{permisos}"
permisos_grupo="{permisos_grupo}"
permisos_otros="{permisos_otros}"

# Mostrar los datos si existen
echo "Directorio: $directorio"
echo "Usuario: $usuario"
echo "Permisos para usuario: $permisos"
echo "Permisos para grupo: $permisos_grupo"
echo "Permisos para otros: $permisos_otros"

# Verificar si se proporcionaron datos del primer formulario
if [ -n "$directorio" ] && [ -n "$usuario" ] && [ -n "$permisos" ] && [ -n "$permisos_grupo" ] && [ -n "$permisos_otros" ]
then
    # Montar el comando para cambiar los permisos
    comando_chmod="chmod $permisos$permisos_grupo$permisos_otros $directorio"

    # Ejecutar el comando para cambiar los permisos
    $comando_chmod

    echo "Permisos cambiados correctamente para $directorio"
else
    echo "Datos insuficientes para cambiar permisos."
fi
