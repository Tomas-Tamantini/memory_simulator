#include <stdio.h>
#include <stdlib.h>
#include "models/structs.h"


void DecodeReqLine(char *reqLine, int *endereco, int *operacao, char *dados) {
    int aux = 0;
    char ender[4];
    while(reqLine[aux] != ' ') {
        ender[aux] = reqLine[aux];
        aux++;
    }
    aux++;

    *endereco = atoi(ender);
    *operacao = reqLine[aux] - '0';
    aux++;
    if(reqLine[aux] == ' ') {
        for(int i=0;i<32;i++) dados[i] = reqLine[aux + 1 + i];
    }

}



void MemoryWrite(Cache& cache, int index, char *Mem) {
    int endereco_anterior = cache.blocos[index].tag * 1024 + index * 16;
    int offset_anterior = cache.blocos[index].write_offset;
    int byte_offset = cache.blocos[index].byteOffset;
    for(int i=0; i<32; i++) { 
        // byte addressing   
        Mem[endereco_anterior * 8 + offset_anterior + byte_offset + i] = cache.blocos[index].dados[offset_anterior + i];
    }
}


char CPUreq(int endereco, int operacao, char *dados, Cache& cache, char *Mem) {

    int index = (endereco & 1008) >> 4;
    int tag = (endereco & 3072) >> 10;
    int byte_offset = endereco & 3;
    int block_offset = (endereco & 12) >> 2;
    int spatial_addr = index * 16 + tag * 1024;
    // Bloco de código responsável pela escrita
    if(operacao) {
        cache.writes++;
        // escreve na memória a palavra que já estava na cache antes se o bloco estiver sujo
        if(cache.blocos[index].sujo) {
            MemoryWrite(cache, index, Mem);
        }  

        cache.AtualizarBloco(tag, index, block_offset, dados, spatial_addr);
        cache.blocos[index].write_offset = block_offset;
        cache.blocos[index].byteOffset = byte_offset;
        cache.blocos[index].sujo = 1;

        return 'W';
    }

    // Bloco da leitura  
    else {
        cache.reads++;

        // bloco de código respósavel pelo miss
        if(!(cache.blocos[index].valido) ||  tag != cache.blocos[index].tag) {
            cache.misses++;
            // escreve na memória a palavra que já estava na cache antes se o bloco estiver sujo
            if(cache.blocos[index].sujo) {
                MemoryWrite(cache, index, Mem);
            }
            printf("MISS!\n");
            cache.blocos[index].sujo = 0;
            // atualiza a cache com os dados do endereço requisitado
            cache.AtualizarBloco(tag, index, block_offset, Mem, spatial_addr);
            return 'M';
        }
        
        cache.hits++;
        printf("HIT!\n");
        //for(int i=0; i<32; i++) printf("%c", cache.blocos[index].dados[block_offset + i]);
        return 'H';
    }
        
}

int main(int argc, char *argv[]) {
    if(argc != 2) {
        printf("Usage: ./MemSimulator.out [CPU request file]\n");
        return 1;
    }
    struct Cache cache;
    cache.iniciarCache();

    char Memoria[32768];
    
    FILE* input_file=fopen(argv[1], "r+t");
    FILE* output_file=fopen("result_C.txt", "w+t");
   
    if(input_file != NULL && output_file != NULL) {
        char reqLine[41];
        int endereco;
        int operacao;
        char dados[32];

        int controle = 0;

        while(!feof(input_file)) {
            fgets(reqLine, 41, input_file);

            /* filtro para ver se o programa leu uma linha que n existe */
            if(reqLine[0] - '0' < 0 || (reqLine[1] - '0' < 0 && reqLine[1] != ' ')) continue;
            
            DecodeReqLine(reqLine, &endereco, &operacao, dados);
            printf(" %s ", reqLine);
            /* escreve os resultados no arquivo de saída*/
            fprintf(output_file, "%d %d ", endereco, operacao);
            if(operacao == 1) {
                for(int i=0; i<32; i++) fprintf(output_file, "%c", dados[i]);
                
            }
            printf(" %d ", controle);
            fprintf(output_file, " %c\n", CPUreq(endereco,operacao,dados,cache,Memoria));
            controle++;
        }

        fprintf(output_file, "\nREADS: %d\nWRITES: %d\nHITS: %d\nMISSES: %d\nHIT RATE: %f\nMISS RATE: %f", 
                    cache.reads, cache.writes, cache.hits, cache.misses, (float)cache.hits/cache.reads, (float)cache.misses/cache.reads);

        fclose(input_file);
        fclose(output_file);
        return 0;
    }
    
    printf("Erro ao carregar os arquivos de entrada/saída.");
    return 1;
}

