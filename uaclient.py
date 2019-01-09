#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa para un cliente."""

import sys
import socket
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time
import hashlib


class ficheroXML(ContentHandler):
    """Fichero XML del cliente que es igual en el servidor."""

    def __init__(self):
        """Definicion del diccionario con los datos del XML."""
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
        """Guarda los atributos."""
        if name in self.diccionario:
            for atribute in self.diccionario[name]:
                self.config[name+"_"+atribute] = attrs.get(atribute, "")

    def get_tags(self):
        """Devuelve los atributos."""
        return self.config


def log(message, FILELOG):
    """Crea el fichero log."""
    time_actual = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))
    fich = open(FILELOG, "a")
    fich.write(time_actual + ' ' + message + '\r\n')
    fich.close()


if __name__ == "__main__":
    """
    Programa principal
    """
    try:
        CONFIG = sys.argv[1]  # FicheroXML.
        METODO = sys.argv[2]  # Metodo SIP.
        OPCION = sys.argv[3]  # Parametro opcional
    except (IndexError, ValueError):
        sys.exit("Usage: python3 uaclient.py config method option")


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
    FILEAUDIO = lista['audio_path']
    FILELOG = lista['log_path']
    IPPROXY = lista['regproxy_ip']
    PUERTOPROXY = lista['regproxy_puerto']
    PORTRTP = lista['rtpaudio_puerto']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IPPROXY, int(PUERTOPROXY)))
            log("Starting...", FILELOG)
            if METODO == 'BYE':
                LINE = METODO + " sip:" + OPCION + " SIP/2.0\r\n"
                print(LINE)
                log("Sent to " + SERVER + ": " + PORT + ":" + LINE, FILELOG)
                my_socket.send(bytes(LINE, 'utf-8'))
                data = my_socket.recv(1024)
                print(data.decode('utf-8'))
                log("Received from: " + SERVER + ":" +
                    PORT + ":" + str(data), FILELOG)  # Arreglar str(data).

            elif METODO == 'REGISTER':
                LINE = METODO + ' sip:' + USERNAME +\
                       ':' + PORT + ' SIP/2.0\r\n'
                LINE += "Expires: " + OPCION + "\r\n"
                print(LINE)
                log("Sent to " + SERVER + ":" +
                    PORT + ":" + ' '.join(LINE.split()), FILELOG)
                my_socket.send(bytes(LINE, 'utf-8'))
                data = my_socket.recv(1024)
                print(data.decode('utf-8'))
                log("Received from " + SERVER + ":" + PORT
                    + ": " + ' '.join(LINE.split()), FILELOG)

                data = data.decode('utf-8').split("\r\n")
                datos = " ".join(data)
                log("Received from " + IPPROXY + " " +
                    PUERTOPROXY + " " + datos, FILELOG)
                if data[0] == "SIP/2.0 401 Unauthorized":
                    variable = hashlib.md5()
                    nonce = data[1].split("=")[-1]
                    variable.update(bytes(USERPASSW, 'utf-8'))
                    variable.update(bytes(nonce, 'utf-8'))
                    LINE += "Authorization: Digest response=" +\
                            variable.hexdigest() + "\r\n"
                    print("Enviando: \r\n" + LINE)
                    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
                    listadatos = LINE.split('\r\n')
                    datos = " ".join(listadatos)
                    log("Sent_to " + IPPROXY + " " + PUERTOPROXY +
                        " " + datos, FILELOG)
                    data = my_socket.recv(1024)
                    print("Recibido: \r\n", data.decode('utf-8'))

            elif METODO == 'INVITE':
                LINE = "INVITE " + "sip:" + OPCION + " SIP/2.0\r\n"
                LINE += "Content-Type: application/sdp\r\n\r\n"
                LINE += "v=0\r\n" + "o=" + USERNAME + " " + SERVER + " \r\n"
                LINE += "s=misesion" + "\r\n" + "t=0" + "\r\n"
                LINE += "m=audio " + PORTRTP + " RTP" + "\r\n"
                print(LINE)
                log("Sent to" + SERVER + ":" + PORT + ":" + USERNAME, FILELOG)
                my_socket.send(bytes(LINE, 'utf-8'))
                data = my_socket.recv(1024)
                print(data.decode('utf-8'))
                log("Received from: ", FILELOG)

                data = data.decode('utf-8').split("\r\n")
                datos = " ".join(data)
                log("Received from " + IPPROXY + " " + PUERTOPROXY +
                    " " + datos, FILELOG)
                if data[0] == "SIP/2.0 100 Trying":
                    # Metodo de asentimiento. ACK sip:receptor SIP/2.0
                    METODO = 'ACK'
                    LINE = METODO + ' sip:' + OPCION + ' SIP/2.0\r\n'
                    print("Enviando: \r\n" + LINE)
                    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
                    listadatos = LINE.split('\r\n')
                    datos = " ".join(listadatos)
                    log("Sent_to " + IPPROXY + " " + PUERTOPROXY +
                        " " + datos, FILELOG)
                    # Envio RTP
                    # aEjecutar es un string con
                    # lo que se ha de ejecutar en la shell
                    aEjecutar = "./mp32rtp -i " + SERVER + " -p 23032 < "
                    aEjecutar += FILEAUDIO
                    print("Vamos a ejecutar", aEjecutar)
                    os.system(aEjecutar)

            else:
                sys.exit('Method not found')
                log("Error: Method not found", FILELOG)
            print("Terminando socket...")
            log("Finishing", FILELOG)

    except ConnectionRefusedError:
        print("Error de conexión")
