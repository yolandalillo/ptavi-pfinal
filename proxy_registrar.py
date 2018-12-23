#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from uaclient import log
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class proxy(ContentHandler):
	def __init__(self):
		self.dic = {
			"server": ["name","ip","puerto"],
			"database": ["path", "passwdpath"],
			"log":["path"],
		}
		self.config = {}
	def start(self,name,attrs):
		if name in self.dic:
			for atribute in self.dic[name]:
				self.conf[name+"_"+atribute] = attrs.get(atribute,"")
	def get_tags(self):
		return self.config

	
	
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
	chandler = proxy
	parser.setContentHandler(chandler)
	parser.parse(open(CONFIG))
	lista = ucharler.get_tags()
	print(lista)

