#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time

class ficheroXML(ContentHandler):
    def __init__(self):
        self.diccionario = {
            "account": ["username", "passwd"],
            "uaserver": ["ip", "puerto"],
            "rtpaudio": ["puerto"],
            "log": ["path"],
	    "regproxy": ["ip","puerto"],
            "audio": ["path"],
        }
        self.lista = []
        self.etiquetas = self.diccionario.keys() #Para obtener las claves del diccionario.

    def startElement(self, name, attrs):
        dic_etiqueta = {}
        if name in self.etiquetas:
            dic_etiqueta['etiqueta'] = name
            for atributo in self.diccionario[name]:
                dic_etiqueta[atributo] = attrs.get(atributo, "")
            self.lista.append(dic_etiqueta)

    def get_tags(self):
        return self.lista

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

    parser = make_parser()
    cHandler = ficheroXML()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))
    lista = cHandler.get_tags()
    for dic in lista:
        print(dic)




