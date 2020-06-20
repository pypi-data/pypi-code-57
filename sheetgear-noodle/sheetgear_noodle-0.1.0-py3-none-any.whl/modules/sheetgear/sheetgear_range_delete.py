#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

RETURN = r'''
# only defaults
'''

# for development only
import os, sys
if 'SHEETGEAR_BRIDGE_HOME' in os.environ:
  sys.path.insert(0, os.environ['SHEETGEAR_BRIDGE_HOME'])

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.sheetgear import convert_error_to_module_output
from sheetgear.bridge.xargs import (create_range_delete_argspec, extract_range_delete_args)
from sheetgear.bridge.client import Handler as SpreadsheetHandler

def main():

  results = dict(changed=False)

  argument_spec = create_range_delete_argspec()

  argument_spec.update(dict(
    shift_direction = dict(type='str', require=False, default='ROW'),
  ))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  constructor_args, sheet_args, action_args = extract_range_delete_args(module.params)

  action_args.update(dict(options = dict(
    dry_run = module.check_mode,
    shift_direction=module.params.get('shift_direction', 'ROW')
  )))

  try:
    _packet = SpreadsheetHandler(**constructor_args).openSheet(**sheet_args).delete(**action_args)
    if hasattr(_packet, 'info'):
      results['changed'] = True
    results['packet'] = _packet
    module.exit_json(**results)
  except Exception as err:
    convert_error_to_module_output(__file__, err, module, results)

if __name__ == '__main__':
  main()
