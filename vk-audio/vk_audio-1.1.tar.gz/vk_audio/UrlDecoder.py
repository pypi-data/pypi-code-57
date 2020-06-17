class UrlDecoder:
    def __init__(self,uid,try_cpp_decoder=False):
        if(try_cpp_decoder):
            self.decoder=SecondDecoder(uid);
        else:self.decoder=None
        self.uid=uid;
    @classmethod
    def r(cls, e, t):
        e, o,b = (list(e), 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/=', len(list(e)))
        while a:
            a -= 1
            i = o.find(e[a])
            if ~i:
                e[a] = o[(i - t)]

        return ''.join(e)
    @classmethod
    def s(cls, e, t):
        if len(e):
            e_length, i, t_ = len(e), {}, t
            if e_length:
                o = e_length
                t_ = abs(t_)
                while o:
                    o -= 1
                    t = (e_length * (o + 1) ^ int(t) + o) % e_length
                    i[o] = t

            i, o = [e[1] for e in sorted((i.items()), key=(lambda a: a[0]))], 1
            e = list(e)
            while o < e_length:
                _, e = cls.splice(e, i[(e_length - 1 - o)], 1, e[o])
                e[o] = _[0]
                o += 1

            e = ''.join(e)
        return e
    def i(self, e, t):
        try:
            return self.s(e, int(t) ^ self.uid)
        except ValueError:
            return e
    @staticmethod
    def x(e, t):
        data = ''
        t = ord(t[0])
        for i in e:
            data += chr(ord(i[0]) ^ t)

        return data
    @classmethod
    def splice(cls, a, b, c, *d):
        if isinstance(b, (tuple, list)):
            return (cls.splice)(a, b[0], b[1], c, *d)
        c += b
        return (a[b:c], list(a)[:b] + list(d) + list(a)[c:])
    @classmethod
    def decode_r(cls, e):
        if not e or len(e) % 4 == 1:
            return False
        o, a, t, r, e_length = (
         0, 0, 0, '', len(e))
        while a < e_length:
            i = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/='.find(e[a])
            if ~i:
                t = 64 * t + i if o % 4 else i
                o += 1
                if (o - 1) % 4:
                    c = chr(255 & t >> (-2 * o & 6))
                    if c != '\x00':
                        r += c
            a += 1

        return r
    def decode(self, url):
        if(self.decoder and self.decoder.HaveDll):
            return delf.decoder.decode(url);
        if url.find('audio_api_unavailable'):
            t = url.split('?extra=')[1].split('#')
            n = '' if '' == t[1] else self.decode_r(t[1])
            t = self.decode_r(t[0])
            if  isinstance(n, str) and t :
                n = n.split(chr(9)) if n else []
            len_n = len(n)
            while len_n:
                len_n -= 1
                a, s = self.splice(n[len_n].split(chr(11)), 0, 1, t)
                _ = getattr(self, a[0], None)
                if _:
                    if len(s) < 2:
                        return url
                t = _(*s)
            if t[:4] == 'http':
                return self.get_mp3(t) if 'index.m3u8?' in t else t
        return t
    def get_mp3(self,url:str):
        a,q = '','';
        for i in url:
            if(i=='/'):
                if(len(q)!=12):a+=q;
                q='';
            elif(q=='/index.m3u8'):q='';a+='.mp3'
            q+=i;
        return a+q;
# okay decompiling decoder.pyc
