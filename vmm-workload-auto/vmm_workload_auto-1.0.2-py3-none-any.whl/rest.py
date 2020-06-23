# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
