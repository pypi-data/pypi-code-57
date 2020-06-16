# coding=utf-8
from __future__ import division, absolute_import, print_function

import sys
def redtext(value = '\n'):
    sys.stderr.writelines([value])
    if '\n' not in value and '\r' not in value: sys.stderr.writelines('\n')
    pass


# --- Encodings --- #

class _Secure:
    pass

class _Encodings:
    pass

class _Test:
    pass

class _EncodingsTest(_Test):
    def _test():
        print = redtext
        errors = {}
        success = []

        tests = _Encodings.__subclasses__()
        for test in tests:
            try:
                testobj = test()
            except Exception as e:
                errors[test.__name__] = e
            else:
                success.append(test.__name__)

        print()
        if len(success) > 0:
            print('SUCCESSES: ')
        for s in success:
            print(s+' - Success')
        if len(errors) > 0:
            print('ERRORS: ')
        for name, e in errors.items():
            print('Error when running '+name+'. Error: '+str(e))

        print()
        print('Total Successes: '+str(len(success)))
        print('Total Errors: '+str(len(errors)))
        print('Percent Success: About \
'+str((len(success)/(len(success)+len(errors))*100))+'%')
        print()
        return errors, success

class NumEncodings(_Encodings):
    def __init__(self):
        class _internal:
            def main():
                return __import__('random'), __import__('string')
            
            def split(str, num):
                return [str[start:start+num] for start in range(0, len(str), \
                                                                num)]

            def ntb(x, b):
                d = ''
                while x:
                    d += str(int(x%b))
                    x //= b
                return d[::-1]
        self._internal = _internal
        self.random, self.string = self._internal.main()
        self.printable = self.string.printable
        self.randint = self.random.randint

        class _get(_Secure):
            def main():
                return int('42112821676159749070709874751994\
4867499418842994346930451824837866394740774515130318342052010\
4023972602739726027397260273972602739726027397260273972602739\
7260273972602739726027397260273972602739726027397260273972602\
73972602739726027397260273972602739726027397260273972602739726\
027397260273972602739726027397260273972602739726027397260273972\
60273972602739726027397260273972602739726027397260273972602739\
7260273972602739726027397260273972602739726027397260273972602739\
726027397260273972602739726027397260273972602739726027397260273\
972602739726027397260273972602739726027397260273972602')

        self._get = _get
        self._secure = self._get.main()
            
    def genkey(self):
        r = []
        for x in range(100):
            y = 0
            while y not in r or y == 0:
                y = self.randint(100000, 999999)
                if y not in r and y != 0:
                    r.append(y)
        k = {}
        for c in range(100):
            k[self.printable[c]] = r[c]
        return k

    def encode(self, msg, key):
        return ''.join([str(key.get(x, x)) for x in msg])

    def decode(self, msg, key):
        key = {y: x for x, y in key.items()}
        return ''.join([str(key.get(int(x), x)) for x in \
                        self._internal.split(msg, 6)])



class PerfectCipher(_Encodings):
    def __init__(self):
        class _internal:
            def main():
                class BlankCryption:
                    def encode(data):
                        d = ''
                        for x in range(min([len(data), \
                                            len(self.BlankCryption.key)])):
                            da = ord(data[x])
                            ke = ord(self.BlankCryption.key[x])
                            en = chr(da+ke)
                            d += en
                        return d

                    def decode(data):
                        d = ''
                        for x in range(min([len(data), \
                                            len(self.BlankCryption.key)])):
                            da = ord(data[x])
                            ke = ord(self.BlankCryption.key[x])
                            de = chr(da-ke)
                            d += de
                        return d
                    
                class Keys:
                    def makekey():
                        key = ''.join([self.random.choice(\
                            self.string.printable) for x in \
                                       range(self.Keys.keylen)])
                        return self.Keys.ed.encode(key)

                    def getkeycodes():
                        return [ord(x) for x in self.Keys.key]

                    def generatekey():
                        return self.Keys.makekey()
                    
                class FileEncoding:
                    def encode(msg):
                        msg = msg.encode() if type(msg) == str else msg
                        return self.b64encode(msg)

                    def decode(msg):
                        msg = msg.encode() if type(msg) == str else msg
                        return self.b64decode(msg).decode()

                class FileWriter:
                    def write(file, msg):
                        return open(file, 'wb').write(msg)

                    def read(file):
                        return open(file, 'rb').read()

                class OrderCryption:
                    def genorder(numkeys):
                        l = [x+1 for x in range(numkeys)]
                        self.random.shuffle(l)
                        return l

                    def genkeys(order):
                        l = len(order)
                        k = [self.genkey() for x in range(l)]
                        return k

                    def processkeys(keys, order):
                        k = []
                        for x in order:
                            k.append(keys[x-1])
                        return k

                    def encodeorder(msg, processedkeys):
                        e = msg
                        for key in processedkeys:
                            self.setkey(key)
                            e = self.encode(e)
                        return e

                    def decodeorder(msg, processedkeys):
                        processedkeys.reverse()
                        e = msg
                        for key in processedkeys:
                            self.setkey(key)
                            e = self.decode(e)
                        return e

                    def combine(o1, k1, o2, k2):
                        si1 = ''
                        for x in o1:
                            si1 += str(x)
                        si2 = ''
                        for x in o2:
                            si2 += str(x)
                        i1 = int(si1)
                        i2 = int(si2)
                        if i1 > i2:
                            s = [o1, o2]
                        else:
                            s = [o2, o1]
                        
                        o = []
                        k = []
                        if s[0] == o1:
                            for x in o1:
                                o.append(x)
                            for x in o2:
                                o.append(x+len(o1))
                            for x in k1:
                                k.append(x)
                            for x in k2:
                                k.append(x)
                        else:
                            for x in o2:
                                o.append(x)
                            for x in o1:
                                o.append(x+len(o1))
                            for x in k2:
                                k.append(x)
                            for x in k1:
                                k.append(x)
                        return o, k

                    def genok(numkeys):
                        o = self.genorder(numkeys)
                        k = self.genkeys(o)
                        return o, k

                    def gensandwich(numkeys):
                        return {'inner': self.genok(numkeys),
                                'outer': self.genok(numkeys)}

                    def processsand(sand):
                        d = {x: list(y) for x, y in sand.items()}
                        d['inner'][1] = self.processkeys(d['inner'][1], d['inner'][0])
                        d['outer'][1] = self.processkeys(d['outer'][1], d['outer'][0])
                        return d

                    def encodesand(msg, processedsand):
                        d = processedsand
                        processedkeys = d['inner'][1], d['outer'][1]
                        msg = self.encodeorder(msg, processedkeys[1])
                        msg = self.encodeorder(msg, processedkeys[0])
                        msg = self.encodeorder(msg, processedkeys[1])
                        return msg

                    def decodesand(msg, processedsand):
                        d = processedsand
                        processedkeys = d['inner'][1], d['outer'][1]
                        msg = self.decodeorder(msg, processedkeys[1])
                        msg = self.decodeorder(msg, processedkeys[0])
                        msg = self.decodeorder(msg, processedkeys[1])
                        return msg

                    def combinesand(sand1, sand2):
                        d = {'inner': self.combine(sand1['inner'][0], sand1['inner'][1],
                                                   sand2['inner'][0], sand2['inner'][1]),
                             'outer': self.combine(sand1['outer'][0], sand1['outer'][1],
                                                   sand2['outer'][0], sand2['outer'][1])}
                        return d

                    def encodersa(rsa):
                        self.setkey(self.getkey()*len(rsa))
                        return self.encode(__import__('__main__').RSA().key_to_str(rsa))

                    def decodersa(rsa):
                        self.setkey(self.getkey()*len(rsa))
                        return __import__('__main__').RSA().str_to_key(self.decode(rsa))
                    
                class RSA:
                    def genRSA(len):
                        import Crypto.PublicKey.RSA as r
                        return r.generate(len)
                    
                    
                return __import__('random'), __import__('string'), \
                       __import__('base64'), BlankCryption, Keys, \
                       FileEncoding, FileWriter, OrderCryption, RSA

        self._internal = _internal
        self.random, self.string, self.base64, self.BlankCryption, \
                     self.Keys, self.FileEncoding, self.FileWriter,\
                     self.oc, self.RSA = self._internal.main()
        self.b64encode = self.base64.b64encode
        self.b64decode = self.base64.b64decode
        self.BlankCryption.keylen = 8192
        self.BlankCryption.key = None
        self.BlankCryption.random = self.random
        self.BlankCryption.string = self.string
        if self.BlankCryption.key == None:
            self.BlankCryption.key = ''.join([self.random.choice(\
                self.string.printable) for x in \
                range(self.BlankCryption.keylen)])
        else:
            self.BlankCryption.key = self.BlankCryption.key
            
        self.Keys.key = self.BlankCryption.key
        self.Keys.keylen = self.BlankCryption.keylen
        self.Keys.ed = self.BlankCryption
        self.Keys.keycodes = self.Keys.getkeycodes()

    def encodersa(self, rsa):
        return self.oc.encodersa(rsa)

    def decodersa(self, rsa):
        return self.oc.decodersa(rsa)

    def combinesand(self, sand1, sand2):
        return self.oc.combinesand(sand1, sand2)

    def gensand(self, numkeys):
        return self.oc.gensandwich(numkeys)

    def processsand(self, sand):
        return self.oc.processsand(sand)

    def encodesand(self, msg, processedsand):
        return self.oc.encodesand(msg, processedsand, rsa)

    def decodesand(self, msg, processedsand):
        return self.oc.decodesand(msg, processedsand, rsa)

    def rsa(self, length):
        return self.encode(str(self.RSA.genRSA(length).n))

    def genorder(self, numkeys):
        return self.oc.genorder(numkeys)

    def genkeys(self, order):
        return self.oc.genkeys(order)

    def genok(self, numkeys):
        return self.oc.genok(numkeys)

    def processkeys(self, keys, order):
        return self.oc.processkeys(keys, order)

    def encodeorder(self, msg, processedkeys):
        return self.oc.encodeorder(msg, processedkeys)

    def decodeorder(self, msg, processedkeys):
        return self.oc.decodeorder(msg, processedkeys)

    def combine(self, o1, k1, o2, k2):
        return self.oc.combine(o1, k1, o2, k2)

    def encode(self, msg):
        return self.Keys.ed.encode(msg)

    def decode(self, msg):
        return self.Keys.ed.decode(msg)

    def setkey(self, key):
        self.BlankCryption.keylen = len(key)
        self.BlankCryption.key = key
        self.Keys.keylen = len(key)
        self.Keys.key = key

    def getkey(self):
        return self.Keys.key

    def genkey(self):
        return self.Keys.generatekey()

from base64 import b64encode, b64decode
from math import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify
import sys


PY3 = sys.version_info[0] == 3

if PY3:
    binary_type = bytes
    range_func = range
else:
    binary_type = str
    range_func = xrange

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

class RSA(_Encodings):
    def is_prime(self, n, k=30):
        # http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
        if n <= 3:
            return n == 2 or n == 3
        neg_one = n - 1

        # write n-1 as 2^s*d where d is odd
        s, d = 0, neg_one
        while not d & 1:
            s, d = s + 1, d >> 1
        assert 2 ** s * d == neg_one and d & 1

        for _ in range_func(k):
            a = randrange(2, neg_one)
            x = pow(a, d, n)
            if x in (1, neg_one):
                continue
            for _ in range_func(s - 1):
                x = x ** 2 % n
                if x == 1:
                    return False
                if x == neg_one:
                    break
            else:
                return False
        return True


    def randprime(self, n=10 ** 8):
        p = 1
        while not self.is_prime(p):
            p = __import__('random').randrange(n)
        return p


    def multinv(self, modulus, value):
        """
            Multiplicative inverse in a given modulus

            >>> multinv(191, 138)
            18
            >>> multinv(191, 38)
            186
            >>> multinv(120, 23)
            47
        """
        # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        x, lastx = 0, 1
        a, b = modulus, value
        while b:
            a, q, b = b, a // b, a % b
            x, lastx = lastx - q * x, x
        result = (1 - lastx * modulus) // value
        if result < 0:
            result += modulus
        assert 0 <= result < modulus and value * result % modulus == 1
        return result

    def keygen(self, n, public=None):
        """ Generate public and private keys from primes up to N.

        Optionally, specify the public key exponent (65537 is popular choice).

            >>> pubkey, privkey = keygen(2**64)
            >>> msg = 123456789012345
            >>> coded = pow(msg, *pubkey)
            >>> plain = pow(coded, *privkey)
            >>> assert msg == plain

        """
        # http://en.wikipedia.org/wiki/RSA
        prime1 = self.randprime(n)
        prime2 = self.randprime(n)
        composite = prime1 * prime2
        totient = (prime1 - 1) * (prime2 - 1)
        if public is None:
            private = None
            while True:
                private = randrange(totient)
                if gcd(private, totient) == 1:
                    break
            public = self.multinv(totient, private)
        else:
            private = self.multinv(totient, public)
        assert public * private % totient == gcd(public, totient) == gcd(private, \
                                                                         totient) \
               == 1
        assert pow(pow(1234567, public, composite), private, composite) == 1234567
        return KeyPair(Key(public, composite), Key(private, composite))


    def encode(self, msg, pubkey, verbose=False):
        chunksize = int(log(pubkey.modulus, 256))
        outchunk = chunksize + 1
        outfmt = '%%0%dx' % (outchunk * 2,)
        bmsg = msg if isinstance(msg, binary_type) else msg.encode('utf-8')
        result = []
        for start in range_func(0, len(bmsg), chunksize):
            chunk = bmsg[start:start + chunksize]
            chunk += b'\x00' * (chunksize - len(chunk))
            plain = int(hexlify(chunk), 16)
            coded = pow(plain, *pubkey)
            bcoded = unhexlify((outfmt % coded).encode())
            if verbose:
                print('Encode:', chunksize, chunk, plain, coded, bcoded)
            result.append(bcoded)
        return b''.join(result)


    def decode(self, bcipher, privkey, verbose=False):
        chunksize = int(log(privkey.modulus, 256))
        outchunk = chunksize + 1
        outfmt = '%%0%dx' % (chunksize * 2,)
        result = []
        for start in range_func(0, len(bcipher), outchunk):
            bcoded = bcipher[start: start + outchunk]
            coded = int(hexlify(bcoded), 16)
            plain = pow(coded, *privkey)
            chunk = unhexlify((outfmt % plain).encode())
            if verbose:
                print('Decode:', chunksize, chunk, plain, coded, bcoded)
            result.append(chunk)
        return b''.join(result).rstrip(b'\x00').decode('utf-8')


    def key_to_str(self, key):
        """
        Convert `Key` to string representation
        >>> key_to_str(Key(50476910741469568741791652650587163073, 95419691922573224706\
        255222482923256353))
        '25f97fd801214cdc163796f8a43289c1:47c92a08bc374e96c7af66eb141d7a21'
        """
        return ':'.join((('%%0%dx' % ((int(log(number, 256)) + 1) * 2)) % number) \
                        for number in key)


    def str_to_key(self, key_str):
        """
        Convert string representation to `Key` (assuming valid input)
        >>> (str_to_key('25f97fd801214cdc163796f8a43289c1:47c92a08bc374e96c7af66eb141d7a21') ==
        ...  Key(exponent=50476910741469568741791652650587163073, modulus=95419691922\
        573224706255222482923256353))
        True
        """
        return Key(*(int(number, 16) for number in key_str.split(':')))

# --- Compressors --- #

class _Compressors:
    pass

class _CompressorsTest(_Test):
    def _test():
        print = redtext
        errors = {}
        success = []

        tests = _Compressors.__subclasses__()
        for test in tests:
            try:
                testobj = test()
            except Exception as e:
                errors[test.__name__] = e
            else:
                success.append(test.__name__)

        print()
        if len(success) > 0:
            print('SUCCESSES: ')
        for s in success:
            print(s+' - Success')
        if len(errors) > 0:
            print('ERRORS: ')
        for name, e in errors.items():
            print('Error when running '+name+'. Error: '+str(e))

        print()
        print('Total Successes: '+str(len(success)))
        print('Total Errors: '+str(len(errors)))
        print('Percent Success: About \
'+str((len(success)/(len(success)+len(errors))*100))+'%')
        print()
        return errors, success

class Compressor(_Compressors):
    def __init__(self):
        class _internal:
            def main():
                return __import__('base64'), __import__('random')
                
            def mbytes(data):
                if type(data) == str: return data.encode()
                return data

            def mstr(data):
                if type(data) == bytes: return data.decode()
                return data

            def compress(data):
                return self.mstr(self.b64encode(self.mbytes(data)).decode())

            def decompress(data):
                return self.mstr(self.b64decode(self.mbytes(data)))

            def numencode(data):
                return [x for x in self.mbytes(data)]

            def numdecode(data):
                return bytes(data)

            def numtofile(data):
                return self.mstr(' '.join([str(x) for x in data]))

            def numfromfile(data):
                return [int(x) for x in data.split()]

            def mencoding(charmap):
                _map = dict((c, r) for chars, r in charmap for c in list(chars))
                return _map

            def encode(data, encoding):
                return ''.join((encoding.get(x) or x) for x in data)

            def decode(data, encoding):
                encoding = {y: x for x, y in encoding.items()}
                return ''.join((encoding.get(x) or x) for x in data)

            def getfunctions():
                return self._internal.mbytes, self._internal.mstr, \
                       self._internal.compress, self._internal.decompress, \
                       self._internal.numencode, self._internal.numdecode, \
                       self._internal.numtofile, self._internal.numfromfile, \
                       self._internal.mencoding, self._internal.encode, \
                       self._internal.decode

        self._internal = _internal
        self.base64, self.random = self._internal.main()
        self.b64encode = self.base64.b64encode
        self.b64decode = self.base64.b64decode
        self.mbytes, self.mstr, self.compress, self.decompress, \
                     self.numencode, self.numdecode, self.numtofile, \
                     self.numfromfile, self.mencoding, self.encode, \
                     self.decode = self._internal.getfunctions()

# --- Code Breakers --- #
# -- Frequency Calculators -- #
class _FCalculator:
    pass

class _FCalculatorTest(_Test):
    def _test():
        print = redtext
        errors = {}
        success = []

        tests = _FCalculator.__subclasses__()
        for test in tests:
            try:
                testobj = test()
            except Exception as e:
                errors[test.__name__] = e
            else:
                success.append(test.__name__)

        print()
        if len(success) > 0:
            print('SUCCESSES: ')
        for s in success:
            print(s+' - Success')
        if len(errors) > 0:
            print('ERRORS: ')
        for name, e in errors.items():
            print('Error when running '+name+'. Error: '+str(e))

        print()
        print('Total Successes: '+str(len(success)))
        print('Total Errors: '+str(len(errors)))
        print('Percent Success: About \
'+str((len(success)/(len(success)+len(errors))*100))+'%')
        print()
        return errors, success

class FCalculator(_FCalculator):
    def __init__(self):
        from collections import Counter
        self.Counter = Counter
        class _internal:
            def similar(base, nums):
                l = {}
                for x in nums:
                    l[abs(base - x)] = x
                ml = [x for x in l]
                m = min(ml)
                return l[m]

            def getenkey():
                return {'a': 0.08497, 'b': 0.01492, 'c': 0.02202, \
                        'd': 0.04253, 'e': 0.11162, 'f': 0.02228, \
                        'g': 0.02015, 'h': 0.06094, 'i': 0.07546, \
                        'j': 0.00153, 'k': 0.01292, 'l': 0.04025, \
                        'm': 0.02406, 'n': 0.06749, 'o': 0.07507, \
                        'p': 0.01929, 'q': 0.00095, 'r': 0.07587, \
                        's': 0.06327, 't': 0.09356, 'u': 0.02758, \
                        'v': 0.00978, 'w': 0.0256, 'x': 0.0015, \
                        'y': 0.01994, 'z': 0.00077}

            def getrenkey():
                return {y: x for x, y in self._internal.getenkey().items()}

            def getfreq(s):
                Counter = self.Counter
                s = s.lower()
                return {x[0]: x[1]/len(s) for x in Counter(s).most_common()}

            def compfreq(f):
                k = list(self._internal.getrenkey())
                return
            
        self._internal = _internal

class _Vars:
    pass

class _VarsTest(_Test):
    def _test():
        print = redtext
        errors = {}
        success = []

        tests = _Vars.__subclasses__()
        for test in tests:
            try:
                testobj = test()
            except Exception as e:
                errors[test.__name__] = e
            else:
                success.append(test.__name__)

        print()
        if len(success) > 0:
            print('SUCCESSES: ')
        for s in success:
            print(s+' - Success')
        if len(errors) > 0:
            print('ERRORS: ')
        for name, e in errors.items():
            print('Error when running '+name+'. Error: '+str(e))

        print()
        print('Total Successes: '+str(len(success)))
        print('Total Errors: '+str(len(errors)))
        print('Percent Success: About \
'+str((len(success)/(len(success)+len(errors))*100))+'%')
        print()
        return errors, success

class Vars(_Vars):
    def __init__(self):
        class _internal:
            pass

        self._internal = _internal

    def bytes2str(self, bytes):
        return __import__('base64').b64encode(bytes).decode()

    def str2bytes(self, str):
        return __import__('base64').b64decode(str.encode())

    def str2int(self, str):
        return tuple([ord(x) for x in str])

    def int2str(self, int):
        return ''.join([chr(x) for x in int])

    def bytes2int(self, bytes):
        return tuple([x for x in bytes])

    def int2bytes(self, int):
        return bytes(list(int))


class _Pickle:
    pass

class _PickleTest(_Test):
    def _test():
        print = redtext
        errors = {}
        success = []

        tests = _Pickle.__subclasses__()
        for test in tests:
            try:
                testobj = test()
            except Exception as e:
                errors[test.__name__] = e
            else:
                success.append(test.__name__)

        print()
        if len(success) > 0:
            print('SUCCESSES: ')
        for s in success:
            print(s+' - Success')
        if len(errors) > 0:
            print('ERRORS: ')
        for name, e in errors.items():
            print('Error when running '+name+'. Error: '+str(e))

        print()
        print('Total Successes: '+str(len(success)))
        print('Total Errors: '+str(len(errors)))
        print('Percent Success: About \
'+str((len(success)/(len(success)+len(errors))*100))+'%')
        print()
        return errors, success

class PickleMain(_Pickle):
    def __init__(self):
        class _internal:
            pass

        self._internal = _internal

    def encode(self, data):
        return __import__('pickle').dumps(data)

    def decode(self, data):
        return __import__('pickle').loads(data)
        
def _test():
    print = redtext
    errs = 0
    suc = 0
    for test in _Test.__subclasses__():
        print('Testing '+test.__name__+' class. ')
        print()
        t = test._test()
        errs += len(t[0])
        suc += len(t[1])

    print('Errors: %s'%errs)
    print('Successes: %s'%suc)
    print()

    for test in _Test.__subclasses__():
        for obj in globals()[test.__name__.split('Test')[0]].__subclasses__():
            globals()[obj.__name__.lower()] = obj()
            print('"'+obj.__name__.lower()+'" is a test object of the \
'+obj.__name__+' class. ')

    sys.stderr.writelines(['\nPress enter to exit or start interaction. '])
    input()

if __name__ == '__main__':
    _test()
