# coding=utf-8
from __future__ import absolute_import

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import datetime
import json
import logging

import requests

from ..common.utils import CommonUtlis, CommonParams

logger = logging.getLogger(__file__)


class Auth(object):
    def __init__(self, accessKey, accessSecret, SysAccessKey, SysAccessSecret, dryOn=u'false'):
        self.dryOn = dryOn
        self.accessKey = accessKey
        self.accessSecret = accessSecret
        self.SysAccessKey = SysAccessKey
        self.SysAccessSecret = SysAccessSecret

    def getSignedHeader(self, headerMap):
        if not self.checkHeaders(headerMap):
            return
        return CommonUtlis.getSignedHeader(headerMap)

    def getSignatureHeader(self, dryOn=u"false", accessKey=u"", SysAccessKey=u"",
                           accessSecret=u"", SysAccessSecret=u"",
                           host=u"", httpMethod=u"", url=u"", queryString=u"",
                           body=u"", headers=None):
        if not headers:
            headers = dict()
        headers[CommonParams.X_NSF_SIGNATURE_METHOD] = CommonParams.SIGNATURE_METHOD
        headers[CommonParams.X_NSF_SIGNATURE_VERSION] = CommonParams.SIG_VERSION_V1
        headers[CommonParams.X_NSF_DryRun] = dryOn
        headers[CommonParams.X_NSF_SIGNATURE_NONCE] = CommonUtlis.getRandomNum(64)  # 随机64 位数
        headers[CommonParams.X_NSF_AccessKey] = accessKey
        headers[CommonParams.X_SYS_AccessKey] = SysAccessKey
        # 获取时间 格式为 %Y-%m-%dT%H:%M:%SZ
        headers[CommonParams.X_NSF_DATE] = datetime.datetime.utcnow().strftime(CommonParams.ISO8601_DATE_TIME_FORMATTER)
        host = host.split(u":")[0]
        headers[CommonParams.HOST] = host
        canonicalQueryString = CommonUtlis.getCanonicalQueryString(queryString)
        canonicalHeader = CommonUtlis.getCanoicalHeader(headers)

        signedHeader = CommonUtlis.getSignedHeader(headers)

        hashBody = CommonUtlis.getHashBodyHex(body)
        string2Sign = "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (
            CommonParams.SIGNATURE_METHOD, httpMethod, url, canonicalQueryString, canonicalHeader, signedHeader,
            hashBody
        )
        signature = CommonUtlis.generateSignature(accessSecret, string2Sign, u"HmacSHA256")
        headers[CommonParams.X_NSF_SIGNED_HEADERS] = signedHeader
        headers[CommonParams.X_NSF_SIGNATURE] = signature
        # 获取子系统的signature
        SysSignature = CommonUtlis.generateSignature(SysAccessSecret, string2Sign, u"HmacSHA256")
        headers[u"myhost"] = host
        headers[u"url"] = url
        headers[CommonParams.X_SYS_SIGNATURE] = SysSignature

        return headers

    def checkHeaders(self, headerMap):
        return set(headerMap).issuperset(CommonParams.StandardardHeader)

    def GetHeader(self):
        u"""
        加密获取请求头信息
        :return:
        """
        url = u'/' + u"/".join(self.url.split(u'/')[3:])
        print u"我是url: %s" %(url)
        return self.getSignatureHeader(dryOn=self.dryOn, accessKey=self.accessKey,
                                       accessSecret=self.accessSecret,
                                       SysAccessKey=self.SysAccessKey,
                                       SysAccessSecret=self.SysAccessSecret,
                                       host=self.host, httpMethod=self.httpMethod, url=url,
                                       queryString=self.queryString,
                                       body=self.body, headers=self.headers)

    def request(self, method, url, params=None, body=None, headers={u"content-type": u"application/json"}, ):
        self.url = url
        self.queryString = params
        self.headers = headers
        self.body = body
        self.host = url.split(u'/')[2]
        self.httpMethod = method
        self.request_headers = self.GetHeader()
        dic = {u'url': url, u'data': self.body, u'headers': self.request_headers, u'params': self.queryString}
        if self.httpMethod == u"POST":
            print dic
            res = requests.post(**dic)
        elif self.httpMethod == u"DELETE":
            res = requests.delete(**dic)
        elif self.httpMethod == u"PUT":
            res = requests.put(**dic)
        else:
            res = requests.get(**dic)
        try:
            content = CommonUtlis.unicode_convert(json.loads(res.content.decode(u'utf-8')))
        except Exception, e:
            content = res.content
        return content
