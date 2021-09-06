struct Bloco {
    int valido;
    int sujo;
    int tag;
    char dados[128] = { '0' };
    int write_offset;
    int byteOffset;
};


struct Cache {
    Bloco blocos[64];
    unsigned int hits;
    unsigned int misses;
    unsigned int reads;
    unsigned int writes;

    void iniciarCache();
    void AtualizarBloco(int tag, int indice, int bloffset, char *dados, char *Mem, int operacao);
};

void Cache::iniciarCache() {this->hits = 0; this->misses = 0; this->reads = 0; this->writes = 0;
 for(int i = 0; i<64; i++) {this->blocos[i].valido=0;this->blocos[i].sujo = 0;this->blocos[i].tag=0;this->blocos[i].write_offset=0;this->blocos[i].byteOffset=0;}
}

void Cache::AtualizarBloco(int tag, int indice, int bloffset, char *dados, char *Mem, int operacao) {
    int spatialAddr = (indice << 4) + (tag << 10);
    this->blocos[indice].tag = tag;
    if(!this->blocos[indice].valido || !operacao) {
        /* atualiza a cache com os dados atuais da memória no endereço espacial especificado */
        for(int i=0; i<128; i++) this->blocos[indice].dados[i] = Mem[spatialAddr + i];
        this->blocos[indice].valido = 1;
    }     
    if(operacao) {
        /* atualiza a cache com os dados do store word */
        for(int i=0;i<32;i++) this->blocos[indice].dados[bloffset*32+ i] = dados[i];
    }
}