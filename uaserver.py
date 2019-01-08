#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socketserver
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from uaclient import ficheroXML
from uaclient import log


try:
    CONFIG = sys.argv[1]  # FicheroXML.
except(IndexError, ValueError):
        sys.exit("Usage: python3 uaserver.py config")


class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):
            while 1:
                log("Starting...", FILELOG)
                line = self.rfile.read()
                print("El proxy nos manda " + line.decode('utf-8'))
                lista = line.decode('utf-8')
                METODO = lista.split(" ")[0]
                if METODO == "INVITE":
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    break
                    log("Sent to" + SERVER + ":" + PORT + ":" + USERNAME, FILELOG)
                    log("Received from: ", FILELOG)
                elif METODO == "ACK":
                    aEjecutar = "./mp32rtp -i " + SERVER + " -p 23032 < "
                    aEjecutar += FILEAUDIO
                    print("Vamos a ejecutar", aEjecutar)
                    os.system(aEjecutar)
                    log("Sent to" + SERVER + ":" + PORT + ":" + USERNAME + aEjecutar, FILELOG)
                elif METODO == "BYE":
                    self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
                    log("Sent to" + SERVER + ":" + PORT + ":" + USERNAME, FILELOG)
                    log("Received from: ", FILELOG)
                elif METODO != ("REGISTER" or "INVITE" or "ACK"):
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed"
                                     + b"\r\n")
                    log("Error: Method Not Allowed", FILELOG)

                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request" + b"\r\n")
                    log("Error: Bad Request")
                if not line:
                    break
            log("Finishing", FILELOG)


if __name__ == "__main__":
    """
    Programa principal
    """

    # Parse el fichero XML.
    parser = make_parser()
    cHandler = ficheroXML()
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
    serv = socketserver.UDPServer((SERVER, int(PORT)), EchoHandler)
    print("Listening...")
    try:
        # Creamos el servidor.
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit("Servidor Finalizado")
