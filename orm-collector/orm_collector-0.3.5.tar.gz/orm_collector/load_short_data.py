"""
Este script es la versión recortada para
cargar solamente la info general de los tipos
de bases de datos y protocolos

Luego, mediante interfaz el usuario podrá cargar
los datos particulares de cada estación
"""

from manager import SessionCollector
from pathlib import Path
import csv

pwd = str(Path(__file__).resolve().parent)

file_protocol = pwd+"/fixtures/protocol.csv"
file_dbtype = pwd+"/fixtures/dbtype.csv"

session = SessionCollector()

this_protocol = dict()

with open(file_protocol, 'r') as rfile:
    reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)
        for k in row.keys():
            row[k] = row[k].rstrip().lstrip()
        p = row['name']
        if not session.get_protocol_id(p) and p != '':
            this_protocol[int(row['id'])] = session.protocol(**row)

this_dbtype = dict()

print("Protocol ok")

with open(file_dbtype, 'r') as rfile:
    reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        for k in row.keys():
            row[k] = row[k].rstrip().lstrip()
        print(row)
        p = row['name']
        if not session.get_dbtype_id(p) and p != '':
            this_dbtype[int(row['id'])] = session.dbtype(**row)

this_dbdata = dict()

print("DBType ok")
