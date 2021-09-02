#include <stdio.h>

int *DecParaBin(int n) {
    static int numBin[32];
    int i = 31;
    while (n > 0) {
        numBin[i] = n % 2;
        n = n / 2;
        i--;
    }
    return numBin;
}


struct Bloco {
    int valido = 0;
    int sujo = 0;
    int tag;
    char dados[128];
};


struct Cache {
    Bloco blocos[64];
    unsigned int hits = 0;
    unsigned int misses = 0;
    unsigned int reads = 0;
    unsigned int writes = 0;

    void AtualizarTag(int *endereco, int indice);
};

void Cache::AtualizarTag(int *endereco, int indice) {
    this->blocos[indice].tag = endereco[20] * 8 + endereco[21] * 4 + endereco[22] * 2 + endereco[23] * 1;
}



char CPUreq(int endereco, int operacao, char *dados, Cache& cache, char *Mem) {
    int *addr = DecParaBin(endereco);
    // tradução do índice do binário para o decimal
    int index = addr[29] * 1 + addr[28] * 2 + addr[27] * 4 + addr[26] * 8 + addr[25] * 16 + addr[24] * 32; 
    int block_offset = (addr[31] * 1 + addr[30] * 2) * 32;
    int endereco_anterior = cache.blocos[index].tag * 64 + index; // endereco atual presente na cache

    // Bloco de código responsável pela escrita
    if(operacao) {
        cache.writes++;
        // escreve na memória o bloco que já estava na cache antes se o bloco estiver sujo
        if(cache.blocos[index].sujo) {
            for(int i=0; i<128; i++) { 
                // byte addressing
                Mem[endereco_anterior * 8 + i] = cache.blocos[index].dados[i];
            }
        }  
        cache.AtualizarTag(addr, index); // atualiza o bloco após
        for(int i=0;i<32;i++) cache.blocos[index].dados[block_offset + i] = dados[i];
        cache.blocos[index].sujo = 1;
        cache.blocos[index].valido = 1;
        return 'W';
    }

    // Bloco da leitura  
    else {
        cache.reads++;
        if(!(cache.blocos[index].valido) || endereco != endereco_anterior) {
            cache.misses++;
            printf("\nMISS! A palavra requisitada n está no cache");
            // atualiza a cache com os dados do endereço requisitado
            for(int i=0; i<128; i++) cache.blocos[index].dados[i] = Mem[endereco * 8 + i];
            cache.AtualizarTag(addr, index);
            return 'M';
        }
        cache.hits++;
        printf("\nHIT! Dados da palavra requisitada: ");
        for(int i=0; i<32; i++) printf("%c", cache.blocos[index].dados[block_offset + i]);
        return 'H';
    }
        
}

int main() {
    struct Cache cch;
    char Memoria[32768];
    FILE* input_file=fopen("input_model.txt", "r+t");
    if(input_file == NULL) {
        printf("Erro ao carregar o arquivo de teste");
        return 1;
    }
    int addr, op; 
    char data[32];
    fscanf(input_file, "%d %d %s", &addr, &op, data);
    printf("%d %d %s %c\n", addr, op, data, CPUreq(addr,op,data,cch,Memoria));
    while(!feof(input_file)) {
        fscanf(input_file, "%d %d %s", &addr, &op, data);
        printf("%d %d %s %c\n", addr, op, data, CPUreq(addr,op,data,cch,Memoria));  
    }
    fclose(input_file);
    return 0;

}