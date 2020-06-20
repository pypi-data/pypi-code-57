from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# for development only
import os, sys
if 'SHEETGEAR_BRIDGE_HOME' in os.environ:
  sys.path.insert(0, os.environ['SHEETGEAR_BRIDGE_HOME'])

from ansible import errors

import uuid

class FilterModule(object):
  def filters(self):
    return {
      'generate_uuid': self.generate_uuid
    }
  
  def generate_uuid(self, str):
    return uuid.uuid4()
