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
from sheetgear.bridge.xargs import (create_spreadsheet_argspec, extract_spreadsheet_args)
from sheetgear.bridge.client import Handler as SpreadsheetHandler

def main():

  results = dict(changed=False)

  argument_spec = create_spreadsheet_argspec()

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  if module.check_mode:
    module.exit_json(**results)

  constructor_args = extract_spreadsheet_args(module.params)

  try:
    results['credentials'] = SpreadsheetHandler(**constructor_args).loadToken()
    module.exit_json(**results)
  except Exception as err:
    module.fail_json(msg=convert_error_to_module_output(__file__, err), **results)

if __name__ == '__main__':
  main()
