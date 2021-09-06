#!/bin/bash
printf "Deseja rodar a Simulação em Python? [S (sim) | n (rodar em C)] "
read resposta

if [ $resposta = "n" -o $resposta = "N" ]; then
    if !(g++ MemSimulator.c -o MemSimulator.out); then
        echo "Não foi possível compilar, g++ está instalado em sua máquina?"
        exit 1
    fi
    printf "Digite o path do arquivo texto de requisições da CPU a ser testado (Default: ./input_model.txt):  "
    read reqsPath
    if [ -z "$reqsPath" ]; then 
        ./MemSimulator.out input_model.txt
        echo "Resultados escritos em result_C.txt"
    else 
        ./MemSimulator.out $reqsPath
        echo "-------------------------------------------------------------
        Resultados escritos em result_C.txt"
    fi
fi

