#!/usr/bin/env python3
#
# Sheetgear Lookup Plugin
#
# A simple example of using the sheetgear plugin in a role:
#    ---
#    - debug: msg="{{ lookup('sheetgear', 'showinfo', dict()) }}"
#
# The plugin must be run with SHEETGEAR_CREDENTIALS_FILE and SHEETGEAR_TOKEN_FILE set and exported.
#
# The plugin can be run manually for testing:
#   python ansible/plugins/lookup/sheetgear.py count '{"spreadsheet_id": "1YZmd9xR4r5ZxcQtkh5aeDe0SYUt6RwrhX9DssRQ1v4c"}'
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
  lookup: sheetgear
  author: sheetgear <sheetgear@gmail.com>
  version_added: "0.1.0"
  short_description: get the number of rows and fetch data from these rows of a grid range in a spreadsheet
  description:
      - This lookup returns the number and data of rows in a grid range.
  options:
    _terms:
      subtask_name: name of the subtask, either 'count' or 'fetch'
      required: True
  notes:
    - nothing
"""

# for development only
import os, sys
if 'SHEETGEAR_BRIDGE_HOME' in os.environ:
  sys.path.insert(0, os.environ['SHEETGEAR_BRIDGE_HOME'])

import json

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from sheetgear.bridge.client import Handler as SpreadsheetHandler
from sheetgear.bridge.utils import pick_object_fields
from sheetgear.bridge.xargs import (
      extract_spreadsheet_args,
      extract_sheet_args,
      extract_frame_range_args,
      extract_range_fetch_args,
)

display = Display()

class LookupModule(LookupBase):

  def run(self, terms, variables=None, **kwargs):
    ret = []

    if len(terms) == 0:
      raise AnsibleError("A subtask name ('count', 'fetch') must be provided")
    _subtask_name = terms[0]

    if len(terms) <= 1:
      raise AnsibleError("The sheetgear parameters must be provided")
    _parameters = terms[1]

    if not isinstance(_parameters, dict):
      raise AnsibleError("The sheetgear parameters must be a dictionary object")

    # get the spreadsheet info
    if _subtask_name == 'spreadsheet_info':
      constructor_args = extract_spreadsheet_args(_parameters)
      self.__vvvv(_subtask_name, constructor_args)

      ret.append(SpreadsheetHandler(**constructor_args).properties)
      return ret

    # get the sheet properties
    if _subtask_name == 'sheet_properties':
      constructor_args, sheet_args = extract_sheet_args(_parameters)
      self.__vvvv(_subtask_name, constructor_args, sheet_args)

      ret.append(SpreadsheetHandler(**constructor_args).openSheet(**sheet_args).sheet_properties)
      return ret

    # get the length of a frame
    if _subtask_name in ['count', 'range_count', 'range_length']:
      _subtask_name = 'range_count'
      constructor_args, sheet_args, action_args = extract_frame_range_args(_parameters)
      self.__vvvv(_subtask_name, constructor_args, sheet_args, action_args)

      ret.append(SpreadsheetHandler(**constructor_args).openSheet(**sheet_args).count(**action_args))
      return ret

    # fetch the data of a frame
    if _subtask_name in ['fetch', 'range_fetch', 'range_data']:
      _subtask_name = 'range_fetch'
      constructor_args, sheet_args, action_args = extract_range_fetch_args(_parameters)
      self.__vvvv(_subtask_name, constructor_args, sheet_args, action_args)
      _result = SpreadsheetHandler(**constructor_args).openSheet(**sheet_args).fetch(**action_args)

      if kwargs.get('wantlist', False):
        ret = _result['data']
      else:
        ret.append(_result)
      return ret

    # show the context of the lookup call
    ret.append(
      dict(
        terms=terms,
        variables=pick_object_fields(variables, [
          'ansible_connection',
          'ansible_version',
          'ansible_check_mode',
          'ansible_diff_mode',
          'ansible_inventory_sources',
          'ansible_run_tags',
          'ansible_skip_tags',
          'ansible_play_name',
          'ansible_play_hosts',
          'ansible_python_interpreter',
          'inventory_hostname',
          'playbook_dir',
          'environment',
        ]),
        options=kwargs
      )
    )
    return ret

  def __vvvv(self, action_name, constructor_args=None, sheet_args=None, action_args=None):
    if isinstance(constructor_args, dict):
      display.vvvv(u"create a SpreadsheetHander with id: {spreadsheet_id}".format(**constructor_args))

    if isinstance(action_args, dict):
      _action_msg = None
      if action_name == 'range_count':
        _action_msg = u"count total of rows in the grid range: {frame_range}"
      if action_name == 'range_fetch':
        _action_msg = u"fetch rows in the grid range: {frame_range}"

      if isinstance(_action_msg, str):
        display.vvvv(_action_msg.format(**action_args))
    pass

def main(argv=sys.argv[1:]):
  if len(argv) <= 1:
    print("Usage: sheetgear.py sub_task_name params_json_object")
    return -1

  newargv = [ argv[0], json.loads(argv[1]) ]

  print(LookupModule().run(newargv, {}))
  return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
