#!/bin/bash
# Recoger los argumentos pasados desde Django
directorio="{directorio}"
usuario="{usuario}"
grupo="{grupo}"
tipo="{tipo}"

# Mostrar los datos si existen
echo "Directorio: $directorio"
echo "Usuario: $usuario"
echo "Grupo: $grupo"
echo "Tipo: $tipo"

read -p "¿Estos parametros son ciertos? (S/N)" confirmacion

if [ "$confirmacion" = "S" ]
then
    # Verificar si se proporcionaron datos del segundo formulario
    if [ -n "$directorio" ] && [ -n "$usuario" ]
    then
        if [ "$tipo" = "u" ] && [ -z "$grupo" ]
        then
            # Montar el comando para cambiar el usuario y el grupo
            comando_chown="chown -R $usuario:$usuario $directorio"

            # Ejecutar el comando para cambiar el usuario y el grupo
            $comando_chown

            echo "Usuario y grupo cambiados correctamente para $directorio"
        elif [ "$tipo" = "u" ] && [ -n "$grupo" ]
        then
            # Montar el comando para cambiar el usuario y el grupo
            comando_chown="chown -R $usuario:$grupo $directorio"

            # Ejecutar el comando para cambiar el usuario y el grupo
            $comando_chown

            echo "Usuario y grupo cambiados correctamente para $directorio"
        elif [ "$tipo" = "g" ] && [ -n "$grupo" ]
        then
            # Montar el comando para cambiar el grupo
            comando_chgroup="chgrp -R $grupo $directorio"

            # Ejecutar el comando para cambiar el grupo solamente
            $comando_chgroup
        elif [ "$tipo" = "g" ] && [ -z "$grupo" ]
        then
            echo "Dato de grupo faltante"
        else
            echo "Error inesperado, vuelva a rellenar el form"
        fi
    else
        echo "Datos insuficientes para cambiar usuario/grupo de este directorio."
    fi
else
    echo "Operacion cancelada"
fi
