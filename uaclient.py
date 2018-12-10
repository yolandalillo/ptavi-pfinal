#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

try:
    CONFIG = sys.argv[1] #Fichero XML
    METODO = sys.argv[2] #Metodo SIP
    OPCION = sys.argv[3] #Parametro opcional
except (IndexError, ValueError):
    sys.exit("Usage: python3 uaclient.py config method option")

def __init__(self):
    self.diccionario = {
        "account": ["username", "passwd"],
        "uaserver": ["ip", "puerto"],
        "rtpaudio": ["puerto"],
        "log": ["path"],
        "audio": ["path"],
    }


if __name__ == "__main__":