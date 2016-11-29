#!/usr/bin/env python

from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO
import time
import struct
from array import array
import threading


class RF24module:
    add_cordinatore = 0x1FFFFFFFF0
    channel = 90;
    add_nodo_vergine = 0x0000000010

    def __init__(self):
        self.list1Lock = threading.Lock()

        self.irq_gpio_pin = None
        self.radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
        self.radio.begin()
        self.radio.enableDynamicPayloads()
        self.radio.setRetries(15,15)
        self.radio.setChannel(RF24module.channel)
        self.radio.setDataRate(RF24_2MBPS)
        self.radio.setPALevel(RF24_PA_MAX)
        self.radio.openReadingPipe(1,RF24module.add_cordinatore)      #Mio cordinatore !
        self.radio.printDetails()
        self.radio.startListening()
        self.millis = lambda: int(round(time.time() * 1000))

    def set_address_nodo(self, nodo):
        self.radio.openWritingPipe(nodo)      #sed address Nodo !

    #Trova e acquisisci Nodo Vergine!
    def find_nodo(self):
        print("Find-Acquisizione del Nodo.......")
        self.radio.stopListening()
        self.radio.openWritingPipe(RF24module.add_nodo_vergine)
        playload = [0xAF]
        byteplayload = bytearray.fromhex('{:6x}'.format(RF24module.add_cordinatore))
        byteplayload.reverse()
        for item in byteplayload:
            playload.append(item)       
        a = "".join(map(chr, playload))
        self.radio.write(a, 6)
        self.radio.startListening()

        # Wait here until we get a response, or timeout
        started_waiting_at = self.millis()
        timeout = False
        while (not self.radio.available()) and (not timeout):
            if (self.millis() - started_waiting_at) > 2000:
                timeout = True
        if timeout:
            print('failed, response timed out.')
            return None
        else:
            lend = self.radio.getDynamicPayloadSize()
            if(lend == 0):
                print("[ ACQUISIZIONE ]errore LEN")
            else:
                receive_payload = self.radio.read(lend)
                address_nodo = []
                if receive_payload[0] == 0xAE:
                    i = 0
                    for item in receive_payload:
                        if i > 0:
                            address_nodo.append(item)
                        i = i + 1
                    address_nodo.reverse()
                    print("[ ACQUISIZIONE ]....................OK")
                    at = [0,0,0]
                    for item in address_nodo:
                        at.append(item)
                    print (at)
                    a = array('B', at[:8])
                    ah = struct.unpack('Q', a)
                    ah1 = hex(ah[0])
                    address_nodo = ah1[2:]
                    a = address_nodo[:-1]
                    temp = a[:-6]
                    a1 = temp[0:2]
                    a2 = temp[2:4]
                    a3 = temp[4:6]
                    a4 = temp[6:8]
                    a5 = temp[8:10]
                    return a5 + a4 + a3 + a2 + a1
            return None

    def get_stato_nodo(self,nodo):

        #print("************************TRASMETTO********************")
        #print(nodo)

        #send get stato
        self.radio.stopListening();

        a = int(nodo, 16) #hex(int(nodo, 16))
        self.radio.openWritingPipe(a)
        self.radio.openReadingPipe(1,RF24module.add_cordinatore)      #Mio cordinatore !

        #self.radio.printDetails()

        playload = [0xA3]
        a = "".join(map(chr, playload))
        r = self.radio.write(a, 1)

        #print (r)

        self.radio.startListening();
        #ricevi stato
        started_waiting_at = self.millis()
        timeout = False
        while (not self.radio.available()) and (not timeout):
            if (self.millis() - started_waiting_at) > 300:
                timeout = True
        if timeout:
            print('failed, response timed out.')
            return None
        else:
            lend = self.radio.getDynamicPayloadSize()
            if(lend == 0):
                print("errore rx")
            else:
                stato_nodo = {}
                receive_payload = self.radio.read(lend)
                if receive_payload[0] == 0xA2:
                    stato_nodo['Tipo'] = receive_payload[1];
                    if (receive_payload[1]==5):
                        stato_nodo['ch1b'] = receive_payload[2];
                        stato_nodo['ch2b'] = receive_payload[3];
                        stato_nodo['ch3b'] = receive_payload[4];
                        stato_nodo['ch4b'] = receive_payload[5];
                        stato_nodo['ch1d'] = receive_payload[6];
                        stato_nodo['ch2d'] = receive_payload[7];
                        stato_nodo['ch3d'] = receive_payload[8];
                        stato_nodo['ch4d'] = receive_payload[9];
                        return stato_nodo
                    else:
                        return stato_nodo
        return None

    def get_stato_nodi(self,nodi):
        lista_stato_nodi = {}
        """
        while nodi:
            item = nodi.pop()
            print('-------')
            print(item)
            lista_stato_nodi[item] = self.get_stato_nodo(item)
            time.sleep(1)
        return lista_stato_nodi
        """
        for nodo in nodi:
            try:
                self.list1Lock.acquire()
                a = None
                for i in range(3): #range(2):
                    a = self.get_stato_nodo(nodo)
                    if(a!=None):
                        print (nodo + "  ;   " + str(i))
                        break
                lista_stato_nodi[nodo] = a
                #time.sleep(0.05)
            finally:
                self.list1Lock.release()
        return lista_stato_nodi
        

    def get_tipo_nodo(self,nodo):
        a=self.get_stato_nodo(nodo)
        if(a!=None):
            return a['Tipo']


    def send_stato_command(self,nodo, datijson):
        ch1b = 0;
        ch2b = 0;
        ch3b = 0;
        ch4b = 0;
        if(datijson['ch1b']):
            ch1b = 1;
        if(datijson['ch2b']):
            ch2b = 1;
        if(datijson['ch3b']):
            ch3b = 1;
        if(datijson['ch4b']):
            ch4b = 1;

        ch1d = int(datijson['ch1d'])
        ch2d = int(datijson['ch2d'])
        ch3d = int(datijson['ch3d'])
        ch4d = int(datijson['ch4d'])

        self.radio.stopListening();
        a = int(nodo, 16) #hex(int(nodo, 16))
        self.radio.openWritingPipe(a)
        self.radio.openReadingPipe(1,RF24module.add_cordinatore)      #Mio cordinatore !

        playload = [0xE0, ch1b,ch2b,ch3b,ch4b,ch1d,ch2d,ch3d,ch4d]
        a = "".join(map(chr, playload))
        r = self.radio.write(a, 1)

        #print (r)

        self.radio.startListening();




    def try_test_trasmitting(self, nodo):
        #to int
        a = int(nodo, 16) #hex(int(nodo, 16))
        #test trasmitting
        self.radio.openWritingPipe(a)
        send_payload = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ789012"
        self.radio.stopListening();
        self.radio.write( send_payload, len(send_payload) )
        self.radio.startListening();
        print("trasmesso!")

    def test_iswork(self):
        print("----------------^^^^^^^^^^^^^^^^^^-----------------------")
        self.radio.printDetails()


if __name__ == "__main__":
    while True:
        test = RF24module()
        """
        nodo = test.find_nodo()
        if(nodo != None):
            while True:
                print(nodo) 
                time.sleep(5)
                test.try_test_trasmitting(nodo)
        time.sleep(15)
        """
        nodia= ['ff000aa020','ff000aa021']
        #nodia= ['ff000aa020','ff000aa020']
        stato_nodi = test.get_stato_nodi(nodia)
                
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        
        print(stato_nodi)
        time.sleep(5)