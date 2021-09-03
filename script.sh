#!/bin/bash
echo "Hello World!"

if g++ MemSimulator.c -o MemSimulator.out; then
    ./MemSimulator.out input_model.txt
    echo "Resultados escritos em result_C.txt"
else
    echo "Não foi possível compilar, g++ está instalado em máquina?"
fi

