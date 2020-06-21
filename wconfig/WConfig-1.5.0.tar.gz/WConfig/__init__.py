# -*- encoding: utf-8 -*-

import os
import sys
import pickle

"""
    Pickle.load(FILE) -> OBJECT
    Pickle.loads(DATA[BYTES]) -> OBJECT

    Pickle.dump(FILE) -> None
    Pickle.dumps(DATA[OBJECT]) -> Bytes
"""

"""
    Config(path, encoding='utf-8', type=YAML, format='$k: $v') -> Config Object
    Config.removeLine(ln) : remove a line of file
    Config.save() : save file
    Config.set(key, val) : set value
"""

YAML = '.yml'
TEXT = '.text'
CFG = '.cfg'
INI = '.ini'

ENDL = '\n'

__all__ = ['Config','YAML','TEXT','CFG','INI','ENDL']

class Config:
    def __init__(self, path, encoding = 'utf-8', type = YAML, format = '$k: $v', descriptions = []):
        self.f = open(path, 'ab')
        self.path = path
        self.type = YAML
        self.format = format
        self.encoding = encoding

        for i in descriptions:
            self.f.write(bytes(('#%s' % i)+ENDL) ,self.encoding)

        self.save()

    def removeLine(self, ln):
        self.f.close()

        with open(self.path,'rb') as of:
            with open(self.path,'rb+') as nf:
                cl = 0

                while cl < (ln-1):
                    of.readline()
                    cl += 1

                skp = of.tell()
                nf.seek(skp)

                of.readline()
                nl = of.readline()

                while nl:
                    nf.write(nl)
                    nl = of.readline()
                nf.truncate()

    def save(self):
        self.f.close()
        self.f = open(self.path, 'ab')

    def set(self, key, val):
        key = str(key)
        if self.get(key):
            a = self.get(key, True)
            if not a[0] == None:
                self.removeLine(a[1])
                self.save()

        if isinstance(val, (str, int, float)):
            value = str(val)
            self.f.write(bytes(self.format.replace("$k", key).replace("$v", val)+"\n",encoding = "UTF-8"))
        else:
            data = pickle.dumps(val)
            self.f.write(bytes(self.format, 'utf-8').replace(b"$k", bytes(key, 'utf-8')).replace(b"$v", data)+b"\n")

    def get(self, key, returnSeek = False):
        key = bytes(key, 'utf-8')
        readline = None
        spfont = self.format.replace('$k', '').replace('$v', '')

        kn = self.format.count('$k')
        vn = self.format.count('$v')

        self.f.close()
        self.f = open(self.path, 'rb')
        sk = 0
        while not readline == b'':
            readline = self.f.readline()
            if readline == b'':
                break
            sk += 1
            re = readline.split(bytes(spfont, 'utf-8'))

            if kn > 1:
                re[0] = re[0][0:int(len(re[0])/2)]

            if re[0] == key:
                self.save()
                
                try:
                    data = pickle.loads(bytes(spfont, 'utf-8').join(re[1:]).replace(b'\n',b''))
                    #print(1)
                    return data if not returnSeek else (data,sk)
                except:
                    data = str(bytes(spfont, 'utf-8').join(re[1:]).replace(b'\n',b''),'utf-8')
                    return data if not returnSeek else (data,sk)

        self.save()
        return None if not returnSeek else (None,0)

    def getAll(self):
        readline = None
        spfont = self.format.replace('$k', '').replace('$v', '')
        lis = {}

        kn = self.format.count('$k')
        vn = self.format.count('$v')

        self.f.close()
        self.f = open(self.path, 'rb')
        
        while not readline == b'':
            readline = self.f.readline()
            if readline == b'':
                break

            re = readline.split(bytes(spfont, 'utf-8'))

            if kn > 1:
                re[0] = re[0][0:int(len(re[0])/2)]
                
            try:
                data = pickle.loads(bytes(spfont, 'utf-8').join(re[1:]).replace(b'\n',b''))
                lis[str(re[0],'utf-8')] = data
            except:
                try:
                    data = str(bytes(spfont, 'utf-8').join(re[1:]).replace(b'\n',b''),'utf-8')
                    lis[str(re[0],'utf-8')] = data
                except UnicodeDecodeError:
                    print('Please check file encoding or add "class_key %s" to your python.' % str(re[0],'utf-8'))

        self.save()
        return lis
