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

import re

def get_resource_by_label(resource, labelname):

    resource_name_list = []

    reObjLabel = re.compile('.+?Label')

    resource_details_op = resource.getv2().Response.formattedOutput

    if not resource_details_op:
        return False

    for n in resource_details_op:
        resource_dict = dict()
        for key in list(n.keys()):
            if reObjLabel.match(key):
                for l in n[key].split(','):
                    if l == labelname:
                        keyList = list(n.keys())
                        for i, item in enumerate(keyList):
                            if re.search('{}.+?'.format(resource.__name__.rsplit('.')[1]), item.lower()):
                                resource_dict.update({item:n[item]})
                        resource_name_list.append(resource_dict)
    return resource_name_list

def get_resource_id_by_name(resource, name):
    resourceId = str()
    resource_details_op = resource.getv2().Response.output
    if resource_details_op:
        try:
            itemList = next((item for item in resource_details_op if item["name"] == name))
            resourceId = itemList['id']
            return str(resourceId)
        except StopIteration as E:
            return resourceId
    else:
        return resourceId

def get_all_networks_from_node(name):

    from iotiumlib import node

    str1 = list(dict())

    node_details_op = node.getv2().Response.output
    if node_details_op is False:
        return False
    try:
        itemList = next((item for item in node_details_op if item["name"] == name))
    except StopIteration:
        return False

    if 'networks' in itemList:
        for network in itemList['networks']:
            if network['name']:
                networkId = network['id']
                networkName = network['name']
                str1.append({networkName:networkId})
        return str1

def get_resource_name_by_id(resource, id):
    resourceName = str()
    resource_details_op = resource.getv2().Response.output
    if resource_details_op:
        try:
            itemList = next((item for item in resource_details_op if item["id"] == id))
            resourceName = itemList['name']
            return str(resourceName)
        except StopIteration as E:
            return resourceName
    else:
        return resourceName

