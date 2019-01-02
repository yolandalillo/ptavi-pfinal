#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from uaclient import log
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import socket
import socketserver
import json
from uaclient import log


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
    """ Clase para un servidor SIP. """

    dic_usuarios= {}

    def json2registered(self): 
# Abrir fichero y obtenemos diccionario.
        try:
            with open(DATABASE,"r") as file_json:
                self.dic_usuarios = json.load(file_json)
       	except:
            self.dic_usuarios = {}

    def register2json(self):
    # Introducimos usuario en el fichero JSON.
        with open(DATABASE,"w") as file_json:
            json.dump(self.dic_usuarios, file_json, sort_keys=True, indent=4)

    def expired(self):
    # Para borrar los usuarios registrados.
        del_list = []
        actual = time.strftime( '%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        for usuarios in self.dic_usuarios:
            if self.dic_usuarios[usuarios]["expires"] <= actual:
                del_list.append(usuarios)
        for usuarios in del_list:
            del self.dic_usuarios[usuarios]





if __name__ == "__main__":
    """
    Programa principal
    """

    try:
        CONFIG = sys.argv[1]
        # Parse del fichero XML.
        parser = make_parser()
        cHandler = proxy()
        parser.setContentHandler(cHandler)
        parser.parse(open(CONFIG))
        lista = cHandler.get_tags()
        print(lista)
    
        NAME = lista["server_name"]
        SERVER = lista["server_ip"], int(lista["server_puerto"])
        FILELOG = lista["log_path"]
        DATABASE = lista["database_path"]
        PASSWD_PATH = lista["database_passwdpath"]
        PROXY_HEADER = "Via: SIP/2.0/UDP {}:{}".format(SERVER[0], SERVER[1])

    except IndexError:
    	sys.exit("Usage: python proxy_registrar.py config")

    SERV = socketserver.UDPServer(SERVER, SIPRegisterHandler)
    print("Server " + NAME + " listening at port 5555...")
    #FILELOG( "Server " + NAME + " listening at port 5555...")
    try:
        SERV.serve_forever()
    except KeyboardInterrupt:
        sys.exit("\r\nClosed")









