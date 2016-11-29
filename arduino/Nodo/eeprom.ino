#include <EEPROM.h>
#include "setting.h"




struct _setting setting;

struct _conv16to8 {
  union {
    unsigned int a;
    unsigned char bytes[2];
  };  
}conv16to8;
 

void load_setting(void){
  unsigned int i, checksum;
  uint8_t data[sizeof(setting)];
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {  
  checksum = 0;
 
  for(i = 0; i<sizeof(setting); i++){
      *((unsigned char*)(&setting) + i) = 0; 
      data[i] = EEPROM.read(i);
      checksum = checksum + data[i];
      /*Serial.print("i: ");
      Serial.println(i);
      Serial.print("value: ");
      Serial.println(data[i],HEX);*/
  }

  conv16to8.bytes[1] = EEPROM.read(sizeof(setting));
  conv16to8.bytes[0] = EEPROM.read(sizeof(setting) + 1);

  if(conv16to8.a == checksum){
    //Serial.println("CHECKSUM UGUALE");
    //Popula struttura
    for(i = 0; i<sizeof(setting); i++){
        *((unsigned char*)(&setting) + i) = data[i]; 
    } 
    /*   
    Serial.println("popula setting");
    Serial.println("ADDRESS CORDINATORE: ");

    conv64to8.a =  setting.address_cordinatore;
    Serial.println(conv64to8.bytes[0],HEX);
    Serial.println(conv64to8.bytes[1],HEX);
    Serial.println(conv64to8.bytes[2],HEX);
    Serial.println(conv64to8.bytes[3],HEX);
    Serial.println(conv64to8.bytes[4],HEX);
  */


    
  }else {
    //checksum diverso [errore] , popula default
    Serial.println("CHECKSUM **DIVERSO**");
    setting.address_nodo = ADD_NODO_VERGINE;
    setting.address_cordinatore = 0xFFFFFFFFF0LL;
    setting.tipo_nodo = TIPO_NODO;
    setting.dimmer_1 = 0;
    setting.dimmer_2 = 0;
    setting.dimmer_3 = 0;
    setting.dimmer_4 = 0;

    //Save
    save_setting();
    
  }
}
}

void save_setting(void){
  unsigned int i, checksum;
  uint8_t data[sizeof(setting)];
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {  
  checksum = 0;

  for(i = 0; i<sizeof(setting); i++){
      data[i] = *((unsigned char*)(&setting) + i);     
      checksum = checksum + data[i];
      EEPROM.write(i, data[i]);
      /*Serial.print("i: ");
      Serial.println(i);
      Serial.print("value: ");
      Serial.println(data[i],HEX);*/
      
  }
  //Scrivi checksum
  conv16to8.a = checksum;
  EEPROM.write(sizeof(setting), conv16to8.bytes[1]);
  EEPROM.write(sizeof(setting) + 1, conv16to8.bytes[0]);  

}
  
}
