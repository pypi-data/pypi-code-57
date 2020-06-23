

import time as _time
import json as _json
from collections import defaultdict as _defaultdict
from concurrent import futures as _futures
from copy import deepcopy as _deepcopy
from typing import Union, IO
from datetime import datetime
# Non standard libraries
import pandas as _pd
import requests as _requests
import jwt as _jwt
from pathlib import Path


# Set up default values
_org_id, _api_key, _tech_id, _pathToKey, _secret, _companyid = "", "", "", "", "", ""
_TokenEndpoint = "https://ims-na1.adobelogin.com/ims/exchange/jwt"
_cwd = Path.as_posix(Path.cwd())
_date_limit = 0
_token = ''
_header = {}


def createConfigFile(verbose: object = False)->None:
    """
    This function will create a 'config_admin.json' file where you can store your access data. 
    """
    json_data = {
        'org_id': '<orgID>',
        'api_key': "<APIkey>",
        'tech_id': "<something>@techacct.adobe.com",
        'secret': "<YourSecret>",
        'pathToKey': '<path/to/your/privatekey.key>',
    }
    with open('config_admin.json', 'w') as cf:
        cf.write(_json.dumps(json_data, indent=4))
    if verbose:
        print(' file created at this location : '+_cwd + '/config_admin.json')


def importConfigFile(file: str)-> None:
    """
    This function will read the 'config_admin.json' to retrieve the information to be used by this module. 
    """
    global _org_id
    global _api_key
    global _tech_id
    global _pathToKey
    global _secret
    global _endpoint
    with open(file, 'r') as file:
        f = _json.load(file)
        _org_id = f['org_id']
        _api_key = f['api_key']
        _tech_id = f['tech_id']
        _secret = f['secret']
        _pathToKey = f['pathToKey']


# Launch API Endpoint
_endpoint = 'https://platform.adobe.io'


def retrieveToken(verbose: bool = False, save: bool = False, **kwargs)->str:
    """ Retrieve the token by using the information provided by the user during the import importConfigFile function. 

    Argument : 
        verbose : OPTIONAL : Default False. If set to True, print information.
    """
    global _token
    with open(_pathToKey, 'r') as f:
        private_key_unencrypted = f.read()
        header_jwt = {'cache-control': 'no-cache',
                      'content-type': 'application/x-www-form-urlencoded'}
    jwtPayload = {
        # Expiration set to 24 hours
        "exp": round(24*60*60 + int(_time.time())),
        "iss": _org_id,  # org_id
        "sub": _tech_id,  # technical_account_id
        "https://ims-na1.adobelogin.com/s/ent_dataservices_sdk": True,
        "aud": "https://ims-na1.adobelogin.com/c/"+_api_key
    }
    encoded_jwt = _jwt.encode(
        jwtPayload, private_key_unencrypted, algorithm='RS256')  # working algorithm
    payload = {
        "client_id": _api_key,
        "client_secret": _secret,
        "jwt_token": encoded_jwt.decode("utf-8")
    }
    response = _requests.post(_TokenEndpoint, headers=header_jwt, data=payload)
    json_response = response.json()
    token = json_response['access_token']
    updateHeader(token=token)
    expire = json_response['expires_in']
    global _date_limit  # getting the scope right
    _date_limit = _time.time() + expire/1000 - 500  # end of time for the token
    if save:
        with open('token.txt', 'w') as f:  # save the token
            f.write(token)
    if verbose == True:
        print('token valid till : ' + _time.ctime(_time.time() + expire/1000))
        print('token has been saved here : ' + Path.as_posix(Path.cwd()))
    return token


def _checkToken(func):
    """    decorator that checks that the token is valid before calling the API    """
    def checking(*args, **kwargs):  # if function is not wrapped, will fire
        global _date_limit
        now = _time.time()
        if now > _date_limit - 1000:
            global _token
            _token = retrieveToken(*args, **kwargs)
            return func(*args, **kwargs)
        else:  # need to return the function for decorator to return something
            return func(*args, **kwargs)
    return checking  # return the function as object

###


@_checkToken
def _getData(endpoint: str, params: dict = None, data=None, header_info=None, *args, **kwargs):
    """
    Abstraction for getting data
    """
    global _header
    if header_info is not None:
        _header['Accept'] = _header['Accept']+header_info
    if params == None and data == None:
        res = _requests.get(endpoint, headers=_header)
    elif params != None and data == None:
        res = _requests.get(endpoint, headers=_header, params=params)
    elif params == None and data != None:
        res = _requests.get(endpoint, headers=_header, data=data)
    elif params != None and data != None:
        res = _requests.get(endpoint, headers=_header,
                            params=params, data=data)
    try:
        json = res.json()
    except:
        json = {'error': ['Request Error']}
    return json


@_checkToken
def _postData(endpoint: str, params: dict = None, data=None, *args, **kwargs):
    """
    Abstraction for getting data
    """
    global _header
    if params == None and data == None:
        res = _requests.post(endpoint, headers=_header)
    elif params != None and data == None:
        res = _requests.post(endpoint, headers=_header, params=params)
    elif params == None and data != None:
        res = _requests.post(endpoint, headers=_header, data=_json.dumps(data))
    elif params != None and data != None:
        res = _requests.post(endpoint, headers=_header,
                             params=params, data=_json.dumps(data=data))
    try:
        json = res.json()
    except:
        json = {'error': ['Request Error']}
    return json


@_checkToken
def _patchData(endpoint: str, params: dict = None, data=None, *args, **kwargs):
    """
    Abstraction for getting data
    """
    global _header
    if params == None and data == None:
        res = _requests.patch(endpoint, headers=_header)
    elif params != None and data == None:
        res = _requests.patch(endpoint, headers=_header, params=params)
    elif params == None and data != None:
        res = _requests.patch(endpoint, headers=_header,
                              data=_json.dumps(data))
    elif params != None and data != None:
        res = _requests.patch(endpoint, headers=_header,
                              params=params, data=_json.dumps(data=data))
    try:
        json = res.json()
    except:
        json = {'error': ['Request Error']}
    return json


@_checkToken
def _deleteData(endpoint: str, params: dict = None, data=None, *args, **kwargs):
    """
    Abstraction for getting data
    """
    global _header
    if params == None and data == None:
        res = _requests.delete(endpoint, headers=_header)
    elif params != None and data == None:
        res = _requests.delete(endpoint, headers=_header, params=params)
    elif params == None and data != None:
        res = _requests.delete(endpoint, headers=_header,
                               data=_json.dumps(data))
    elif params != None and data != None:
        res = _requests.delete(endpoint, headers=_header,
                               params=params, data=_json.dumps(data=data))
    try:
        status_code = res.status_code
    except:
        status_code = {'error': ['Request Error']}
    return status_code


def updateHeader(companyid: str = None, token: str = _token, **kwargs)->None:
    """ update the header when new token is generated
    This would be mandatory id you retrieved the company ID with the option "all". 
    Retrieving the company ID with option first or with a given position 
    will automatically call this method. 
    """
    global _header
    global _api_key
    global _companyid
    global _token
    global _org_id
    if token:
        _token = token
    _header = {"Accept": "application/vnd.adobe.xed-id+json",
               "Content-Type": "application/json",
               "Authorization": "Bearer "+_token,
               "X-Api-Key": _api_key,
               "x-gw-ims-org-id": _org_id
               }


_endpoint_schema = '/data/foundation/schemaregistry'


def getStats():
    path = '/stats/'
    res = _getData(_endpoint+_endpoint_schema+path)
    return res


def getSchemas():
    path = '/tenant/schemas/'
    res = _getData(_endpoint+_endpoint_schema+path)
    return res


def deleteSchema(schema_id: str = None):
    """
    Arguments:
        schema_id : meta:altId returned
    """
    if schema_id is None:
        raise Exception("Require an ID")
    path = f'/tenant/schemas/{schema_id}'
    res = _deleteData(_endpoint+_endpoint_schema+path)
    return res


def getMixins():
    path = '/tenant/mixins/'
    res = _getData(_endpoint+_endpoint_schema+path)
    return res


def getMixin(mixin_id: str = None, version: str = '1'):
    """
    Arguments:
        mixin_id : meta:altId
        version : version of the mixin
    """
    header_info = ';version='+str(version)
    path = f'/tenant/mixins/{mixin_id}'
    res = _getData(_endpoint+_endpoint_schema+path, header_info=header_info)
    return res


def deleteMixin(mixin_id: str = None):
    """
    Arguments:
        schema_id : meta:altId returned
    """
    if mixin_id is None:
        raise Exception("Require an ID")
    path = f'/tenant/mixins/{mixin_id}'
    res = _deleteData(_endpoint+_endpoint_schema+path)
    return res


def updateMixin(mixin_id: str = None, data: dict = None):
    """
    Arguments:
        schema_id : REQUIRED : meta:altId returned
        data : REQUIRED : dictionary on what to update on that mixin. 
    """
    if mixin_id is None or data is None:
        raise Exception("Require an ID and data")
    path = f'/tenant/mixins/{mixin_id}'
    res = _patchData(_endpoint+_endpoint_schema+path, data=data)
    return res


json_extend = [{'op': 'replace',
                'path': '/meta:intendedToExtend',
                'value': ['https://ns.adobe.com/xdm/context/profile',
                          'https://ns.adobe.com/xdm/context/experienceevent']}]
