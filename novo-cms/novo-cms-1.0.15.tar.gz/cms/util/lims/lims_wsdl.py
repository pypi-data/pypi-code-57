#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import json

from suds.client import Client
from suds.sax.attribute import Attribute
from suds.plugin import MessagePlugin
from suds import sudsobject


reload(sys)
sys.setdefaultencoding('utf-8')


class _AttributePlugin(MessagePlugin):
    """
    Suds plug-in extending the method call with arbitrary attributes.
    """
    __module__ = __name__
    __qualname__ = '_AttributePlugin'

    def marshalled(self, context):
        methods = context.envelope.getChild('Body').getChild(
            'RunActionDirect').getChild('parameters').children
        for method in methods:
            method.attributes.append(
                Attribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'))
            method.attributes.append(
                Attribute('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema'))
            method.attributes.append(Attribute('xsi:type', 'xsd:string'))


class LIMS(object):
    def __init__(self):
        pass

    def search_stage(self, stagecode, departmentid, starttime, endtime):
        pass



uri = 'http://lims.novogene.com/STARLIMS11.novogene/Services/generic.asmx?WSDL'
client = Client(uri)

client.options.plugins = [_AttributePlugin()]

stagecode = ['P101SC17101283-01-J002', 'X101SC19123647-Z01-J004']

info_dict = {
    'stagecode': stagecode,
    'businesslinecode': '1911',
    'startTime': '2020-01-01 00:00:00',
    'endTime': '2020-06-19 00:00:00',
}

limsaccount = 'LIDANQING'
limspasswd = 'danqingli123'

parameters = client.factory.create('ArrayOfAnyType')
parameters.anyType.append(json.dumps(info_dict))

res = client.service.RunActionDirect('KF_WebServices.kf_NovoToLimsGetStagingInformation',
                                     parameters, limsaccount, limspasswd)

# res = client.service.RunActionDirect('KF_WebServices.AI_BaseQCReportsByJQ',
#                                      parameters, limsaccount, limspasswd)

for row in res.anyType:
    print(row.anyType)
