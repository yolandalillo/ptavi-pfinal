#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa para un proxy."""

import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import socket
import socketserver
import json
from uaclient import log
import hashlib
import time
import random


class proxy(ContentHandler):
    """Fichero XML del proxy."""

    def __init__(self):
        """Definicion del diccionario con los datos del XML del proxy."""
        self.dic = {"server": ["name", "ip", "puerto"],
                    "database": ["path", "passwdpath"],
                    "log": ["path"],
                    }
        self.config = {}

    def startElement(self, name, attrs):
        """Guarda los atributos."""
        if name in self.dic:
            for atribute in self.dic[name]:
                self.config[name+"_"+atribute] = attrs.get(atribute, "")

    def get_tags(self):
        """Devuelve los atributos."""
        return self.config


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Clase para un servidor SIP."""

    dic_usuarios = {}
    nonce = {}

    def json_pass(self):
        """Crea fichero de las contraseñas ."""
        try:
            with open(PASSWD_PATH, "r") as file_json:
                self.dic_passwd = json.load(file_json)
        except FileNotFoundError:
                self.dic_passwd = {}

    def register_pass(self):
        """Introduce contraseñas en el json."""
        with open(PASSWD_PATH, "w") as file_json:
            json.dump(self.dic_passwd, file_json, sort_keys=True, indent=4)

    def json2registered(self):
        """Crea fichero json y lo metemos dentro del diccionario."""
        try:
            with open(DATABASE, "r") as file_json:
                self.dic_usuarios = json.load(file_json)
        except FileNotFoundError:
            self.dic_usuarios = {}

    def register2json(self):
        """Introduce usuario en el json."""
        with open(DATABASE, "w") as file_json:
            json.dump(self.dic_usuarios, file_json, sort_keys=True, indent=4)

    def borrar_resgistrados(self):
        """Para borrar los usuarios registrados."""
        del_list = []
        for usuarios in self.dic_usuarios:
            if self.dic_usuarios[usuarios]["expires"] <= time.time():
                del_list.append(usuarios)
        for usuarios in del_list:
            del self.dic_usuarios[usuarios]

    # Codigos de respuesta.
    def ack(self, usuarios):
        """Codigo de respuesta ack."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            destination = usuarios.split()[1][4:]
            ip_port = (self.dic_usuarios[destination]['addr'],
                       int(self.dic_usuarios[destination]['port']))
            sock.connect(ip_port)
            texto = add_header(usuarios)
            sock.send(bytes(texto, 'utf-8'))
            try:
                recv = sock.recv(1024).decode('utf-8')
                print(recv)
            except socket.timeout:
                pass

    def register(self, usuarios):
        """Codigo de respuesta register."""
        c_usuarios = usuarios.split()  # Sacamos informacion del usuario.
        print(c_usuarios)
        usuario_port = c_usuarios[1].split(':')[2]
        usuario_name = c_usuarios[1].split(':')[1]
        usuario_ip, usuario_exp = self.client_address[0], c_usuarios[4]
        # Controlando el tiempo.
        time_exp = int(usuario_exp) + time.time()
        str_exp = time.time()
        usuarios.split()
        if usuarios.split()[0] == 'REGISTER' and len(usuarios.split()) == 5:
            if usuario_name not in self.dic_usuarios:
                self.nonce[usuario_name] = str(random.randint(0, 999999999999))
                to_send = ("SIP/2.0 401 Unauthorized\r\nWWW-Authenticate: " +
                           "Digest nonce=" +
                           self.nonce[usuario_name] + "\r\n\r\n")
            else:
                to_send = ("SIP/2.0 200 OK" + "\r\n\r\n")
            self.wfile.write(bytes(to_send, 'utf-8'))
            log("send" + usuario_ip + usuario_port + to_send, FILELOG)

        elif usuarios.split()[0] == 'REGISTER' and len(usuarios.split()) == 8:
            comprobar = c_usuarios[7].split('=')[1]
            contrasena = self.dic_passwd[usuario_name]["passwd"]
            variable = hashlib.md5()
            variable.update(bytes(contrasena, 'utf-8'))
            variable.update(bytes(self.nonce[usuario_name], 'utf-8'))
            if variable.hexdigest() == comprobar:
                self.dic_usuarios[usuario_name] = {'addr': usuario_ip,
                                                   'expires': str_exp,
                                                   'port': usuario_port,
                                                   'time': time_exp,
                                                   }
                to_send = ("SIP/2.0 200 OK" + "\r\n\r\n")
            else:
                to_send = ("ERROR: Contraseña incorrecta")
        else:
            to_send = ("SIP/2.0 404 User Not Found: usuario no registrado" +
                       "\r\n\r\n")

        self.wfile.write(bytes(to_send, 'utf-8'))
        log("send" + usuario_ip + usuario_port + to_send, FILELOG)
        self.register2json()

    def bye(self, usuarios):
        """Codigo de respuesta bye."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                destination = usuarios.split()[1][4:]
                ip_port = (self.dic_usuarios[destination]['addr'],
                           int(self.dic_usuarios[destination]['port']))
                sock.connect(ip_port)
                texto = add_header(usuarios)
                sock.send(bytes(texto, 'utf-8'))
                recv = sock.recv(1024).decode('utf-8')
            except (ConnectionRefusedError, KeyError):
                recv = ""
                self.wfile.write(bytes("SIP/2.0 404 User Not Found\r\n\r\n",
                                       'utf-8'))
        if recv == ("SIP/2.0 200 OK" + "\r\n\r\n"):
            texto = add_header(recv)
            self.socket.sendto(bytes(texto, 'utf-8'), self.client_address)

    def invite(self, usuarios):
        """Codigo de respuesta invite."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            destination = usuarios.split()[1][4:]
            try:
                ip_port = (self.dic_usuarios[destination]['addr'],
                           int(self.dic_usuarios[destination]['port']))
                sock.connect(ip_port)
                texto = add_header(usuarios)
                sock.send(bytes(texto, 'utf-8'))
                recv = sock.recv(1024).decode('utf-8')
            except (ConnectionRefusedError, KeyError):
                recv = ""
                self.wfile.write(bytes("SIP/2.0 400 Bad Request\r\n\r\n",
                                       'utf-8'))

        if recv.split('\r\n')[0:3] == ["100", "180", "200"]:
            texto = add_header(recv)
            print(texto)
            self.socket.sendto(bytes(texto, 'utf-8'), self.client_address)
        try:
            if recv.split()[1] and recv.split()[1] == "480":
                texto = add_header(recv)
                self.socket.sendto(bytes(texto, 'utf-8'), self.client_address)
        except IndexError:
            pass

    def handle(self):
        """Cada vez que un cliente envia una peticion se ejecuta."""
        usuarios = self.request[0].decode('utf-8')
        c_addr = (self.client_address[0], str(self.client_address[1]))
        log("recv" + c_addr[0] + c_addr[1] + usuarios, FILELOG)
        unallow = ["CANCEL", "OPTIONS", "SUSCRIBE", "NOTIFY", "PUBLISH",
                   "INFO", "PRACK", "REFER", "MESSAGE", "UPDATE"]
        print(usuarios)
        method = usuarios.split()[0]
        self.json2registered()
        self.json_pass()
        self.borrar_resgistrados()
        if method == "REGISTER":
            self.register(usuarios)
        elif method == "INVITE":
            self.invite(usuarios)
        elif method == "ACK":
            self.ack(usuarios)
        elif method == "BYE":
            self.bye(usuarios)
        elif method in unallow:
            to_send = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
            log("send" + c_addr[0] + c_addr[1] + to_send, FILELOG)
            self.wfile.write(bytes(to_send, 'utf-8'))
        else:
            to_send = "SIP/2.0 400 Bad Request\r\n\r\n"
            log("send" + c_addr[0] + c_addr[1] + to_send,  FILELOG)
            self.wfile.write(bytes(to_send, 'utf-8'))


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
        SERVERPORT = lista["server_puerto"]

    except IndexError:
        sys.exit("Usage: python proxy_registrar.py config")

    SERV = socketserver.UDPServer(SERVER, SIPRegisterHandler)
    print("Server " + NAME + " listening at port " + SERVERPORT + "...")
    log("Server" + NAME + " listening at port " + SERVERPORT + "...", FILELOG)
    try:
        SERV.serve_forever()
    except KeyboardInterrupt:
        sys.exit("\r\n Proxy finalizado")
