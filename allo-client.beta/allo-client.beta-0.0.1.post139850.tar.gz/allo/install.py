#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def do_install_dependencies():
    corepath = os.path.dirname(os.path.realpath(__file__))
    command = "ansible-playbook " + corepath + "/playbooks/install_allo.yml"
    oscall_result = os.system(command)
    if os.WEXITSTATUS(oscall_result) != 0:
        print("Error on dependencies installation")
        return os.WEXITSTATUS(oscall_result)
    return 0
