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
            "log": ["path"],
            "audio": ["path"],
        }
        self.datos = []
        self.etiquetas = self.diccionario.keys() #Para obtener las claves del diccionario.

    def startElement(self, name, attrs):
        dic_etiqueta = {}
        if name in self.etiquetas:
            dic_etiqueta['etiqueta'] = name
            for atributo in self.diccionario[name]:
                dic_etiqueta[atributo] = attrs.get(atributo, "")
            self.datos.append(dic_etiqueta)

    def get_tags(self):
        return self.datos




if __name__ == "__main__":
    """
    Programa principal
    """
    try:
        CONFIG = sys.argv[1] #FicheroXML
        METODO = sys.argv[2]  # Metodo SIP
        OPCION = sys.argv[3]  # Parametro opcional
        parser = make_parser()
        cHandler = ficheroXML()
        parser.setContentHandler(cHandler)
        parser.parse(open(sys.argv[1]))
        datos = cHandler.get_tags()
        print(datos)
        valor = diccionario_gets(rtpaudio)
        print(valor)
    except (IndexError, ValueError):
        sys.exit("Usage: python3 uaclient.py config method option")