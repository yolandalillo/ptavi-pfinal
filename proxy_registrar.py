#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from uaclient import log
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import socket
import socketserver
import json


class proxy(ContentHandler):
    def __init__(self):
        self.dic = {
		"server": ["name","ip","puerto"],
		"database": ["path", "passwdpath"],
		"log":["path"],
		
         }
        self.config = {}

    def startElement(self,name,attrs):
        if name in self.dic:
            for atribute in self.dic[name]:
                self.config[name+"_"+atribute] = attrs.get(atribute, "")

    def get_tags(self):
        return self.config

class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    dic_registrados = {}

    def json2registered(self): 
# Abrir fichero y obtener diccionario.
        with open(CONFIG["database_passwdpath"],"r") as file_json:
            self.dicc_usuarios = json.load(file_json)
            print(self.dicc_usuarios)
    def register2json(self):
        json.dump(self.dic_registrados, open(CONFIG["database_path"],"w"))
	        	
if __name__ == "__main__":
    """
    Programa principal
    """
    CONFIG = sys.argv[1]

    try:
        print("Server MiServidor listening at port 5555...")
    except IndexError:
    	sys.exit("Usage: python proxy_registrar.py config")

# Parse del fichero XML.
    parser = make_parser()
    cHandler = proxy()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))
    lista = cHandler.get_tags()
    print(lista)

