#coding=utf-8
from __future__ import absolute_import
import hashlib
import hmac
import re
import urllib2, urllib, urlparse
from random import Random

from .decorators import exceptionHandler


class CommonParams(object):
    SIGNATURE_METHOD = u"HMAC-SHA256"
    SIG_VERSION_V1 = u"1.0"
    X_NSF_DATE = u"X-NSF-Date"
    X_NSF_SIGNED_HEADERS = u"X-NSF-SignedHeaders"
    X_NSF_SIGNATURE_VERSION = u"X-NSF-SignatureVersion"
    X_NSF_SIGNATURE_METHOD = u"X-NSF-SignatureMethod"
    X_NSF_SIGNATURE_NONCE = u"X-NSF-SignatureNonce"
    X_NSF_DryRun = u"X-NSF-DryRun"
    X_NSF_AccessKey = u"X-NSF-AccessKey"
    X_SYS_AccessKey = u"X-SYS-AccessKey"
    X_NSF_AccessSecret = u"X-NSF-AccessSecret"
    X_NSF_SIGNATURE = u"X-NSF-Signature"
    X_SYS_SIGNATURE = u"X-SYS-Signature"
    HOST = u"host"
    ISO8601_DATE_TIME_FORMATTER = u"%Y-%m-%dT%H:%M:%SZ"
    StandardardHeader = (X_NSF_DATE, X_NSF_SIGNATURE_VERSION, X_NSF_SIGNATURE_METHOD, X_NSF_SIGNATURE_NONCE,
                         X_NSF_DryRun, X_NSF_AccessKey, HOST)


class CommonUtlis(object):
    pattern = re.compile(u"\s+")
    EMPTY_STRING = u""

    @classmethod
    def getRandomNum(cls, length):
        r = Random()
        length = 1 if length <= 0 else length
        array = [unicode(r.randrange(0, 10)) for i in xrange(length)]
        return u"".join(array)

    @classmethod
    def getCanonicalQueryString(cls, queryString):
        if not queryString:
            return u""
        parameters = dict()
        array = queryString.split(u"&")
        for param in array:
            keyValue = param.split(u"=")
            if not keyValue:
                continue
            key = keyValue[0]
            if len(key) == 0:
                parameters[key] = cls.EMPTY_STRING
            else:
                parameters[key] = keyValue[1]
        sortedKeys = list(parameters)
        if not sortedKeys:
            return cls.EMPTY_STRING
        sortedKeys.sort()
        res = u""
        for key in sortedKeys:
            value = cls.__percentEncode(key)
            res = "%s&%s=%s" %(res,value,parameters[key])
        return res[1:]

    @classmethod
    def getCanoicalHeader(cls, headerMap):
        signedHeadSet = set(headerMap)
        headers = dict()
        for headerName in signedHeadSet:
            value = headerMap.get(headerName)
            headers[headerName.lower()] = value
        headerNames = list(headers)
        headerNames.sort()
        # headerNames.sort()
        canonicalHeaders = u"".join(["%s:%s\n"%(headerName,cls.trimall(headers[headerName])) for headerName in headerNames])
        return canonicalHeaders

    @classmethod
    def __percentEncode(cls, value):
        if not value:
            return value
        return urllib.quote(value)

    @classmethod
    def trimall(cls, value):
        if not value:
            return cls.EMPTY_STRING
        return value.strip()
        # return re.sub(cls.pattern, value.strip(), " ")

    @classmethod
    @exceptionHandler(result=None)
    def getHashBodyHex(cls, value):
        md = hashlib.sha256()
        if not isinstance(value,unicode):
            value = value.encode(encoding=u"utf-8")
        md.update(value)
        return md.hexdigest()

    @classmethod
    @exceptionHandler(result=u"")
    def getSignedHeader(cls, headers):
        signedHeadSet = set(headers)
        signedHeaderString = u"".join([signedString.lower() + u";" for signedString in signedHeadSet])
        return signedHeaderString[:-1]

    @classmethod
    @exceptionHandler(result=u"")
    def generateSignature(cls, secret, stringToSign, algorithm = u'SHA256'):
        # algorithm = hashlib.new(algorithm)
        return cls.__hmac(secret.encode(u'utf-8'), stringToSign.encode(u'utf-8'), algorithm)

    @classmethod
    def __hmac(cls, secretBytes, stringToSign, algorithm):
        signature = hmac.new(secretBytes, stringToSign, digestmod=hashlib.sha256).hexdigest()
        return signature

    @classmethod
    def __HmacSHA256(cls, secretBytes, stringToSign):
        signature = hmac.new(unicode(secretBytes).encode(u'utf-8'),unicode(stringToSign).encode(u'utf-8'),
                             digestmod=hashlib.sha256).digest()
        return signature.hex().lower()

    @classmethod
    def unicode_convert(cls,input):
        if isinstance(input, dict):
            return {cls.unicode_convert(key): cls.unicode_convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [cls.unicode_convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
