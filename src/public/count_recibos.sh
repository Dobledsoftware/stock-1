#!/bin/bash

# Verificar el número de argumentos
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <parametro1>"
    exit 1
fi

# Asignar parámetros a variables
parametro1="$1"

# Ejecutar el script de Python
python3 ../count_recibos.py "$parametro1"
#python /home/pablo/desarrollo/docker/python/count_recibos.py "$parametro1"

# Verificar el código de retorno del script de Python
# if [ $? -eq 1 ]; then
#     echo "Hubo un error al ejecutar el script de Python."
#     exit 1
# fi

echo $?
