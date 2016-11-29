import tornado.ioloop
import tornado.web
from tornado import websocket
import json

import AggiungiNodi
import Nodi
import RF24module
import database




radioNodi = RF24module.RF24module()
dbn = database.nodi_database()



cl = []     #websocket connessioni

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('WebSite1/nodi.html')



class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('WebSite1/main.html')






#        for c in cl:
#           c.write_message(data)

class SocketHandler(websocket.WebSocketHandler):
    nodolast_temp = None

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)
        #self.write_message("HELLO WEBSOCKET")

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):        
        #legge comando e invialo ai nodi
        #attendi risposta dai nodi e invia stato nodi al server web
        #print "Client %s received a message : %s" % (self.id, message)
        #print("messaggio websocket")
        data = json.loads(message)
        if (data.has_key("coamando")):
            if (data.has_key("nodo")):
                
                print("TESTTTTTTTTTTTTT NODO 1")

                jsonnodo = radioNodi.get_stato_nodo(data['nodo'])
                if(jsonnodo!= None):
                    jsonnodo['nodo'] = data['nodo']
                    jsonnodo['disable'] = 'false'
                    for c in cl:
                        c.write_message(json.dumps(jsonnodo))

                    print("TESTTTTTTTTTTTTT NODO --> ABILIATTO 1")

                else:
                    print("TESTTTTTTTTTTTTT NODO --> DISABILIATTO 1")

                    jsonnodo = {}
                    jsonnodo['nodo'] = data['nodo']
                    jsonnodo['disable'] = 'true'
                    for c in cl:
                        c.write_message(json.dumps(jsonnodo))

            else:
                if(data['coamando'] == 'get_stato_nodo'):
                    if(SocketHandler.nodolast_temp!=None):

                        print("TESTTTTTTTTTTTTT NODO 2")

                        jsonnodo = radioNodi.get_stato_nodo(SocketHandler.nodolast_temp)
                        if(jsonnodo!= None):
                            jsonnodo['nodo'] = SocketHandler.nodolast_temp
                            jsonnodo['disable'] = 'false'
                            for c in cl:
                                c.write_message(json.dumps(jsonnodo))
    
                            print("TESTTTTTTTTTTTTT NODO --> ABILIATTO 2")

                        else:
                            jsonnodo = {}
                            jsonnodo['nodo'] = SocketHandler.nodolast_temp
                            jsonnodo['disable'] = 'true'
                            for c in cl:
                                c.write_message(json.dumps(jsonnodo))

                            print("TESTTTTTTTTTTTTT NODO --> DISABILIATTO 2")

        else:
            if (data.has_key("nodo")):
                if(data.has_key("stato")):

                    print("*****************")
                    if(Nodi.store_setting_nodi != None):
                        if(Nodi.store_setting_nodi.has_key(data["nodo"])):
                            
                            if(Nodi.store_setting_nodi[data["nodo"]]['funzionamento'][0]['ch1'] == 'false'):
                                data["stato"]['ch1d'] = 100
                            if(Nodi.store_setting_nodi[data["nodo"]]['funzionamento'][0]['ch2'] == 'false'):
                                data["stato"]['ch2d'] = 100
                            if(Nodi.store_setting_nodi[data["nodo"]]['funzionamento'][0]['ch3'] == 'false'):
                                data["stato"]['ch3d'] = 100
                            if(Nodi.store_setting_nodi[data["nodo"]]['funzionamento'][0]['ch4'] == 'false'):
                                data["stato"]['ch4d'] = 100
                            
                    radioNodi.send_stato_command(data["nodo"], data["stato"])
                    SocketHandler.nodolast_temp = data["nodo"]

        




def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/main.html", HomeHandler),
        (r"/nodi.html", MainHandler),

        #json request --- Nodi.html----
        (r"/GetListaNodiSetting.json", AggiungiNodi.GetListaNodiSettingHandler),
        (r"/AggiungiNodi.json", AggiungiNodi.AggiungiNodiHandler),
        (r"/RimuoviNodo.json", AggiungiNodi.RimuoviNodoHandler),
        (r"/OrdineNodi.json", AggiungiNodi.OrdineNodiHandler),
        (r"/FunzionamentoNodo.json", AggiungiNodi.FunzionamentoNodoHandler),
        #json request --- main.html----
        (r"/GetListaNodi.json", Nodi.GetListaNodiHandler),
        (r"/GetNodo.json", Nodi.Get_funzionamento_nodoHandler),

        

        #websocket
        (r'/ws', SocketHandler),

	    (r'/WebSite1/js/(.*)', tornado.web.StaticFileHandler, {'path': '/home/app/WebSite1/js/'}),
	    (r'/WebSite1/css/(.*)', tornado.web.StaticFileHandler, {'path': '/home/app/WebSite1/css/'}),
	    (r'/WebSite1/image/(.*)', tornado.web.StaticFileHandler, {'path': '/home/app/WebSite1/image/'}),

    ], debug=True)



if __name__ == "__main__":    
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()