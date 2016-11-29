# LightHub

--------Raspberry:---------
Raspberry è il cordinatore e webserver, il webserver è installato in "/home/app", installate librerie "RF24" per nrf24l01+ , 
pyton tornado, mysql.

Connessioni:
Raspberry      nrf24l01+
22[GPIO25]       CE
24[GPIO8]        CSN
23[GPIO11]       SCK
21[GPIO9]        MISO
20[GPIO10]       MOSI
  ---            IRQ
 

--------Arduino UNO:----------
Arduino Uno usati come nodi
Per ogni nodo cambiare "const uint64_t ADD_NODO = 0x0000000023LL;" DEVE ESSERE UNIVOCO !

Connessioni:
dimmer_1 : 3
dimmer_2 : 4
dimmer_3 : 5
dimmer_4 : 6

Arduino      nrf24l01+
7                CE
8                CSN
13               SCK
11               MISO
12               MOSI
  ---            IRQ
  
switch [per programmazione, acquisizione da parte del cordinatore]  - A0
led - A1

La programmazione avviene in automatico, svolgere i seguenti passi:
1 - Premere il puslante del nodo
2- Nella web-app sezione "Nodi" , clicca "Aggiungi Nodo"


