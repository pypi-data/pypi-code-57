import hashlib
import pickle
import copy
import os
from base64 import *

def createdb(dbname, dbdata):
    db = pickle.dumps(dbname), pickle.dumps(dbdata)
    db = b64encode(db[0]), b64encode(db[1])
    db = b'\x00'.join(db)
    db = b64encode(db)
    return db

def _updatedb(dbdata, dbnewdata):
    dbdata = copy.copy(dbdata)
    dbdata.update(dbnewdata)
    return dbdata

def updatedb(bytes_data, dbnewdata):
    db = bytes_data
    g = getdb(db)
    return createdb(g[0], _updatedb(g[1], dbnewdata))

def hashpwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def verifypwd(hashed, pwd):
    return hashed == hashpwd(pwd)

def savedb(dbname, dbdata, dbfilename):
    return open(dbfilename, 'wb').write(createdb(dbname, dbdata))

def opendb(dbfilename):
    return getdb(open(dbfilename, 'rb').read())

def deldb(dbfilename):
    os.remove(dbfilename)

def getdb(bytes_data):
    dbdata = bytes_data
    db = b64decode(dbdata)
    db = db.split(b'\x00')
    db = b64decode(db[0]), b64decode(db[1])
    db = pickle.loads(db[0]), pickle.loads(db[1])
    return db
