#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "setting.h"
#include "Dimmer.h"
#include <util/atomic.h>
/*
Protocollo

            1 char                                      |      
--------------------------------------------------------|----------------------------------------------------------------------------
     Tipo Messaggio                                     |
-0XAF=Acquisizione Cordinatore                             |
-1=Invio Comandi al Nodo                                |
-2=Leggi Valori del Nodo e Tipo Nodo                    |
-3=Ping, Nodo is Alive?                                 |
-------------------------------------------------------------------------------------------------------------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-0XAF=Acquisizione Cordinatore (Cordinatore invia questo playload al Nodo)
--------------------------------------------------------|----------------------------------------------------------------------------
                    1 char                              |       Add Cordinatore 5-byte     
--------------------------------------------------------|----------------------------------------------------------------------------
                                                        |
                                                        |
                     0XAF                               |
                                                        |

-0XAF=Acquisizione Cordinatore (Nodo invia questo playload al Cordinatore)
--------------------------------------------------------|---------------------------|-------------------------------------------------
                    1 char                              |       Add Nodo 5-byte     |
--------------------------------------------------------|---------------------------|-------------------------------------------------
                                                        |                           |
                                                        |                           |
                     0XAE                               |                           |
                                                        |                           |
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-0XA3 Leggi Valori del Nodo e Tipo Nodo
cordinatore invia
--------------------------------------------------------|----------------------------------------------------------------------------
                    1 char                              |         
--------------------------------------------------------|----------------------------------------------------------------------------
                                                        |
                                                        |
                     0XA3                               |
                                                        |

nodo risponde
--------------------------------------------------------|---------------------------|-------------------------------------------------
                    1 char                              |          tipo             |  ch1  | ch2 | ch3 | ch4
--------------------------------------------------------|---------------------------|-------------------------------------------------
                                                        |                           |
                                                        |          1byte            | 0-100 | 0-100
                     0XA2                               |                           |
                                                        |                           |
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-0xE0 Ricevo comandi stato da parte del cordinatore
cordinatore invia
--------------------------------------------------------|----------------------------------------------------------------------------
                    1 char                              |         
--------------------------------------------------------|----------------------------------------------------------------------------
                                                        |
                                                        |
                     0xE0                               |  ch1b,ch2b,ch3b,ch4b  ,ch1d,ch2d,ch3d,ch4d
                                                        |

                                  

*/
//DIMMER SETTING
/*const int channel_1 3
const int channel_2 4
const int channel_3 5
const int channel_4 6
*/
Dimmer dimmerCH1(3, DIMMER_RAMP,0.1,50);
Dimmer dimmerCH2(4, DIMMER_RAMP,0.1,50);
Dimmer dimmerCH3(5, DIMMER_RAMP,0.1,50);
Dimmer dimmerCH4(6, DIMMER_RAMP,0.1,50);


const uint64_t ADD_NODO_VERGINE = 0x0000000010LL;   //NODO VERGINE !
const uint64_t ADD_NODO = 0x0000000023LL; //0xFF000AA020LL; //0x0000000020LL;           //NODO [univoco]!

                            
const char TIPO_NODO = 5;                           // TIPO DIMMER 4CH

//dimmer
uint8_t CH1b,CH2b,CH3b,CH4b,CH1d,CH2d,CH3d,CH4d;

/* PIN DEFINITION */

// Set up nRF24L01 radio on SPI bus plus pins 7 & 8
RF24 radio(7,8);


extern  struct _setting setting;
const int max_payload_size = 32;
uint8_t receive_payload[max_payload_size+1]; // +1 to allow room for a terminating NULL char
uint8_t len = 0;

typedef enum { VERGINE = 0, ACQUISIZIONE, RUNNING } role_e;                 // The various roles supported by this sketch
role_e stato_NODO = VERGINE;

//general variable
bool timeout = false;
unsigned long started_waiting_at;



void setup(void)
{
  Serial.begin(115200);
  pinMode(A0, INPUT);
  digitalWrite(A0, HIGH);
  
  pinMode(A1, OUTPUT);
  digitalWrite(A1, LOW);

  //Leggi impostazioni EEPROM
  load_setting();

  radio.begin();
  // enable dynamic payloads
  radio.enableDynamicPayloads();
  // optionally, increase the delay between retries & # of retries
  radio.setChannel(90);
  radio.setDataRate(RF24_2MBPS);
  radio.setPALevel(RF24_PA_MAX);
 
  radio.setRetries(5,15);

  //radio.openWritingPipe(pipes[1]);         
  radio.openReadingPipe(1,setting.address_nodo);        //Mio Nodo !
  radio.openWritingPipe(setting.address_cordinatore);

  
  radio.startListening();

  //Verifica se VERGINE
  if(setting.address_nodo == ADD_NODO_VERGINE){
    stato_NODO = VERGINE;
    digitalWrite(A1, HIGH);
  }else{

    Serial.println("[STATO].....Running");

    stato_NODO = RUNNING;
    digitalWrite(A1, LOW);
  }

  radio.printDetails();

  //test
  CH1b = 0;
  CH2b = 0;
  CH1d = 0;
  CH2d = 0;
  CH3d = 0;
  CH4d = 0;


  dimmerCH1.begin(); 
  dimmerCH2.begin();
  dimmerCH3.begin();
  dimmerCH4.begin();
  
    TCNT2 = 0;                      // Clear timer
    TCCR2A = 0x02;         // Timer config byte A
    TCCR2B = 0x02;         // Timer config byte B
    TIMSK2 = 0x02;                 // Timer Compare Match Interrupt Enable
    OCR2A = 100 * 60 / 50 - 1; // Compare value (frequency adjusted)
  
//dimmerCH1.setMinimum(1);

  dimmerCH1.set(CH1d);
  dimmerCH2.set(CH2d);
  dimmerCH3.set(CH3d);
  dimmerCH4.set(CH4d);



  
}

void loop(void)
{

   switch(stato_NODO){
      case VERGINE:
        digitalWrite(A1, HIGH);
        Serial.println("[ VERGINE ]");

        if(digitalRead(A0)==0){
          //Modalita programmazione [ACQUISIZIONE]  
          digitalWrite(A1, HIGH);
      ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {  
          stato_NODO = ACQUISIZIONE;
          setting.address_nodo = ADD_NODO_VERGINE;
          radio.openReadingPipe(1,setting.address_nodo);        //Mio Nodo VERGINE!
      }
          radio.stopListening();
        }
      break;
    
      case ACQUISIZIONE:
        Serial.println("[ ACQUISIZIONE ]");
        acquisizione();
      break;    
        
      case RUNNING:
        //Serial.println("[ RUNNING ]");

        if(digitalRead(A0)==0){
          //Modalita programmazione [ACQUISIZIONE]  
          digitalWrite(A1, HIGH);
ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {            
          stato_NODO = ACQUISIZIONE;
          setting.address_nodo = ADD_NODO_VERGINE;
          radio.openReadingPipe(1,setting.address_nodo);        //Mio Nodo VERGINE!
}          
          radio.stopListening();
          break;
        }
        
        //Running
        work();
      break;    
   }

  
  /*
    while ( radio.available() )
    {
      // Fetch the payload, and see if this was the last one.
      uint8_t len = radio.getDynamicPayloadSize();
      
      // If a corrupt dynamic payload is received, it will be flushed
      if(!len){
        continue; 
      }
      
      radio.read( receive_payload, len );

      // Put a zero at the end for easy printing
      receive_payload[len] = 0;

      Serial.print(F(" value="));
      Serial.println(receive_payload);

      // First, stop listening so we can talk
      radio.stopListening();
      // Now, resume listening so we catch the next packets.
      radio.startListening();
    }


    */
}










