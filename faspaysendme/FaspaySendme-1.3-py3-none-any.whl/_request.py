import configparser
import datetime
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from FaspaySendme import _http

_config         = None;
_faspayKey      = None;
_timestamp      = None;
_signature      = None;
_authorization  = None;
_token          = None;
_accessToken    = None;
_errors         = {};

def generateHeadersRequest(self):
    self._config = configparser.ConfigParser()
    self._config.read('SendMeConfig.ini')
    if _config.sections() == []: raise Exception("File Config not found. Please create file config based on Readme.md")

    self._timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    self._faspayKey = _config.get(_http.getEnvironment(), "faspay_key")
    self._authorization = self.generateAuthorization(self)

    self._accessToken = getToken(self)
    generateToken(self)
    self._signature = generateSignature(self)
    _http.setHeaders(_http, _faspayKey, _timestamp, _signature, _authorization)

def getToken(self):
    section = "get_token"
    generateToken(self, section)
    self._signature = generateSignature(self, _http._method[section])
    _http.setHeaders(_http, _faspayKey, _timestamp, _signature, _authorization)
    _http._url = _http._host[_http.getEnvironment()] + _http._path[section]
    _http.curl(_http)
    rspd = _http.getResponseParam(_http)

    if len(rspd) > 0 and rspd["status"] == "2":
        return rspd["access_token"]
    else:
        print(rspd);exit();

    return False

def generateAuthorization(self):
    faspaySecret    = _config.get(_http.getEnvironment(), "faspay_secret")
    appKey          = _config.get(_http.getEnvironment(), "app_key")
    appSecret       = _config.get(_http.getEnvironment(), "app_secret")

    string = appKey + ":" + appSecret
    auth = self.encryptAES256(string, faspaySecret)
    return auth

def generateToken(self, section=None):
    if section == "get_token":
        string = _config.get(_http.getEnvironment(), "client_key") + ":" + _config.get(_http.getEnvironment(), "client_secret")
        self._token = base64.b64encode(string.encode()).decode()
    else:
        string = _config.get(_http.getEnvironment(), "client_key") + ":" + _config.get(_http.getEnvironment(), "client_secret") + ":" + _accessToken
        self._token = base64.b64encode(string.encode()).decode()

def generateSignature(self, method=None, path=None):
    requestBody = ""

    if method == None: method = _http.getMethod(_http)
    if path == None: path = _http.getPath(_http)

    stringToSign = [method, path, _timestamp, _token, requestBody]
    stringToSign = ":".join(stringToSign)
    sign = self.encryptAES256(stringToSign, _config.get(_http.getEnvironment(), "faspay_secret"))
    return sign

def encryptAES256(string, key):
    plaintext   = string
    method      = AES.MODE_CBC
    iv          = _config.get(_http.getEnvironment(), "iv")

    passwd    = hashlib.sha256(key.encode()).digest()[0:32]
    iv        = hashlib.md5(key.encode() + iv.encode()).hexdigest()[-16:]
    raw       = pad(plaintext.encode(), AES.block_size)

    cipher    = AES.new(passwd, method, iv.encode())
    ciphEnc   = cipher.encrypt(raw)
    enc       = base64.b64encode(ciphEnc)
    return enc.decode()

def setErrors(self, code, message):
    self._errors = {
        "error" : True,
        "code" : code,
        "message" : message
    }