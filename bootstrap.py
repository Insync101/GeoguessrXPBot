# Written by corewave M8 D30 Y2022.

from ast import Import
from logging import exception
from queue import Empty
import subprocess
import json

STATUS = "Modules missing: "
MODULES = ['requests', 'uuid', 'http']
TOKEN = json.load(open('ncfa.json'))['_ncfa']
LENGTH = len(STATUS)

if len(TOKEN) == 0:
    TOKEN = input("Account token: ")
    with open('ncfa.json', 'w') as outfile:
        outfile.write(json.dumps({'_ncfa': TOKEN}))

for M in MODULES:
    try:
         __import__(M)
         print("{}: ☑.".format(M.capitalize()))
    except ImportError as e:
        STATUS += ("{} ".format(M))

if len(STATUS) > LENGTH:
    raise exception(STATUS)
else:
    print("\n")
    exec(open("main.py").read())
