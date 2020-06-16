from .util import PerfectCipher, RSA, Compressor
from .backup import set_backup, get_backup, del_backup

class Person:
    def __init__(self, name, verbose = False):
        print = lambda x: __import__('sys').stderr.writelines([x+'\n']) if verbose else \
                lambda x: None

        pickle = __import__('pickle')
        print('Saving name...')
        self.name = name
        print('Saved name.')
        print('Generating & Saving perfectcipher...')
        self.perfectcipher = PerfectCipher()
        klen = 2**20
##        klen = 5
        self.perfectcipher.Keys.keylen = klen
        self.perfectcipher.BlankCryption.keylen = klen
        self.perfectcipher.setkey(self.perfectcipher.genkey())
        print('Generated & Saved perfectcipher.')
        print('Generating & Saving order, keys...')
        self.ok = pickle.dumps(self.perfectcipher.genok(150))
        print('Generated & Saved order, keys.')
        print('Saving order...')
        self.order = pickle.dumps(pickle.loads(self.ok)[0])
        print('Saved order.')
        print('Saving keys...')
        self.keys = pickle.dumps(pickle.loads(self.ok)[1])
        print('Saved keys.')
        print('Generating & Saving RSA...')
        self.rsa = RSA()
        print('Generated & Saved RSA.')
        print('Generating & Saving pubkey, prikey...')
        self.pubkey, self.prikey = self.rsa.keygen(2**1024)
        self.prikey = pickle.dumps(self.prikey)
        print('Generated & Saved pubkey, prikey.')
        print('Generating & Saving compressor...')
        self.compressor = Compressor()
        print('Generated & Saved compressor.')

        globals()['pickle'] = pickle

    def encodeok(self, pubkey, verbose = False):
        print = lambda x: __import__('sys').stderr.writelines([x+'\n']) if verbose else \
                lambda x: None
        
        oel = []
        kel = []
        
        for count in range(len(self.order)):
            print(str(count)+' '+str(len(self.order)-count))
            o = self.rsa.encode(str(self.order[count]), pubkey)
            k = self.rsa.encode(self.keys[count], pubkey)

            oel.append(o)
            kel.append(k)
            
        return oel, kel

    def decodeok(self, ok, prikey, verbose = False):
        print = lambda x: __import__('sys').stderr.writelines([x+'\n']) if verbose else \
                lambda x: None
        
        oel = ok[0]
        kel = ok[1]

        noel = []
        nkel = []

        for count in range(len(oel)):
            print(str(count)+' '+str(len(oel)-count))
            o = int(self.rsa.decode(oel[count], prikey))
            k = self.rsa.decode(kel[count], prikey)

            noel.append(o)
            nkel.append(k)

        return noel, nkel

    def processok(self, ok):
        return self.perfectcipher.processkeys(ok[1], ok[0])

    def encodetext(self, text, pubkey):
        return self.rsa.encode(text, pubkey)

    def decodetext(self, text, prikey):
        return self.rsa.decode(text, prikey)

    def encodebytes(self, data, pok):
        text = __import__('base64').b64encode(data).decode()
        return self.perfectcipher.encodeorder(text, pok)

    def decodebytes(self, data, pok):
        text = self.perfectcipher.decodeorder(data, pok)
        return __import__('base64').b64decode(text.encode())

    def encodefulltext(self, msg, pok, pubkey):
        msg = self.perfectcipher.encodeorder(msg, pok)
        return self.compress(self.rsa.encode(msg, pubkey))

    def decodefulltext(self, msg, pok, prikey):
        msg = self.rsa.decode(self.decompress(msg), prikey)
        return self.perfectcipher.decodeorder(msg, pok)

    def encodefullbytes(self, msg, pok, pubkey):
        msg = self.rsa.encode(msg, pubkey)
        msg = __import__('base64').b64encode(msg).decode()
        return self.compress(self.perfectcipher.encodeorder(msg, pok))

    def decodefullbytes(self, msg, pok, prikey):
        msg = self.perfectcipher.decodeorder(self.decompress(msg), pok)
        msg = __import__('base64').b64decode(msg.encode())
        return self.rsa.decode(msg, prikey)

    def compress(self, data):
        if type(data) == str:
            data = b'str'+data.encode()
        
        return __import__('base64').b64encode(data).decode()

    def decompress(self, data):
        data = __import__('base64').b64decode(data.encode())

        if data.startswith(b'str'):
            return data.strip(b'str').decode()
        return data

    eb = encodefullbytes
    db = decodefullbytes
    et = encodefulltext
    dt = decodefulltext
    c = compress
    d = decompress
