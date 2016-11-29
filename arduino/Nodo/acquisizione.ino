#include <util/atomic.h>

void acquisizione(void){
 
        radio.startListening();
        //Aspetta Cordinatore Trasmette su ADD_NODO vergine

        // Wait here until we get a response, or timeout
        started_waiting_at = millis();
        timeout = false;
        while ( ! radio.available() && ! timeout )
          if (millis() - started_waiting_at > 10000 )
            timeout = true;

        if ( timeout )
        {
          Serial.println("Fallita [ ACQUISIZIONE ] Time Out");
            delay(3000);          
            //Riavvia Arduino
            asm volatile ("  jmp 0");
            return;
        }
        else
        {                
          // Fetch the payload, and see if this was the last one.
          len = radio.getDynamicPayloadSize();
          
          // If a corrupt dynamic payload is received, it will be flushed
          if(!len){
            //Errore Trasmissione
            //Riavvia Arduino
            Serial.println("Now reset");
            delay(3000); 
            asm volatile ("  jmp 0");
            return; 
          }
          
          radio.read( receive_payload, len );
    
          // Put a zero at the end for easy printing
          receive_payload[len] = 0;
/*
          Serial.print("[RX] [LEN]: ");
          Serial.println(len);
          Serial.println("[RX] (Cordinatore Acquisizione)= ");
          for(int i =0; i<len;i++){
            Serial.print("[RX]                : ");          
            Serial.println(receive_payload[i],HEX);
          }
    */
          // First, stop listening so we can talk
          radio.stopListening();

          //Estrai Indirizzo Cordinatore
          //-Dati Validi ?
          if(len != (uint8_t)6){
            Serial.print("[ ACQUISIZIONE ]errore LEN - ");
            Serial.println(len);
            Serial.println("Now reset");                       
            delay(5000);        
            asm volatile ("  jmp 0");
            return;             
          }
          if(receive_payload[0] == 0xAF){                                 //Acquisisce Address da parte del Cordinatore !
            //estrai cordinatore 5byte
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {              
            conv64to8.bytes[0] = receive_payload[1];
            conv64to8.bytes[1] = receive_payload[2];
            conv64to8.bytes[2] = receive_payload[3];
            conv64to8.bytes[3] = receive_payload[4];
            conv64to8.bytes[4] = receive_payload[5];
            conv64to8.bytes[5] = 0;
            conv64to8.bytes[6] = 0;
            conv64to8.bytes[7] = 0;
            setting.address_cordinatore = conv64to8.a;           
}            
            //Serial.print("[ ACQUISIZIONE ]Cordinatore address: ");
            //Serial.println(setting.address_cordinatore);
            radio.openWritingPipe(setting.address_cordinatore);
            radio.printDetails();
            
            setting.address_nodo = ADD_NODO;
            radio.openReadingPipe(1,setting.address_nodo);        //Mio Nodo!            
            save_setting();

                                                                          //Invia Indirizzo del Nodo ! *********************************************
            delay(300);
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {  
            receive_payload[0] = 0xAE;
            conv64to8.a = ADD_NODO;
            receive_payload[1] = conv64to8.bytes[0];
            receive_payload[2] = conv64to8.bytes[1];
            receive_payload[3] = conv64to8.bytes[2];
            receive_payload[4] = conv64to8.bytes[3];
            receive_payload[5] = conv64to8.bytes[4];
}            
            radio.write(receive_payload, 6);

            Serial.println("[ ACQUISIZIONE ] Completata ...Success");
            delay(10);    
            asm volatile ("  jmp 0");
            return;             

           }else{
            Serial.println("[ ACQUISIZIONE ]errore Tipo Messaggio");
            delay(5000);    
            asm volatile ("  jmp 0");
            return;             
          }          
        }
  

}
