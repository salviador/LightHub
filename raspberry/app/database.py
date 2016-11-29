#!/usr/bin/env python
import MySQLdb


class nodi_database:
    def __init__(self):
        # open the database
        self.db = MySQLdb.connect('localhost','root', 'raspberry')
        self.cursor = self.db.cursor()
        """
        sql = "CREATE DATABASE IF NOT EXISTS NODI"
        self.cursor.execute(sql)
        """
        sql = "USE NODI"
        self.cursor.execute(sql)

        
        #crea database -Address Nodo- -Tipo- -Descrizione-
        self.cursor.execute("""create table IF NOT EXISTS nodi (
                address varchar(20) primary key not NULL ,
                tipo varchar(5),
                descrizione varchar(30),
                funzionamento_ch1 varchar(6),
                funzionamento_ch2 varchar(6),
                funzionamento_ch3 varchar(6),
                funzionamento_ch4 varchar(6),               
                stato_ch1b varchar(6),
                stato_ch2b varchar(6),
                stato_ch3b varchar(6),
                stato_ch4b varchar(6),
                stato_ch1d varchar(4),
                stato_ch2d varchar(4),
                stato_ch3d varchar(4),
                stato_ch4d varchar(4),
                ordine INT UNSIGNED)""")
        
        self.cursor.fetchall()
        self.db.commit()

        #self.cursor.execute("""insert into nodi values ('AAFF3360', '5', 'dimmer','false', 'false', 'false','false','false', 'false', 'false','false','10','10','10','10','0')""")

        self.cursor.fetchall()
        self.db.commit()

    def Is_AddressNodo_inDataabase(self,nodo):
        if(nodo != None):
            self.cursor.execute("select * from nodi where address='" + nodo + "'")
            result = self.cursor.fetchall()
            if (len(result) >= 1):
                return True
            else:
                return False
        return False

    def Aggiungi_Nodo_inDatabase(self,nodo,tipo):
        #prima cerca lordine massimo
        numero = 0
        self.cursor.execute("SELECT ordine from nodi ORDER BY ordine DESC LIMIT 1")
        result = self.cursor.fetchall()
        if (len(result) >= 1):
            numero = result[0][0]
            numero = numero + 1
      
        sql = "insert into nodi values ('%s' , '5' , 'dimmer','false', 'false', 'false','false','false', 'false', 'false','false','10','10','10','10', %d)" % (str(nodo), numero)
        self.cursor.execute(sql)
        self.cursor.fetchall()
        self.db.commit()

    def Read_Lista_Nodi_return_JSON(self):
        self.cursor.execute("select * from nodi ORDER BY ordine ASC")
        result = self.cursor.fetchall()
        nodi_json = {}
        if (len(result) >= 1):
            for item in result:
                nodi_json[item[0]] = {"Ordine": item[15] , "Tipo": item[1] , "Descrizione": item[2], "funzionamento" : [{"ch1":item[3],"ch2":item[4],"ch3":item[5],"ch4":item[6]}] , "stato" : [ { "ch1b" : "false" , "ch2b" : "true" , "ch3b" : "true" , "ch4b" : "true" ,  "ch1d" : "40" , "ch2d" : "80" , "ch3d" : "50" , "ch4d" : "20" } ]     }
            return nodi_json
        else:
            return {}

    def Write_Setting_Nodo(self, nodo, checkbox, value):
        namechackbox = ""
        if(checkbox == "Checkbox1"):
            namechackbox = "funzionamento_ch1"
        if(checkbox == "Checkbox2"):
            namechackbox = "funzionamento_ch2"
        if(checkbox=="Checkbox3"):
            namechackbox = "funzionamento_ch3"
        if(checkbox=="Checkbox4"):
            namechackbox = "funzionamento_ch4"

        sql = "UPDATE nodi SET %s='%s' WHERE address='%s'" % (namechackbox, value.lower(), str(nodo))
        self.cursor.execute(sql)
        self.cursor.fetchall()
        self.db.commit()

    def Remove_Nodo(self,nodo):
        sql = "DELETE FROM nodi WHERE address='%s'" % (str(nodo))
        self.cursor.execute(sql)
        self.cursor.fetchall()
        self.db.commit()

    def Set_Ordine_Nodi(self,nodi):
        i=0
        for item in nodi:
            sql = "UPDATE nodi SET ordine=%d WHERE address='%s'" % (i, item)
            self.cursor.execute(sql)
            self.cursor.fetchall()
            self.db.commit()
            i=i+1

    def Get_Nodo(self,nodo):
        self.cursor.execute("select * from nodi where address='" + nodo + "'")
        result = self.cursor.fetchall()
        nodi_json = {}
        for item in result:
            nodi_json['funzionamento'] = {"ch1":item[3],"ch2":item[4],"ch3":item[5],"ch4":item[6]}
            return nodi_json
        else:
            return {}




if __name__ == "__main__":
    dn = nodi_database()
    a = dn.Is_AddressNodo_inDataabase('AAF3360')
    print(a)
    dn.Aggiungi_Nodo_inDatabase('AA0000AAA','5')



