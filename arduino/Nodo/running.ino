#include <util/atomic.h>

void work(void){
  if(radio.available())
  {

     //Serial.print(F(".....recive.... "));
      uint8_t len = radio.getDynamicPayloadSize();

      //Serial.print(F("[RX] [LEN]: "));
      //Serial.println(len);
      
         if(len){
                radio.read( receive_payload, len );
                receive_payload[len] = 0;
/*
                for(int i =0; i<len;i++){
                  Serial.print(F("[dato]: "));          
                  Serial.println(receive_payload[i],HEX);
                }
*/

                switch(receive_payload[0]) {
                    case 0xa3:
                      radio.stopListening();
                      //Serial.print(F("imvia stato]"));
                      //leggi stato e invia
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {                      
                      receive_payload[0] = 0xa2;
                      receive_payload[1] = TIPO_NODO;

                      receive_payload[2] = CH1b;
                      receive_payload[3] = CH2b;
                      receive_payload[4] = CH3b;
                      receive_payload[5] = CH4b;

                      receive_payload[6] = CH1d;
                      receive_payload[7] = CH2d;
                      receive_payload[8] = CH3d;
                      receive_payload[9] = CH4d;
}                     
                      radio.write(receive_payload, 10);
                    break;
                  
                  
                    //Ricevo comandi stato da parte del CORDINATORE
                    case 0xE0:
                      CH1b = receive_payload[1];
                      CH2b = receive_payload[2];
                      CH3b = receive_payload[3];
                      CH4b = receive_payload[4];

                      CH1d = receive_payload[5];
                      CH2d = receive_payload[6];
                      CH3d = receive_payload[7];
                      CH4d = receive_payload[8];
/*
                      Serial.println(CH1b);
                      Serial.println(CH2b);
                      Serial.println(CH3b);
                      Serial.println(CH4b);
                      Serial.println(CH1d);
                      Serial.println(CH2d);
                      Serial.println(CH3d);
                      Serial.println(CH4d);
*/
                    break;
                  default:
                  break;
                }
          
          
          
          
          }
    
    
      radio.stopListening();
     radio.startListening();

   if(CH1b){
        dimmerCH1.on();
        dimmerCH1.set(CH1d);
      }else{
        dimmerCH1.off();
      }
      
      if(CH2b){
        dimmerCH2.on();
        dimmerCH2.set(CH2d);
      }else{
        dimmerCH2.off();
      }  
    
      if(CH3b){
        dimmerCH3.on();
        dimmerCH3.set(CH3d);
      }else{
        dimmerCH3.off();
      }  
    
      if(CH4b){
        dimmerCH4.on();
        dimmerCH4.set(CH4d);
      }else{
        dimmerCH4.off();
      }    


      
  }

  /*
  if(radio.available())
  {
    Serial.print(F("Radio available"));
    
    // Fetch the payload, and see if this was the last one.
    uint8_t len = radio.getDynamicPayloadSize();
    
    // If a corrupt dynamic payload is received, it will be flushed
    if(len){
    
      radio.read( receive_payload, len );
  
      // Put a zero at the end for easy printing
      receive_payload[len] = 0;
  
      Serial.println(F("*******************[RX]***********************"));
      for(int i =0; i<len;i++){
        Serial.print(F("[RX]                : "));          
        Serial.println(receive_payload[i],HEX);
      }            
    }      
    // First, stop listening so we can talk
    radio.stopListening();
    // Now, resume listening so we catch the next packets.
    radio.startListening();
  }
  */
}
