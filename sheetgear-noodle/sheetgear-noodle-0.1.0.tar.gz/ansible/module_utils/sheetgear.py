#!/usr/bin/env python3

# for development only
import os, sys
if 'SHEETGEAR_BRIDGE_HOME' in os.environ:
  sys.path.insert(0, os.environ['SHEETGEAR_BRIDGE_HOME'])

from ansible.module_utils.basic import AnsibleModule
import sheetgear.bridge.errors

def convert_error_to_module_output(filepath, err, module=None, results=dict()):
  _module_name = os.path.splitext(os.path.basename(filepath))[0]

  if isinstance(err, AssertionError):
    _msg = "The [{name}] action has failed: {msg}".format_map({
      'name': _module_name,
      'msg': str(err),
    })
    if isinstance(module, AnsibleModule):
      module.fail_json(msg=_msg, **results)
    return _msg

  _msg = "The [{name}] action has failed, error as string: {err}".format_map({
    'name': _module_name,
    'err': str(err),
  })
  if isinstance(module, AnsibleModule):
    module.fail_json(msg=_msg, **results)
  return _msg
