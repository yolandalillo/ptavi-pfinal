#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

try:
    CONFIG = sys.argv[1]
    METODO = sys.argv[2]
    OPCION = sys.argv[3]
except (IndexError, ValueError):
    sys.exit("Usage: python3 uaclient.py config method option")





if __name__ == "__main__":