# coding=utf-8
import sys
import os
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from utils.system import get_ip_address, get_linux_nvme_devs, get_automation_platform
from test_framework.state import State
from test_framework.state import NodeState
from tool.device import NVME


class StateResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        data = []
        state = NodeState.verdicts_map[self.test_pool.get_current_node_state()]
        ip_ = get_ip_address()
        if "win" in sys.platform:
            system_name = "windows"
            device = NVME()
            dev_list = device.list_dev()
        else:
            system_name = "linux"
            dev_list = get_linux_nvme_devs()
        data.append(state)
        data.append(ip_)
        data.append(system_name)
        if not dev_list:
            dev_list = list()
            dev = {"index": -1, "name": "not find device"}
            dev_list.append(dev)
        data.append(dev_list)
        data.append(get_automation_platform())
        result = {
            "data": data,
            "state": State.PASS
        }
        return result
