#!/usr/bin/python3
 # -*- coding: utf-8 -*-
 
import sys
import socket
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
 
class ficheroXML(ContentHandler):
    def __init__(self):
        self.diccionario = {
            "account": ["username", "passwd"],
            "uaserver": ["ip", "puerto"],
            "rtpaudio": ["puerto"],
	    "regproxy":["ip","puerto"],
            "log": ["path"],
            "audio": ["path"],
        }
        self.config = {}
 
    def startElement(self, name, attrs):
        if name in self.diccionario:
            for atribute in self.diccionario[name]:
                self.config[name+"_"+atribute] = attrs.get(atribute, "")
 
    def get_tags(self):
        return self.config

def log(message):
     #Fichero log
     fich.write(time.strftime('%Y%m%d%H%M%S '))
     fich.write(message +"\r\n")

if __name__ == "__main__":
     """
     Programa principal
     """
     try:
        CONFIG = sys.argv[1] #FicheroXML
        METODO = sys.argv[2]  # Metodo SIP
        OPCION = sys.argv[3]  # Parametro opcional
     except (IndexError, ValueError):
        sys.exit("Usage: python3 uaclient.py config method option")

	#Parse el fichero XML
     parser = make_parser()
     cHandler = ficheroXML()
     parser.setContentHandler(cHandler)
     parser.parse(open(CONFIG))

     lista = cHandler.get_tags()
     print(lista)

     USERNAME = lista['account_username']
     SERVER = lista['uaserver_ip']
     PORT = lista['uaserver_puerto']
    

	




    


