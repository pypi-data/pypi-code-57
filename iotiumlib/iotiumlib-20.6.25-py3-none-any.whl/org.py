"""
// ========================================================================
// Copyright (c) 2018-2019 Iotium, Inc.
// ------------------------------------------------------------------------
// All rights reserved.
//
// ========================================================================
"""

__author__ = "Rashtrapathy"
__copyright__ = "Copyright (c) 2018-2019 by Iotium, Inc."
__license__ = "All rights reserved."
__email__ = "rashtrapathy.c@iotium.io"

from iotiumlib.requires.commonWrapper import *
from iotiumlib.requires.resourcePayload import *

orgId = str()

class org(object):
    def __init__(self, action, payload=None, org_id=None, filters=None):

        if payload is None:
            payload = {}

        def get_org(uri):
            return org.Org(self, method='get', uri=uri)

        def getv2_org(uri):
            return org.Org(self, method='getv2', uri=uri, filters=filters)

        def get_org_name_org(uri):
            return org.Org(self, method='get', uri=uri)

        def get_org_id_org(uri):
            return org.Org(self, method='get', uri=uri)

        def add_org(uri):
            return org.Org(self, method='post', uri=uri)

        def edit_org(uri):
            return org.Org(self, method='put', uri=uri)

        def delete_org(uri):
            return org.Org(self, method='delete', uri=uri)


        _function_mapping = {
            'get' : get_org,
            'getv2': getv2_org,
            'add' : add_org,
            'edit' : edit_org,
            'delete':delete_org,
            'get_org_id': get_org_id_org,
            'get_org_name': get_org_name_org,
        }

        self.uri = {
            get_org: 'api/v1/org',
            get_org_name_org:'api/v1/user/current',
            getv2_org: 'api/v2/org',
            add_org: 'api/v1/org',
            edit_org: 'api/v1/org/{orgId}',
            delete_org: 'api/v1/org/{orgId}',
            get_org_id_org: 'api/v1/org/{orgId}',
        }

        self.payload = resourcePaylod.Organisation(payload).__dict__

        self.orgId = orch.id

        self.Response = Response()

        _wrapper_fun = _function_mapping[action]
        args = '{}_org'.format(action)
        _wrapper_fun(self.uri[eval(args)])

    def Org(self, method, uri, filters=None):

        respOp = dict()
        paramRequired = checkforUriParam(uri)
        if paramRequired:
            for param in paramRequired:
                uri = re.sub(r'{{{}}}'.format(param), eval('self.{}'.format(param)), uri)

        if method == 'get':
            respOp = getApi(formUri(uri))
        elif method == 'getv2':
            self.Response = getApiv2(formUri(uri), filters)
            return self.Response
        elif method == 'post':
            respOp = postApi(formUri(uri), self.payload)
        elif method == 'put':
            respOp = putApi(formUri(uri), self.payload)
        elif method == 'delete':
            respOp = deleteApi(formUri(uri))
        else:
            return self.Response
        self.Response.output = respOp.json()
        self.Response.code = respOp.status_code
        return self.Response

def get(org_id=""):
    if org_id is not None:
        return org(action='get_org_id', org_id=org_id)
    elif org_id is None:
        return org(action='get_org_name')
    else:
        return org(action='get')

def getv2(filters=None):
    return org(action='getv2', filters=filters)

def add(org_name, billing_name, billing_email,
        domain_name="", timezone="",
        headless_mode=False, two_factor=False, vlan_support=False):
    return org(action="add", payload=locals())


def delete(org_id):
    return org(action="delete", org_id= org_id, payload=locals())

