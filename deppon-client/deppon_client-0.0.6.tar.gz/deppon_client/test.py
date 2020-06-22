# coding=utf-8
from __future__ import absolute_import

import json
import sys
from deppon_client.signature.auth import Auth

reload(sys)
sys.setdefaultencoding('utf-8')

accessKey = ''  # 网关授权的AK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
accessSecret = ''  # 网关授权的SK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
SysAccessKey = ''  # 被请求服务授权的AK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。
SysAccessSecret = ''  # 被请求服务授权的SK密钥，从配置文件中获取，保存时必须做加密处理，读取后解密操作。

def get_sys_change(AuthObj, url, queryString={}):
    method = u'GET'
    body = u""
    params = ''
    try:
        for key, value in queryString.items():
            params += key + '=' + value + '&'
        params = params[:-1]
    except:
        print u'参数有无,请参考接口文档'
        return
    headers = {u"content-type": u"application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=body, params=params)
    # 1. py2 的注释如果是中文,需要在顶部声明 coding=utf-8 ,否则会报错
    # 2. 由于py2默认是ascii码,而py3是utf8编码,所以,如果想打印时显示utf8,需要进行序列时声明utf-8,且ensure_ascii=False,否则会转换为ascii编码
    # print json.dumps(res, encoding='utf-8', ensure_ascii=False)
    return res


def post_sys_change(AuthObj, url, body):
    method = u'POST'
    queryString = u""
    body = json.dumps(body)
    headers = {u"content-type": u"application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=body, params=queryString)
    # print json.dumps(res, encoding='utf-8', ensure_ascii=False)
    return res


if __name__ == u'__main__':
    AuthObj = Auth(accessKey=accessKey, accessSecret=accessSecret, SysAccessKey=SysAccessKey,
                   SysAccessSecret=SysAccessSecret)
    # body = {u"change_type": u"蓝鲸变更", u" change_app": u"蓝鲸",
    #         u"change_user": u"T30673",
    #         u"start_time": u"2020-01-01 00:00:00",
    #         u"end_time": u"2020-01-02 00:00:00",
    #         u"change_text": u"测试变更内容"}
    # body = {u"change_type": u"蓝鲸变更123321", u" change_app": u"蓝鲸",
    #         u"change_user": u"T30672",
    #         u"start_time": u"2020-01-01 00:00:00",
    #         u"end_time": u"2020-01-02 00:00:00",
    #         u"change_text": u"新增始发线路"}
    # res = get_sys_change(AuthObj, 'http://192.168.153.1:8000/amsc/message/', body)
    # queryString = {'1': '123'}
    # post_sys_change(AuthObj,u'http://192.168.153.1:8000/amsc/message/', body)
