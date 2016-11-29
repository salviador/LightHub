import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import webapp

import database

global dbn
store_setting_nodi = None

class GetListaNodiHandler(tornado.web.RequestHandler):
    def get(self):
        global store_setting_nodi
        #***************************************
        #***************************************
        #***************************************
        #recupera nodi dal server e inviala al main.html
        #leggi stato dai nodi
        #***************************************
        #***************************************
        #***************************************
        #test --->
        """
        nodo_new = {
            "55754":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"true","ch4":"true"}] , "stato" : [ { "ch1b" : "false" , "ch2b" : "true" , "ch3b" : "true" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "20" } ]   },
            "55753":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"true","ch4":"true"}] , "stato" : [ { "ch1b" : "true" , "ch2b" : "false" , "ch3b" : "true" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "20" } ]   },
            "55752":{"Tipo":"5", "Descrizione":"Dimmer", "funzionamento" : [{"ch1":"false","ch2":"true","ch3":"true","ch4":"true"}] , "stato" : [ { "ch1b" : "true" , "ch2b" : "false" , "ch3b" : "false" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "100" } ]   },


                    }

        self.write(json.dumps(nodo_new)) 
        """
        nodi_new = webapp.dbn.Read_Lista_Nodi_return_JSON()
        #aggiungi ordine
        #nodo_new['OrdineNodi'] = ['addrss_A','addrss_B']
        store_setting_nodi = nodi_new
        print("##################################")
        print(store_setting_nodi)

        numberorder = []
        for item in nodi_new:
            numberorder.append(nodi_new[item]['Ordine'])
        numberorder.sort()

        list_Address = []
        for idn in numberorder:
            for item in nodi_new:
                if(nodi_new[item]['Ordine'] == idn):
                    list_Address.append(item)

        #ora leggi lo stato dei nodi dai sensori
        stato_nodi = webapp.radioNodi.get_stato_nodi(tuple(list_Address))

        
        for item in list_Address:

            nodi_new[item]['disable'] = 'true';

            if(stato_nodi.has_key(item)):
                if(stato_nodi[item] != None):
                    if(stato_nodi[item].has_key('Tipo')):
                        if(stato_nodi[item]['ch1b'] == 0):
                            nodi_new[item]['stato'][0]['ch1b'] = 'false'
                        else:
                            nodi_new[item]['stato'][0]['ch1b'] = 'true'

                        if(stato_nodi[item]['ch2b'] == 0):
                            nodi_new[item]['stato'][0]['ch2b'] = 'false'
                        else:
                            nodi_new[item]['stato'][0]['ch2b'] = 'true'

                        if(stato_nodi[item]['ch3b'] == 0):
                            nodi_new[item]['stato'][0]['ch3b'] = 'false'
                        else:
                            nodi_new[item]['stato'][0]['ch3b'] = 'true'

                        if(stato_nodi[item]['ch4b'] == 0):
                            nodi_new[item]['stato'][0]['ch4b'] = 'false'
                        else:
                            nodi_new[item]['stato'][0]['ch4b'] = 'true'

                        nodi_new[item]['stato'][0]['ch1d'] = str(stato_nodi[item]['ch1d'])
                        nodi_new[item]['stato'][0]['ch2d'] = str(stato_nodi[item]['ch2d'])
                        nodi_new[item]['stato'][0]['ch3d'] = str(stato_nodi[item]['ch3d'])
                        nodi_new[item]['stato'][0]['ch4d'] = str(stato_nodi[item]['ch4d'])

                        nodi_new[item]['disable'] = 'false';
                else:
                    nodi_new[item]['disable'] = 'true';


        nodi_new['OrdineNodi'] = list_Address
        
        #print ("####################")
        #print (nodi_new)
        #print ("----------------------")


        self.write(json.dumps(nodi_new)) 






class Get_funzionamento_nodoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        if (data.has_key("nodo")):
            dbnodo = webapp.dbn.Get_Nodo(data['nodo'])
            dbnodo['nodo'] = data['nodo']

            self.write(json.dumps(dbnodo)) 

