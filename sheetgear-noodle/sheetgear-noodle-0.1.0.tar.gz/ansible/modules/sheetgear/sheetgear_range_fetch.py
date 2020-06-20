#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community',
}

RETURN = r'''
# only defaults
'''

# for development only
import os, sys
if 'SHEETGEAR_BRIDGE_HOME' in os.environ:
  sys.path.insert(0, os.environ['SHEETGEAR_BRIDGE_HOME'])

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.sheetgear import convert_error_to_module_output
from sheetgear.bridge.xargs import (create_range_fetch_argspec, extract_range_fetch_args)
from sheetgear.bridge.client import Handler as SpreadsheetHandler

def main():

  results = dict(changed=False)

  module = AnsibleModule(argument_spec=create_range_fetch_argspec(), supports_check_mode=False)

  constructor_args, sheet_args, action_args = extract_range_fetch_args(module.params)

  try:
    results['packet'] = SpreadsheetHandler(**constructor_args).openSheet(**sheet_args).fetch(**action_args)
    module.exit_json(**results)
  except Exception as err:
    module.fail_json(msg=convert_error_to_module_output(__file__, err), **results)

if __name__ == '__main__':
  main()
