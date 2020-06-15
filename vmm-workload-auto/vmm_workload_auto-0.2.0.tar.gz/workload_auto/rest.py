# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
#

'''
File containing REST handlers.
'''

from flask import Flask, json

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/workload_auto/clean', methods=['POST'])
def workload_clean():
    '''
    Handler to clean up the network attachments.
    '''
    GLOB_CB("CLEAN", None)
    return json.dumps({"success": True}), 201

@api.route('/workload_auto/refresh', methods=['POST'])
def workload_refresh():
    '''
    Handler to re-read the config file contents and re-apply the network
    attachments.
    '''
    GLOB_CB("REFRESH", None)
    return json.dumps({"success": True}), 201

@api.route('/workload_auto/resync', methods=['POST'])
def workload_resync():
    '''
    Handler to re-discover the neighbours and redo the network attachments
    if needed.
    '''
    GLOB_CB("RESYNC", None)
    return json.dumps({"success": True}), 201

GLOB_CB = None

def rest_init(port, cb_arg):
    '''
    Top level REST init routine.
    '''
    global GLOB_CB

    GLOB_CB = cb_arg
    api.run(host='0.0.0.0', port=port)
