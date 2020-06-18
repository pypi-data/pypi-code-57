import json
import pkg_resources


def getRules():
  #with open(pkg_resources.resource_string(__name__, 'rules.json'), 'r') as f:
  return json.loads(pkg_resources.resource_string(__name__, 'rules.json'))
  #return rules
    
