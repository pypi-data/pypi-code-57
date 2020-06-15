import configparser
import json
import requests

_headKey    = "faspay-key"
_headTime   = "faspay-timestamp"
_headSign   = "faspay-signature"
_headAuth   = "faspay-authorization"

_host = dict()
_host["development"]    = "https://dev2.faspay.co.id"
_host["production"]     = "https://web.faspay.co.id"

_path = dict()
_path["get_token"]          = "/account/api/tokens"
_path["register"]           = "/account/api/register"
_path["register_confirm"]   = "/account/api/confirm"
_path["transfer"]           = "/account/api/transfer"
_path["balance_inquiry"]    = "/account/api/balance_inquiry"
_path["inquiry_name"]       = "/account/api/inquiry_name"
_path["mutasi"]             = "/account/api/mutasi"
_path["inquiry_status"]     = "/account/api/inquiry_status"

_method = dict()
_method["get_token"]        = "GET"
_method["register"]         = "POST"
_method["register_confirm"] = "POST"
_method["transfer"]         = "POST"
_method["balance_inquiry"]  = "GET"
_method["inquiry_name"]     = "GET"
_method["mutasi"]           = "GET"
_method["inquiry_status"]   = "GET"

_env                        = "development"
_section                    = "get_token"
_url                        = None
_current_method             = None
_current_path               = None
_content_type               = "application/json"
_headers                    = {}
_reqd                       = dict()
_reqx                       = None
_rspd                       = dict()
_rspx                       = None
_virtual_account            = None
_info                       = {}

def setEnvironment(self, env):
    self._env = env

def getEnvironment():
    return _env

def setSection(self, section):
    self._section = self._info["section"] = section

def getSection():
    return _section

def setRequestParam(self, data={}):
    config = configparser.ConfigParser()
    config.read('SendMeConfig.ini')
    if config.sections() == []: raise Exception("File Config not found. Please create file config based on Readme.md")

    try:
        data["virtual_account"]
    except :
        self.virtual_account = config.get(_env, "virtual_account")
        data.update({"virtual_account" : self.virtual_account})

    self._reqd = data
    #self._reqd = self._info["request"]["array"] = data
    __array2json(self)

def getResponseParam(self):
    __json2array(self)
    return _rspd

def setHeaders(self, valueKey, valueTime, valueSign, valueAuth):
    self._headers = self._info["headers"] = {
        _headKey : valueKey,
        _headTime : valueTime,
        _headSign : valueSign,
        _headAuth : valueAuth
    }

def getMethod(self):
    self._current_method = _method[self.getSection()]
    return _current_method

def getPath(self):
    self._current_path = _path[self.getSection()]
    return _current_path

def generateUrl(self):
    if _env == False or _section == False:
        return False

    host = self._info["host"] = _host[_env]
    path = self._info["path"] = _path[_section]
    self._url = self._info["url"] = host + path
    self._current_method = self._info["method"] = _method[_section]

    if _current_method == "GET" and len(_reqd) > 0:
        arrVal = []
        for x in _reqd: arrVal.append(_reqd[x])
        queryString = "/" + "/".join(arrVal)
        self._url = self._info["url"] = _url + queryString

def __array2json(self, param={}):
    if param == {} : param = _reqd

    if isinstance(param, list):
        self._reqx = json.dumps(param)

    #self._info["request"]["json"] = _reqx

def __json2array(self, param={}):
    if param == {} : param = _rspx

    if isinstance(param, str):
        self._rspd = json.loads(param)

    #self._info["response"]["array"] = _rspd
    #self._info["response"]["json"]  = _rspx

def curl(self):
    result = None
    self._headers["Accept"] = _content_type
    self._headers["Content-Type"] = _content_type

    self._info["headers"] = _headers

    if _reqx == None: self._reqx = _reqd

    r = requests.post(_url, json=_reqx, headers=_headers)
    result = r.text

    if r.status_code != 200: result = json.dumps({"error":True, "message":"faspay.sendme.http.code " + str(r.status_code)})

    self._rspx = result