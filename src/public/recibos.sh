#!/bin/bash

# Verificar el número de argumentos
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <parametro1> <parametro2>"
    exit 1
fi

# Asignar parámetros a variables
parametro1="$1"
parametro2="$2"

# Ejecutar el script de Python
#/home/pablo/.pyenv/versions/3.9.10/envs/recibos_sueldo/bin/python /home/pablo/recibos/parcer_recibos_sueldo.py "$parametro1" "$parametro2"
python3 ../parcer_recibos_sueldo.py "$parametro1" "$parametro2"

# Verificar el código de retorno del script de Python
if [ $? -eq 0 ]; then
    echo "El script de Python se ejecutó correctamente."
    exit 0
else
    echo "Hubo un error al ejecutar el script de Python."
    exit 1
fi
