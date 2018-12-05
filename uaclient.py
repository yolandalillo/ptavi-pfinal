#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

try:
    CONFIG = sys.argv[1] #Fichero XML
    METODO = sys.argv[2] #Metodo SIP
    OPCION = sys.argv[3] #Parametro opcional
except (IndexError, ValueError):
    sys.exit("Usage: python3 uaclient.py config method option")


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""
    def handle(self):
        while 1:
            if METODO == 'REGISTER':

            if METODO == 'INVITE':

            if METODO == 'ACK':

            if METODO == 'BYE'


if __name__ == "__main__":