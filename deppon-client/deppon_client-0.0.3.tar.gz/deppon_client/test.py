#coding=utf-8
from __future__ import absolute_import
import json

from signature.auth import Auth


accessKey = ''  # 网关授权的AK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
accessSecret = ''  # 网关授权的SK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
SysAccessKey = ''  # 被请求服务授权的AK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
SysAccessSecret = ''  # 被请求服务授权的SK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。

AuthObj = Auth(accessKey=accessKey, accessSecret=accessSecret, SysAccessKey=SysAccessKey,
               SysAccessSecret=SysAccessSecret, )


def get_url(url):
    method = u'GET'
    body = u""
    queryString = u"aa=bb&cc=dd"
    headers = {u"content-type": u"application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=body)
    print res

def post_url(url):
    method = u'POST'
    body = json.dumps({u"name":u"测试4",u"user":u"354619"})
    # json.dumps({u"name":u"测试4",u"user":u"354619"})
    queryString = u""
    headers = {u"content-type": u"application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=body, params=queryString)
    print res


if __name__ == u'__main__':
    # res = get_url('http://192.168.153.1:8000/users/getuser/')
    # res = get_url('http://0.0.0.0:8000/users/getuser/')

    post_url(u'http://192.168.153.1:8000/aksk/secret_key/')
