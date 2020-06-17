#import vk_api
#class SecondDecoder(object):
#    def __init__(self,vk_audio:VkAudio):
#        code='var Qt = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/=", Yt = {\n            v: function(e) {\n                return e.split("").reverse().join("")\n            },\n            r: function(e, t) {\n                var n;\n                e = e.split("");\n                for (var i = Qt + Qt, a = e.length; a--; )\n                    ~(n = i.indexOf(e[a])) && (e[a] = i.substr(n - t, 1));\n                return e.join("")\n            },\n            s: function(e, t) {\n                var n = e.length;\n                if (n) {\n                    var i = function(e, t) {\n                        var n = e.length\n                          , i = [];\n                        if (n) {\n                            var a = n;\n                            for (t = Math.abs(t); a--; )\n                                t = (n * (a + 1) ^ t + a) % n,\n                                i[a] = t\n                        }\n                        return i\n                    }(e, t)\n                      , a = 0;\n                    for (e = e.split(""); ++a < n; )\n                        e[a] = e.splice(i[n - 1 - a], 1, e[a])[0];\n                    e = e.join("")\n                }\n                return e\n            },\n            i: function(e, t) {\n                return Yt.s(e, t ^ vk.id)\n            },\n            x: function(e, t) {\n                var n = [];\n                return t = t.charCodeAt(0),\n                each(e.split(""), (function(e, i) {\n                    n.push(String.fromCharCode(i.charCodeAt(0) ^ t))\n                }\n                )),\n                n.join("")\n            }\n        };\n        function Gt(e) {\n            if ((!window.wbopen || !~(window.open + "").indexOf("wbopen")) && ~e.indexOf("audio_api_unavailable")) {\n                var t, n, i = e.split("?extra=")[1].split("#"), a = "" === i[1] ? "" : Kt(i[1]);\n                if (i = Kt(i[0]),\n                "string" != typeof a || !i)\n                    return e;\n                for (var o = (a = a ? a.split(String.fromCharCode(9)) : []).length; o--; ) {\n                    if (t = (n = a[o].split(String.fromCharCode(11))).splice(0, 1, i)[0],\n                    !Yt[t])\n                        return e;\n                    i = Yt[t].apply(null, n)\n                }\n                if (i && "http" === i.substr(0, 4))\n                    return i\n            }\n            return e\n        }\n        function Kt(e) {\n            if (!e || e.length % 4 == 1)\n                return !1;\n            for (var t, n, i = 0, a = 0, o = ""; n = e.charAt(a++); )\n                ~(n = Qt.indexOf(n)) && (t = i % 4 ? 64 * t + n : n,\n                i++ % 4) && (o += String.fromCharCode(255 & t >> (-2 * i & 6)));\n            return o\n        }\n        function Xt(e) {\n            try {\n                return e.play() || Promise.resolve()\n            } catch (e) {\n                return Promise.reject(e)\n            }\n        };';
        
        
#code+='vk={id:%s};'%472427950
#import js2py
#with open('decode.js','w') as file:file.write(code)
#js2py.translate_file('decode.js','decode.py')
#from decode import var
#decode_func = var.get('Gt')
#url = 'https://m.vk.com/mp3/audio_api_unavailable.mp3?extra=Ag5Yzu9AuMOUAJqZmwnnn3rRmvrlwI9XnNa1AJzMzxz2ruD0CwyZCZuTogv4tNH2ztvZmY1SwMuTDs5SsKT1mZeZrdfVogHLEhfhyLy5zhLdmI1wzc1RqvH1wL9sDs9RwuLZDOHLuhDUAtnoyNn1wJHduJrKwMf5nYOZEevWmKK4uI5uBZGWqOjHnfHKytmZyY9OC1zKvg4Zs3jPDgXoyuTJDJr0oMqVzs9Lrg5ysfjXzwe4tfD6mwzqBxnYuZfwzhHguMvmwtfJzuL4mgvgAt9jzLDjtOLkqJC9l3jWn3byDg8YA1r1oq#AqS2mJG"'
#print(decode_func(url))
#import ctypes;
#ids=302808715
#class SecondDecoder:
#    def __init__(self,id):
#         self.HaveDll=True
#         self.dll=ctypes.cdll.LoadLibrary(r'')
#    def decode(url:str,ids:int):
#        self.dll.setUserId(ids)
#        self.dll.decode.restype=ctypes.c_char_p
#        self.dll.decode.argtypes=[ctypes.c_char_p,ctypes.c_bool]
#        self.dll.toMP3.restype=ctypes.c_char_p
#        return self.dll.decode(url.encode(),True).decode()
