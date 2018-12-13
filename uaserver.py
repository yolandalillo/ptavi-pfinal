#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socketserver
import os


try:
    CONFIG = sys.argv[1] #Fichero XML
except (IndexError, ValueError):
    sys.exit("Usage: python3 uaserver.py config")

