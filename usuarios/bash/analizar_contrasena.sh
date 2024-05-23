#!/bin/bash
# Recoge los argumentos pasados desde Python
contrasena="{contrasena}"
validacion="{validacion}"

# Función para generar una contraseña segura con pwgen
generar_contrasena_segura() {
    pwgen -1 -s 16
}

# Mostrar la contraseña proporcionada
echo "Contraseña proporcionada: $contrasena"

# Codificar la contraseña proporcionada con mkpasswd
contrasena_codificada=$(mkpasswd -m sha-512 "$contrasena")

# Contar cuantas veces aparece la contraseña proporcionada en el sistema
veces=$(grep -c "$contrasena_codificada" /etc/shadow)
echo "Número de veces que aparece la contraseña en el sistema: $veces"

echo ""

# Comprobar si la contraseña es insegura y generar una recomendación si es necesario
if [ "$validacion" = "False" ]
then
    echo "La contraseña no cumple con los criterios de seguridad."

    # Generar una contraseña segura como recomendación
    nueva_contrasena=$(generar_contrasena_segura)
    echo "Recomendación: $nueva_contrasena"
else
    echo "La contraseña cumple con los criterios de seguridad."
fi
