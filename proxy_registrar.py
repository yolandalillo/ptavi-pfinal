#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
try:

    CONFIG = sys.argv[1]

except IndexError:
    print("Usage: python proxy_registrar.py config")

print("Server MiServidor listening at port 5555")