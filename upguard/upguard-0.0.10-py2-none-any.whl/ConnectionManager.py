import json
from .BaseObject import BaseObject
class ConnectionManager(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.channels = None
    self.connection_manager_group_id = None
    self.created_at = None
    self.id = None
    self.hostname = None
    self.last_contact = None
    self.stats = None
    self.updated_at = None
  def from_dict(self, d):
    if 'channels' in d:
      self.channels = d['channels']
    if 'connection_manager_group_id' in d:
      self.connection_manager_group_id = d['connection_manager_group_id']
    if 'created_at' in d:
      self.created_at = d['created_at']
    if 'id' in d:
      self.id = d['id']
    if 'hostname' in d:
      self.hostname = d['hostname']
    if 'last_contact' in d:
      self.last_contact = d['last_contact']
    if 'stats' in d:
      self.stats = d['stats']
    if 'updated_at' in d:
      self.updated_at = d['updated_at']
  def to_dict(self):
    d = {}
    d['channels'] = self.channels
    d['connection_manager_group_id'] = self.connection_manager_group_id
    d['created_at'] = self.created_at
    d['id'] = self.id
    d['hostname'] = self.hostname
    d['last_contact'] = self.last_contact
    d['stats'] = self.stats
    d['updated_at'] = self.updated_at
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def connection_manager_group(self):
    obj = self.http_get("/api/v2/connection_manager_groups/{connection_manager_group_id}.json")
    elem = ConnectionManagerGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

