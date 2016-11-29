import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import webapp
import RF24module
import time
import database

global radioNodi
global dbn



class GetListaNodiSettingHandler(tornado.web.RequestHandler):
    def get(self):
        #***************************************
        #***************************************
        #***************************************
        #recupera nodi dal server e inviala al main.html
        #leggi il setting dal database
        #***************************************
        #***************************************
        #***************************************
        #test --->
        """
        nodo_new = {
            "55754":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"false","ch4":"true"}] , "stato" : [ { "ch1b" : "false" , "ch2b" : "true" , "ch3b" : "true" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "20" } ]   },
            "55753":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"true","ch4":"true"}] , "stato" : [ { "ch1b" : "true" , "ch2b" : "false" , "ch3b" : "true" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "20" } ]   },
            "55752":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"true","ch4":"true"}] , "stato" : [ { "ch1b" : "true" , "ch2b" : "false" , "ch3b" : "false" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "100" } ]   },


                    }
        """
        nodi_new = webapp.dbn.Read_Lista_Nodi_return_JSON()
        #aggiungi ordine
        #nodo_new['OrdineNodi'] = ['addrss_A','addrss_B']

        numberorder = []
        for item in nodi_new:
            numberorder.append(nodi_new[item]['Ordine'])
        numberorder.sort()

        list_Address = []
        for idn in numberorder:
            for item in nodi_new:
                if(nodi_new[item]['Ordine'] == idn):
                    list_Address.append(item)

        nodi_new['OrdineNodi'] = list_Address
        self.write(json.dumps(nodi_new)) 


class AggiungiNodiHandler(tornado.web.RequestHandler):
    def get(self):
        #***************************************
        #***************************************
        #***************************************
        #recupera dati con il cordinatore dal wireless nodi
        #***************************************
        #***************************************
        #***************************************
        #test --->
        nodo = webapp.radioNodi.find_nodo()
        #verifica se gia ce nel daatabase
        a = webapp.dbn.Is_AddressNodo_inDataabase(nodo)
        if(a==False):        
            time.sleep(0.1)
            nodo_new = {}
            if (nodo == None):            
                self.write(json.dumps(nodo_new)) 
            else:
                #richiede descrizione nodo
                tipo = webapp.radioNodi.get_tipo_nodo(nodo)
                if (tipo == 5):
                    #un dimmer (x ora solo dimmer)
                    nodo_new = { nodo :{"Tipo": str(tipo), "Descrizione":"Dimmer"}}
                    #aggiungi in database
                    webapp.dbn.Aggiungi_Nodo_inDatabase(nodo, str(tipo))
                else:
                    nodo_new = {}
                    self.write(json.dumps(nodo_new)) 

                #nodo_new = {"55754":{"Tipo":"5", "Descrizione":"Dimmer"}}
                self.write(json.dumps(nodo_new)) 
        else:
            print("Nodo Gia esiste!")
            nodo_new = { "Errore" : "Nodo Esiste" }
            self.write(json.dumps(nodo_new))




class RimuoviNodoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        #***************************************
        #***************************************
        #***************************************
        #rimuovi nodo dal database
        #***************************************
        #***************************************
        #***************************************
        #test --->
        webapp.dbn.Remove_Nodo(str(data["Nodo"]))
        #print('remove: ' + data['Nodo'])


class OrdineNodiHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        #***************************************
        #***************************************
        #***************************************
        #ordini nodi nel database
        #***************************************
        #***************************************
        #***************************************
        #test --->
        webapp.dbn.Set_Ordine_Nodi(data["Nodi"])


class FunzionamentoNodoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        #***************************************
        #***************************************
        #***************************************
        #Funzionamento dimmer,  Setting del nodo da impostare nel database
        #***************************************
        #***************************************
        #***************************************
        #test --->
        nodi_new = webapp.dbn.Write_Setting_Nodo(str(data["Nodo"]),str(data["checkbox"]),str(data["value"]))

        #print(data)

        

        