#!/bin/bash
# Recoger los argumentos
nombre_certificado="{nombre_certificado}"
organizacion="{organizacion}"
unidad_organizacional="{unidad_organizacional}"
localidad="{localidad}"
provincia="{provincia}"
pais="{pais}"
correo_electronico="{correo_electronico}"
departamento="{departamento}"
clave="{clave}"
comentarios="{comentarios}"
directorio_salida="{directorio_salida}"

# Mostrar los datos recogidos
echo "Datos recogidos:"
echo "Nombre del certificado: $nombre_certificado"
echo "Organización: $organizacion"
echo "Unidad organizacional: $unidad_organizacional"
echo "Localidad: $localidad"
echo "Provincia: $provincia"
echo "País: $pais"
echo "Correo electrónico: $correo_electronico"
echo "Departamento: $departamento"
echo "Clave: $clave"
echo "Comentarios: $comentarios"
echo "Directorio de salida: $directorio_salida"

# Solicitar confirmación para continuar
read -p "¿Desea generar el certificado con estos datos? (s/n): " confirmacion

# Comprobar la respuesta
if [ "$confirmacion" != "s" ]
then
    echo "Operación cancelada. No se generará el certificado."
    exit 1
fi

if [ -z "$directorio_salida" ]
then
    # Si no se especifica, utilizar la ruta predeterminada
    directorio_salida="/etc/ssl/certs"
fi

# Comprobar si el directorio de salida existe, si no, crearlo
if [ ! -d "$directorio_salida" ]
then
    mkdir -p "$directorio_salida"
fi

# Generar comando para openssl
comando="openssl req -new -newkey rsa:2048 -days 365 -nodes -x509"

# Agregar cada parámetro si está presente
if [ -n "$organizacion" ]
then
    comando="$comando -subj '/O=$organizacion'"
fi

if [ -n "$unidad_organizacional" ]
then
    comando="$comando -subj '/OU=$unidad_organizacional'"
fi

if [ -n "$localidad" ]
then
    comando="$comando -subj '/L=$localidad'"
fi

if [ -n "$provincia" ]
then
    comando="$comando -subj '/ST=$provincia'"
fi

if [ -n "$pais" ]
then
    comando="$comando -subj '/C=$pais'"
fi

if [ -n "$correo_electronico" ]
then
    comando="$comando -subj '/emailAddress=$correo_electronico'"
fi

if [ -n "$nombre_certificado" ]
then
    comando="$comando -subj '/CN=$nombre_certificado'"
fi

# Establecer la ruta completa del archivo de certificado
ruta_certificado="$directorio_salida/$nombre_certificado.crt"

# Ejecutar el comando
$comando -keyout "$ruta_certificado.key" -out "$ruta_certificado"

# Mostrar mensaje de éxito
echo "Certificado generado con éxito en: $directorio_salida"
