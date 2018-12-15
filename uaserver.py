#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socketserver
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time
# Intentar importart la clase desde uaclient

CONFIG = sys.argv[1]  # FicheroXML.


class XMLserver(ContentHandler):
    def __init__(self):
        self.diccionario = {
            "account": ["username", "passwd"],
            "uaserver": ["ip", "puerto"],
            "rtpaudio": ["puerto"],
            "regproxy": ["ip", "puerto"],
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


class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):
            while 1:
                line = self.rfile.read()
                if not line:
                    break
                print("El proxy nos manda " + line.decode('utf-8'))
                lista = line.decode('utf-8')
                print(lista.split())
                METODO = lista.split(' ')[0]
                if METODO == "INVITE":
                    mensaje = "SIP/2.0 200 OK" + '\r\n' + '\r\n'
                    solicitud = mensaje
                    solicitud += "Content-Type: application/sdp\r\n\r\n"
                    solicitud += "v=0\r\n" + "o=" + account_us + ' '
                    solicitud += uaserver_ip + "\r\n" + "s=misession\r\n"
                    solicitud += "t=0\r\n" + "m=audio " + PORTRTP
                    solicitud += " RTP\r\n\r\n"
                    self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n"
                                     b"SIP/2.0 180 Ring" + b"\r\n")
                    self.wfile.write(bytes(peticion, 'utf-8'))
                elif METODO == "ACK":
                    aEjecutar = "./mp32rtp -i " + SERVER + " -p 23032 < "
                    aEjecutar += FILEAUDIO
                    print("Vamos a ejecutar", aEjecutar)
                    os.system(aEjecutar)
                elif METODO == "BYE":
                    self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
                elif METODO != "REGISTER" or "INVITE" or "ACK":
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed" + b"\r\n")
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request" + b"\r\n")


if __name__ == "__main__":
    """
    Programa principal
    """

    if len(sys.argv) ==2:
    # Parse el fichero XML.
        parser = make_parser()
        cHandler = XMLserver()
        parser.setContentHandler(cHandler)
        parser.parse(open(CONFIG))
        lista = cHandler.get_tags()
        print(lista)
# Variables necesarias.
        USERNAME = lista['account_username']
        USERPASSW = lista['account_passwd']
        SERVER = lista['uaserver_ip']
        PORT = lista['uaserver_puerto']
        AUDIOPORT = lista['rtpaudio_puerto']
        FILEAUDIO = lista['audio_path']
        FILELOG = lista['log_path']
        IPPROXY = lista['regproxy_ip']
        PUERTOPROXY = lista['regproxy_puerto']
        PORTRTP = lista['rtpaudio_puerto']

        serv_servidor = socketserver.UDPServer((SERVER, int(PORT)), EchoHandler)
        print("Listening")
        serv_servidor.serve_forever()


    else:
        sys.exit("Usage: python3 uaserver.py config")


   