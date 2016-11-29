
#ifndef __SETTING__
#define __SETTING__



struct _setting {
  uint64_t address_nodo;
  uint64_t address_cordinatore;
  unsigned char tipo_nodo;
  unsigned char dimmer_1;
  unsigned char dimmer_2;
  unsigned char dimmer_3;
  unsigned char dimmer_4;
};


struct _conv64to8 {
  union {
    uint64_t a;
    unsigned char bytes[8];
  };  
}conv64to8;


#endif
