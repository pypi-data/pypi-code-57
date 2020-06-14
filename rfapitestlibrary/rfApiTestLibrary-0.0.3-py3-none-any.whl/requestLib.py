'''
Documentation: http请求所有方法
对http请求，返回处理的API封装。
引用包名是atBasicLibrary，引用本python文件，请使用Library  atBasicLibrary/requestLib.py.
【1】支持GET, POST, PUT, DELETE 方法
【2】正常的返回结果是字典类型,会返回request和Response的合集
{
    req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
    "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
    }
}
打印日志配置:
isWriteHtml=False  这个目前配置，不起作用。html报告都会打印的
also_console=True  主要是在console上
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   atBasicLibray/keywords/[ ../keywords/sc/request.html | request.robot ],
文档在[ ../keywords/request.doc.html | 这里 ]。
'''
import requests
import os
from robot.api import logger
import json as jsonUtils
from urllib import parse

################################
isWriteHtml=False
also_console=True

#封装的request和Response返回
_REQ="req"
_RESP="resp"
_URI="uri"
_HEADER="header"
_PARAMS="params"
_METHOD="method"
_STATUS_CODE="status_code"
_BODY="body"
_JSON="json"
#默认timeout时间
_TIMEOUT=45

_METHOD_GET="GET"
_METHOD_POST="POST"
_METHOD_PUT="PUT"
_METHOD_DELETE="DELETE"
###############################

def at_http_get(uri, params=None, headers=None, timeout=None):
    '''
    GET 请求。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Get%20request | Get request],
    [../keywords/request.doc.html#GET请求 | Get请求],

    Examples:
        |  关键字      |  参数                            |    参数                          |           参数           |          参数     |
        | at http get | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |   timeout=60      |
        | at http get | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |   timeout=${None} |
    '''
    if uri is None:
        logger.error("uri参数是None!",isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        response = requests.get(uri, headers=headers, params=params, timeout=timeout)
        requests.encoding = 'utf-8'
        reqAndRes=_at_get_req_and_resp_dict(params,headers,None,_METHOD_GET,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_post(uri, params=None, headers=None, body=None,  timeout=None):
    '''
    POST 请求。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型。
   【body】: request的body,String类型。
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Post%20request | Post request],
    [../keywords/request.doc.html#Post请求 | Post请求],

    Examples:
        |    关键字     |  参数                            |    参数                          |           参数           |  参数                |        参数      |
        | at http post | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |  body=13123131       |   timeout=60    |
        | at http post | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |  body={"aa":"123"}   | timeout=${None} |
    '''
    if uri is None:
        logger.error("uri参数是None!",isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        if body is not None:
            body=body.encode('utf-8')
        response = requests.post(uri, params=params, headers=headers, data=body, timeout=timeout)
        requests.encoding = 'utf-8'
        reqAndRes=_at_get_req_and_resp_dict(params,headers,body,_METHOD_POST,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_post_json(url,params=None,headers=None,json=None,timeout=None):
    '''
    POST 请求，是用json方式发送body，支持json String，json 字典或者列表。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型。
   【json】: request的json,符合json格式的String，或者列表(符合json格式，里面是字典)，或者字典格式
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Post%20json%20request | Post json request],
    [../keywords/request.doc.html#Post%20Json请求 | Post Json请求],

    Examples:
        |  关键字            |  参数                            |    参数                          |           参数           |  参数                             |        参数      |
        | at http post json | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |  json='{"aa":"1231","vv":True}'   |   timeout=60    |
        | at http post json | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |  json={"aa":"123"}                | timeout=${None} |
    '''
    if url is None:
        logger.error("url参数是None!",isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        if json is None:
            response = requests.post(url, params=params, headers=headers, json=json, timeout=timeout)
            reqAndRes = _at_get_req_and_resp_dict(params, headers, json, _METHOD_POST, response)
        else:
            if headers is None:
                headers={}
            headers.update({'Content-Type': 'application/json;charset=UTF-8'})
            if isinstance(json,str):
                body = json.encode('utf-8')
            elif isinstance(json,dict):
                body=jsonUtils.dumps(json, ensure_ascii=False).encode(encoding='utf-8')
            else:
                raise AssertionError('json类型不是string或者字典')
            response = requests.post(url, params=params, headers=headers, data=body, timeout=timeout)
            requests.encoding='utf-8'
            reqAndRes=_at_get_req_and_resp_dict(params,headers,json,_METHOD_POST,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_put(uri, params=None, headers=None, body=None,  timeout=None):
    '''
    PUT 请求。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型。
   【body】: request的body,String类型。
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Put%20request | Put request],
    [../keywords/request.doc.html#Put请求 | Put请求],

    Examples:
        |    关键字     |  参数                            |    参数                          |           参数           |  参数                |        参数      |
        | at http put  | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |  body=13123131       |   timeout=60    |
        | at http put  | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |  body={"aa":"123"}   | timeout=${None} |
    '''
    if uri is None:
        logger.error("uri参数是None!",isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        if body is not None:
            body=body.encode('utf-8')
        response = requests.put(uri, params=params, headers=headers, data=body, timeout=timeout)
        requests.encoding = 'utf-8'
        reqAndRes=_at_get_req_and_resp_dict(params,headers,body,_METHOD_PUT,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_put_json(url, params=None, headers=None, json=None,  timeout=None):
    '''
    PUT 请求，是用json方式发送body，支持json String，json 字典或者列表。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型。
   【json】: request的json,符合json格式的String，或者列表(符合json格式，里面是字典)，或者字典格式
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Put%20json%20request | Put json request],
    [../keywords/request.doc.html#Put%20Json请求  | Put Json请求],

    Examples:
        |   关键字          |  参数                            |    参数                          |           参数           |  参数                             |        参数      |
        | at http put json | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |  json='{"aa":"1231","vv":True}'   |   timeout=60    |
        | at http put json | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |  json={"aa":"123"}                | timeout=${None} |
    '''
    if url is None:
        logger.error("url参数是None!",isWriteHtml)
        raise AssertionError("url参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        if headers is None:
            headers = {}
        headers.update({'Content-Type': 'application/json;charset=UTF-8'})
        if json is None:
            response = requests.put(url, params=params, headers=headers, json=json, timeout=timeout)
            reqAndRes = _at_get_req_and_resp_dict(params, headers, json, _METHOD_POST, response)
        else:
            if isinstance(json,str):
                body = json.encode('utf-8')
            elif isinstance(json,dict):
                body=jsonUtils.dumps(json, ensure_ascii=False).encode(encoding='utf-8')
            else:
                raise AssertionError('json类型不是string或者字典')
            response = requests.put(url, params=params, headers=headers, data=body, timeout=timeout)
            requests.encoding = 'utf-8'
            reqAndRes=_at_get_req_and_resp_dict(params,headers,json,_METHOD_POST,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_delete(uri, params=None, headers=None, timeout=None):
    '''
    DELETE 请求。返回封装好的request和response的字典。
   【uri】: request的uri, String类型。
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Delete%20Request | Delete request],
    [../keywords/request.doc.html#Delete请求 | Delete请求],

    Examples:
        |     关键字      |  参数                            |    参数                          |           参数           |          参数     |
        | at http delete | http://localhost:8080/app/aa/bb | params={"cc":"3123","dd":"sada"} | headers={"token":32131} |   timeout=60      |
        | at http delete | http://localhost:8080/app/aa/bb |        params=${None}            |        headers=${None}  |   timeout=${None} |
    '''
    if uri is None:
        logger.error("uri参数是None!",isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        response = requests.delete(uri, headers=headers, params=params, timeout=timeout)
        requests.encoding = 'utf-8'
        reqAndRes=_at_get_req_and_resp_dict(params,headers,None,_METHOD_DELETE,response)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def at_http_post_files(uri, files,params=None,headers=None,timeout=None):
    '''
    POST方法上传多个文件。
   【uri】: request的uri, String类型。
   【files】:
        [
            ("<request name>" , ("<request file name>", open("filePath1", "rb"))),
            ("<request name>" , ("<request file name>", open("filePath2", "rb"), "image/png")),
            ("<request name>" , open("<request file name>", "rb")),
            ("<request name>" , open("<request file name>", "rb").read())
        ]
   【params】: request的parameter,字典类型。
   【headers】: request的header，字典类型
   【timeout】: request过期时间，float类型。单位秒。
    RETURN: 封装好的request和response的字典。字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Post%20Upload%20Files | Post upload files],
    [../keywords/request.doc.html#Post上传文件 | Post上传文件],

    '''
    if uri is None:
        logger.error("uri参数是None!", isWriteHtml)
        raise AssertionError("uri参数是None")
    if timeout is None:
        timeout=_TIMEOUT
    try:
        response = requests.post(uri,files=_at_fill_http_files(files),params=params,headers=headers,timeout=timeout)
        reqAndRes = {}
        reqAndRes[_REQ] = _at_fill_req_dict(response.url,params,headers, response.text,_METHOD_POST)
        reqAndRes[_RESP] = _at_fill_resp_dict(response)
        _at_log_req_and_rep(reqAndRes)
        return reqAndRes
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def _at_fill_http_files(file_path_dict):
    '''
    提供字典型filepath，生成符合上传要求的文件列表
   【file_path_dict】:字典类型，比如
         {
            <文件路径>:<request  name>,
            <文件路径>:<request  name>,
            <文件路径>:<request  name>
        }
    RETURN:列表类型。
        [
            ("<request  name>" , ("<request file name>", open("filePath1", "rb"))),
            ("<request name>" , ("<request file name>", open("filePath2", "rb"), "image/png")),
            ("<request name>" , open("<request file name>", "rb")),
            ("<request name>" , open("<request file name>", "rb").read())
        ]
    '''
    # 由于robot framework variable不是春字典型，所以注释掉后面的验证字典
    # if type(file_path_dict) is not type(builtins.__dict__):
    #     raise AssertionError("上传文件的参数不是字典类型")
    fileList=[]
    for key,value in file_path_dict.items():
        fileTuple=(value, (_at_get_file_name(key), open(key, "rb")))
        fileList.append(fileTuple)
    return fileList

def _at_fill_resp_dict(response):
    '''
    内部方法，通过Response组装成特殊格式字典。
    【response】: requests response类型
    RETURN: 字典类型。
    {
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
    }
    '''
    resp = {}
    resp[_STATUS_CODE] = response.status_code
    resp[_HEADER] = response.headers
    resp[_BODY] = response.text
    if response.text is not None and response.text !='':
        try:
            resp[_JSON]=jsonUtils.loads(response.text,encoding='utf-8')
        except Exception:
            #什么都不做
            logger.debug("无法解析response body到json",html=True)
    return resp

def _at_fill_req_dict(url,params,headers,body,method):
    '''
    内部方法，通过Request各个参数组成特殊格式字典。
   【url】: url，String类型。
   【params】: request的parameter,字典类型。
   【headers】: header，字典类型。
   【body】: String类型，request body。
   【method】: GET，POST，PUT，DELETE 方法。
    RETURN :
    {
        "header":<请求header,字典类型>,
        "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
        "uri":<uri String类型，含被转义的字符>,
        "method":"<GET/POST/PUT/DELETE>",
        "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
    }
    '''
    req = {}
    req[_URI] = url
    req[_METHOD] = method
    if params is not None:
        try:
            req[_PARAMS] = jsonUtils.dumps(params, ensure_ascii=False)
        except:
            req[_PARAMS] = str(params)
    if headers is not None:
        try:
            req[_HEADER] = jsonUtils.dumps(headers, ensure_ascii=False)
        except:
            req[_HEADER] = str(headers)
    if body is not None:
        if isinstance(body,str):
            req[_BODY] = body
        if isinstance(body,list) or isinstance(body,dict):
            try:
                req[_BODY] = jsonUtils.dumps(body, ensure_ascii=False)
            except:
                req[_BODY]=str(body)
    return req

def _at_get_req_and_resp_dict(params,headers,body,method,response):
    '''
    内部方法，通过Request各个参数和Response组装成特殊格式字典。
   【params】: request的parameter,字典类型。
   【headers】: header，字典类型。
   【body】: String类型，request body。
   【method】: GET，POST，PUT，DELETE 方法。
   【response】: requests response类型
    RETURN：字典类型。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    '''
    req_and_resp = {}
    url=response.url
    req=_at_fill_req_dict(url,params,headers,body,method)
    resp=_at_fill_resp_dict(response)
    req_and_resp[_REQ] = req
    req_and_resp[_RESP] = resp
    _at_log_req_and_rep(req_and_resp)
    return req_and_resp

def at_get_http_response(reqAndRespDic):
    '''
    通过字典获得response，返回字典
   【reqAndRespDic】: 字典类型
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN ： 字典类型
    {
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
    }
    '''
    return reqAndRespDic[_RESP]

def at_get_http_response_status_code(reqAndRespDic):
    '''
    获得response status code。返回Int类型。
   【reqAndRespDic】: request和response字典
   {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: int类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Get%20response%20status%20code | Get response status code],
    [../keywords/request.doc.html#获得response%20status%20code | 获得response status code],
    '''
    return at_get_http_response(reqAndRespDic)[_STATUS_CODE]

def at_get_http_response_header(reqAndRespDic):
    '''
    获得response headers。返回字典类型。
   【reqAndRespDic】: request和response字典
   {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: 字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Get%20response%20header | Get response header],
    [../keywords/request.doc.html#获得response%20header | 获得response header],
    '''
    return at_get_http_response(reqAndRespDic)[_HEADER]

def at_get_http_response_body(req_and_resp_dict):
    '''
    获得response body。返回String类型。
   【req_and_resp_dict】: request和response字典
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: String类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Get%20response%20body | Get response body],
    [../keywords/request.doc.html#获得response%20body | 获得response body],
    '''
    return at_get_http_response(req_and_resp_dict)[_BODY]

def at_get_http_response_json_body(req_and_resp_dict):
    '''
    获得response body。返回字典类型。
   【req_and_resp_dict】: request和response字典
    RETURN: 字典类型。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Get%20response%20json%20body | Get response json body],
    [../keywords/request.doc.html#获得Response%20json%20body| 获得Response json body],
    '''
    try:
        json_body=jsonUtils.loads(at_get_http_response(req_and_resp_dict)[_BODY])
        return json_body
    except:
        raise AssertionError("返回不是标准json,无法进行下一步校验")

def at_get_http_request(req_and_resp_dict):
    '''
    通过字典获得request，返回字典
   【req_and_resp_dict】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: 字典类型。
    {
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
    }
    '''
    return req_and_resp_dict[_REQ]

def get_http_request_header(req_and_resp_dict):
    '''
    通过字典获得request headers，返回字典
   【req_and_resp_dict】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: 字典类型。
    '''
    return at_get_http_request(req_and_resp_dict)[_HEADER]

def at_get_http_request_body(req_and_resp_dict):
    '''
    通过字典获得request body，返回String类型。
   【req_and_resp_dict】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: String类型。
    '''
    return at_get_http_request(req_and_resp_dict)[_BODY]

def at_get_http_request_method(req_and_resp_dict):
    '''
    通过字典获得request method，返回String类型。
   【req_and_resp_dict】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
            }
    }
    RETURN: String类型。
    '''
    return at_get_http_request(req_and_resp_dict)[_METHOD]

def at_get_http_request_uri(req_and_resp_dict):
    '''
    通过字典获得request URI，返回String类型。
   【reqAndRespDic】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
        }
    }
    RETURN: String类型。
    '''
    return at_get_http_request(req_and_resp_dict)[_URI]

def at_get_http_request_params(req_and_resp_dict):
    '''
    通过字典获得request parameters，返回字典类型。
   【req_and_resp_dict】: request和response字典。
    {
        req:{
            "header":<请求header,字典类型>,
            "body":<请求body, String类型，注意本方法不支持GET和DELETE传BODY>,
            "uri":<uri String类型，含被转义的字符>,
            "method":"<GET/POST/PUT/DELETE>",
            "params":"<Query parameters,就是?之后的key=value,代码会来帮你转义,其他不用管>"
        },
        "resp":{
            "header":<返回的header,字典类型>,
            "status_code":<返回的status code,整型>，
            "body":"<返回的body,String类型>"
        }
    }
    RETURN: 字典类型。
    '''
    return at_get_http_request(req_and_resp_dict)[_PARAMS]

def at_http_request(method, url, params=None, data=None,json=None,headers=None,cookies=None,files=None,auth=None,timeout=None,allow_redirects=None,proxies=None,verify=None,stream=None,cert=None):
    '''
    http请求通用方法。
   【method】: GET，POST，PUT，DELETE 方法。
   【url】  : url，String类型。
   【params】: request的parameter,字典类型。
   【data】: body data,String类型。
   【json】: body json。字典或者列表类型。
   【headers】: header，字典类型。
   【cookies】: cookie,字典类型。
   【files】: 文件，特殊类型的字典。
   【auth】:auth验证，元组类型。
   【timeout】: request timeout。过期时间。单位秒。
   【allow_redirects】:允许重定向。boolean类型。
   【proxies】:(optional) Dictionary mapping protocol to the URL of the proxy.
   【verify】: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
   【stream】: (optional) if ``False``, the response content will be immediately downloaded.
   【cert】: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
   【log_req】:
    RETURN：对request和Response字典的封装。

    目前使用该方法的关键字是:
    [../keywords/request.doc.html#Send%20request | Send request],
    [../keywords/request.doc.html#发送Request | 发送Request],
    '''
    if timeout is None:
        timeout=_TIMEOUT
    try:
        response=requests.request(method, url, params=params, data=data,json=json,headers=headers,cookies=cookies,files=files,auth=auth,timeout=timeout,allow_redirects=allow_redirects,proxies=proxies,verify=verify,stream=stream,cert=cert)
        req_and_resp = {}
        req=None
        if data is not None:
            req = _at_fill_req_dict(url, params, headers, data, method)
        if json is not None:
            req = _at_fill_req_dict(url, params, headers, json, method)
        if req is None:
            req = _at_fill_req_dict(url, params, headers, None, method)
        resp = _at_fill_resp_dict(response)
        req_and_resp[_REQ] = req
        req_and_resp[_RESP] = resp
        _at_log_req_and_rep(req_and_resp)
        return req_and_resp
    except requests.exceptions.RequestException as e:
        logger.error('发送请求失败，原因：%s' % e)
        raise AssertionError('发送请求失败，原因：%s' % e)

def _at_get_file_name(file_path):
    '''
    通过文件的相对路径或者绝对路径获取文件名
   【file_path】: String类型，文件的相对路径或者绝对路径
    RETURN: 文件名，String类型

    Examples:
        |      关键字       |  参数  |
        | at get file name | <path> |
    '''
    if not os.path.exists(file_path):
        raise AssertionError("[ %s ]文件不存在" % file_path)
    return os.path.basename(file_path)

def _at_log_req_and_rep(req_and_resp):
    '''
    Log request and response。
   【reqAndRes】: 收集request和response的字典
    '''
    if req_and_resp.get(_REQ) is not None:
        req=req_and_resp.get(_REQ)
        if req.get(_URI) is not None:
            logger.info('Request url: ' + req[_URI], html=isWriteHtml, also_console=also_console)
        if req.get(_METHOD) is not None:
            logger.info('Request method: ' + req[_METHOD], html=isWriteHtml, also_console=also_console)
        if req.get(_PARAMS) is not None:
            logger.info('Request parameters: ' + req[_PARAMS], html=isWriteHtml, also_console=also_console)
        if req.get(_HEADER) is not None:
            logger.info('Request header: ' + req[_HEADER], html=isWriteHtml, also_console=also_console)
        if req.get(_BODY) is not None:
            logger.info('Request body: ' + req[_BODY], html=isWriteHtml, also_console=also_console)

    if req_and_resp.get(_RESP) is not None:
        resp = req_and_resp.get(_RESP)
        if resp.get(_STATUS_CODE) is not None:
            logger.info('Response status code: ' + str(resp[_STATUS_CODE]), html=isWriteHtml, also_console=also_console)
        if resp.get(_HEADER) is not None:
            try:
                if isinstance(resp.get(_HEADER),dict) or isinstance(resp.get(_HEADER),list):
                    header=jsonUtils.dumps(resp.get(_HEADER),ensure_ascii=False)
                    logger.info('Response header: ' + header, html=isWriteHtml, also_console=also_console)
                if isinstance(resp.get(_HEADER), str):
                    logger.info('Response header: ' + resp[_HEADER], html=isWriteHtml, also_console=also_console)
            except:
                logger.info('Response header: ' + str(resp[_HEADER]), html=isWriteHtml, also_console=also_console)
        if resp.get(_BODY) is not None:
            logger.info('Response body: ' + resp[_BODY], html=isWriteHtml, also_console=also_console)

def at_quote(string):
    '''
    编码。url encode。目前requests header不支持中文。因此需要编码。
    暂时只暴露代码关键字。
    [string]: String类型。需要编码的值。
    RETURN: 编码后的String，String类型

    Examples:
        |   关键字  |  参数 |            结果     |
        | at quote | 哈哈  | %E5%93%88%E5%93%88  |
    '''
    return parse.quote(string)

def at_unquote(string):
    '''
    解码。url decode。暂时只暴露代码关键字。
    [string]: String类型。需要解码的值。
    RETURN: 解码后的String，String类型

    Examples:
        |   关键字    |           参数       |  结果  |
        | at unquote | %E5%93%88%E5%93%88  |   哈哈 |
    '''
    return parse.unquote(string)
