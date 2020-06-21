import httplib
import json
import requests
class BaseObject:
  def from_dict(self, d):
    if 'appliance_url' in d:
      self.appliance_url = d['%!s(MISSING)']
    if 'api_key' in d:
      self.api_key = d['%!s(MISSING)']
    if 'sec_key' in d:
      self.sec_key = d['%!s(MISSING)']
    if 'insecure' in d:
      self.insecure = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['appliance_url'] = self.appliance_url
    d['api_key'] = self.api_key
    d['sec_key'] = self.sec_key
    d['insecure'] = self.insecure
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def __init__(self, appliance_url, api_key, sec_key, insecure = False):
    if appliance_url.startswith("http://") or appliance_url.startswith("https://"):
      # all good
      pass
    else:
      appliance_url = "https://" + appliance_url
    self.appliance_url = appliance_url
    self.api_key = api_key
    self.sec_key = sec_key
    self.insecure = insecure
  

    
  def make_headers(self):
    return {
      'Authorization': 'Token token="' + str(self.api_key) + str(self.sec_key) + '"',
      'Content-Type': 'application/json'
    }
  

    
  def http_get(self, path):
    url = str(self.appliance_url) + path
    headers = self.make_headers()
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      raise response.text
    return response.json()
  

    
  def http_post(self, path, body):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.post(url, data=body, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
      return response.json()
    raise response.txt
  

    
  def http_put(self, path, body):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.put(url, data=body, headers=headers)
    if response.status_code != 204:
      raise response.text
    return response.json()
  

    
  def http_delete(self, path):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
      raise response.text
    return response.json()
  

class Account(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def connection_managers(self):
    obj = self.http_get("/api/v2/connection_managers.json")
    list = []
    for x in obj:
      elem = ConnectionManager(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.hostname = x["hostname"]
      elem.last_contact = x["last_contact"]
      list.append(elem)
    return list
  

    
  def connection_manager_groups(self):
    obj = self.http_get("/api/v2/connection_manager_groups.json")
    list = []
    for x in obj:
      elem = ConnectionManagerGroup(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

    
  def new_environment(self):
    return Environment(self.appliance_url, self.api_key, self.sec_key, self.insecure)
  

    
  def environments(self):
    obj = self.http_get("/api/v2/environments.json")
    list = []
    for x in obj:
      elem = Environment(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

    
  def events_with_view_name(self, view_name):
    url = "/api/v2/events.json%!!(MISSING)S(string=?view_name=" + str(view_name) + ")"
    obj = http_get(url)
    list = []
    for x in list:
      elem = Event(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.type_id = x["type_id"]
      elem.environment_id = x["environment_id"]
      elem.created_at = x["created_at"]
      list.append(elem)
    return list
  

    
  def events_with_query(self, query):
    url = "/api/v2/events.json%!!(MISSING)S(string=?query=" + str(query) + ")"
    obj = http_get(url)
    list = []
    for x in list:
      elem = Event(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.type_id = x["type_id"]
      elem.environment_id = x["environment_id"]
      elem.created_at = x["created_at"]
      list.append(elem)
    return list
  

    
  def event_actions(self):
    obj = self.http_get("/api/v2/event_actions.json")
    list = []
    for x in obj:
      elem = EventAction(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      elem.status = x["status"]
      elem.type = x["type"]
      list.append(elem)
    return list
  

    
  def incidents(self):
    obj = self.http_get("/api/v2/incidents.json")
    list = []
    for x in obj:
      elem = Incident(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.external_id = x["external_id"]
      elem.short_description = x["short_description"]
      elem.started_at = x["started_at"]
      elem.ended_at = x["ended_at"]
      elem.url = x["url"]
      list.append(elem)
    return list
  

    
  def jobs(self):
    obj = self.http_get("/api/v2/jobs.json")
    list = []
    for x in obj:
      elem = Job(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.organisation_id = x["organisation_id"]
      elem.source_id = x["source_id"]
      elem.source_type = x["source_type"]
      elem.status = x["status"]
      list.append(elem)
    return list
  

    
  def new_node(self):
    return Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/nodes.json")
    list = []
    for x in obj:
      elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      elem.external_id = x["external_id"]
      elem.environment_id = x["environment_id"]
      elem.operating_system_family_id = x["operating_system_family_id"]
      elem.operating_system_id = x["operating_system_id"]
      list.append(elem)
    return list
  

    
  def node_groups(self):
    obj = self.http_get("/api/v2/node_groups.json")
    list = []
    for x in obj:
      elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

    
  def operating_system_families(self):
    obj = self.http_get("/api/v2/operating_system_families.json")
    list = []
    for x in obj:
      elem = OperatingSystemFamily(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

    
  def operating_systems(self):
    obj = self.http_get("/api/v2/operating_systems.json")
    list = []
    for x in obj:
      elem = OperatingSystem(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      elem.operating_system_family_id = x["operating_system_family_id"]
      list.append(elem)
    return list
  

    
  def system_metrics(self):
    obj = self.http_get("/api/v2/system_metrics.json")
    list = []
    for x in obj:
      elem = SystemMetric(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.metric = x["metric"]
      elem.value = x["value"]
      elem.timestamp = x["timestamp"]
      list.append(elem)
    return list
  

    
  def users(self):
    obj = self.http_get("/api/v2/users.json")
    list = []
    for x in obj:
      elem = User(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      elem.surname = x["surname"]
      elem.email = x["email"]
      elem.role = x["role"]
      list.append(elem)
    return list
  

    
  def invite_user(self, email, role):
    url = "/api/v2/users/invite.json?email=" + str(email) + "&role=" + str(role) + ""
    obj = http_post(url, None)
    return obj
  

    
  def find_node_by_external_id(self, external_id):
    url = "/api/v2/nodes/lookup.json?external_id=" + str(external_id) + ""
    obj = http_get(url)
    id = obj["node_id"]
    elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def find_node_by_name(self, name):
    url = "/api/v2/nodes/lookup.json?name=" + str(name) + ""
    obj = http_get(url)
    id = obj["node_id"]
    elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def find_node_by_id(self, id):
    url = "/api/v2/nodes/{id}.json?id=" + str(id) + ""
    obj = http_get(url)
    elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.from_hash(obj)
    return elem

class ConnectionManager(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'hostname' in d:
      self.hostname = d['%!s(MISSING)']
    if 'last_contact' in d:
      self.last_contact = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['hostname'] = self.hostname
    d['last_contact'] = self.last_contact
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def connection_manager_group(self):
    obj = self.http_get("/api/v2/connection_manager_groups/{connection_manager_group_id}.json")
    elem = ConnectionManagerGroup(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

class ConnectionManagerGroup(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def connection_managers(self):
    obj = self.http_get("todo")
    list = []
    for x in obj:
      elem = ConnectionManager(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

class Environment(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
    if 'organisation_id' in d:
      self.organisation_id = d['%!s(MISSING)']
    if 'short_description' in d:
      self.short_description = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['organisation_id'] = self.organisation_id
    d['short_description'] = self.short_description
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def load(self):
    obj = self.http_get("/api/v2/environments/{id}.json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/environments.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    del d["id"]
    del d["organisation_id"]
    self.http_put("/api/v2/environments/{id}.json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/environments/{id}.json")
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/environments/{id}/nodes.json")
    list = []
    for x in obj:
      elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

class Event(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'type_id' in d:
      self.type_id = d['%!s(MISSING)']
    if 'environment_id' in d:
      self.environment_id = d['%!s(MISSING)']
    if 'created_at' in d:
      self.created_at = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['type_id'] = self.type_id
    d['environment_id'] = self.environment_id
    d['created_at'] = self.created_at
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def environment(self):
    obj = self.http_get("/api/v2/environments/" + str(self.environment_id) + ".json")
    elem = Environment(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    elem.organisation_id = obj["organisation_id"]
    elem.short_description = obj["short_description"]
    elem.node_rules = obj["node_rules"]
    return elem
  

class EventAction(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
    if 'status' in d:
      self.status = d['%!s(MISSING)']
    if 'type' in d:
      self.type = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['status'] = self.status
    d['type'] = self.type
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
class Incident(BaseObject):
  def from_dict(self, d):
    if 'ended_at' in d:
      self.ended_at = d['%!s(MISSING)']
    if 'external_id' in d:
      self.external_id = d['%!s(MISSING)']
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'short_description' in d:
      self.short_description = d['%!s(MISSING)']
    if 'started_at' in d:
      self.started_at = d['%!s(MISSING)']
    if 'url' in d:
      self.url = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['ended_at'] = self.ended_at
    d['external_id'] = self.external_id
    d['id'] = self.id
    d['short_description'] = self.short_description
    d['started_at'] = self.started_at
    d['url'] = self.url
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
class MediumType(BaseObject):
  pass
class Node(BaseObject):
  def from_dict(self, d):
    if 'connection_manager_group_id' in d:
      self.connection_manager_group_id = d['%!s(MISSING)']
    if 'environment_id' in d:
      self.environment_id = d['%!s(MISSING)']
    if 'external_id' in d:
      self.external_id = d['%!s(MISSING)']
    if 'hostname' in d:
      self.hostname = d['%!s(MISSING)']
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'medium_hostname' in d:
      self.medium_hostname = d['%!s(MISSING)']
    if 'medium_type' in d:
      self.medium_type = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
    if 'node_type' in d:
      self.node_type = d['%!s(MISSING)']
    if 'operating_system_family_id' in d:
      self.operating_system_family_id = d['%!s(MISSING)']
    if 'operating_system_id' in d:
      self.operating_system_id = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['connection_manager_group_id'] = self.connection_manager_group_id
    d['environment_id'] = self.environment_id
    d['external_id'] = self.external_id
    d['hostname'] = self.hostname
    d['id'] = self.id
    d['medium_hostname'] = self.medium_hostname
    d['medium_type'] = self.medium_type
    d['name'] = self.name
    d['node_type'] = self.node_type
    d['operating_system_family_id'] = self.operating_system_family_id
    d['operating_system_id'] = self.operating_system_id
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def load(self):
    obj = self.http_get("/api/v2/nodes/{id}.json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/nodes.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    del d["id"]
    self.http_put("/api/v2/nodes/{id}.json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/nodes/{id}.json")
  

    
  def connection_manager_group(self):
    obj = self.http_get("/api/v2/connection_manager_groups/{connection_manager_group_id}.json")
    elem = ConnectionManagerGroup(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def environment(self):
    obj = self.http_get("/api/v2/environments/" + str(self.environment_id) + ".json")
    elem = Environment(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def operating_system(self):
    obj = self.http_get("/api/v2/operating_systems/{operating_system_id}.json")
    elem = OperatingSystem(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def operating_system_family(self):
    obj = self.http_get("/api/v2/operating_system_families/{operating_system_family_id}.json")
    elem = OperatingSystemFamily(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def start_scan(self, ):
    url = "/api/v2/nodes/{id}/start_scan.json"
    obj = http_post(url, None)
    return obj
  

class NodeGroup(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def load(self):
    obj = self.http_get("/api/v2/node_groups/{id}.json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/node_groups.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/node_groups/{id}.json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/node_groups/{id}.json")
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/node_groups/{id}/nodes.json")
    list = []
    for x in obj:
      elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

class NodeType(BaseObject):
  pass
class OperatingSystem(BaseObject):
  def from_dict(self, d):
    if 'description' in d:
      self.description = d['%!s(MISSING)']
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
    if 'operating_system_family_id' in d:
      self.operating_system_family_id = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['description'] = self.description
    d['id'] = self.id
    d['name'] = self.name
    d['operating_system_family_id'] = self.operating_system_family_id
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def operating_system_family(self):
    obj = self.http_get("/api/v2/operating_system_families/{operating_system_family_id}.json")
    elem = OperatingSystemFamily(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

class OperatingSystemFamily(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def operating_systems(self):
    obj = self.http_get("/api/v2/operating_system_families/{id}/operating_systems.json")
    list = []
    for x in obj:
      elem = OperatingSystem(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.name = x["name"]
      list.append(elem)
    return list
  

class ScheduledJob(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'source_id' in d:
      self.source_id = d['%!s(MISSING)']
    if 'source_name' in d:
      self.source_name = d['%!s(MISSING)']
    if 'source_type' in d:
      self.source_type = d['%!s(MISSING)']
    if 'status' in d:
      self.status = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['source_id'] = self.source_id
    d['source_name'] = self.source_name
    d['source_type'] = self.source_type
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def load(self):
    obj = self.http_get("/api/v2/scheduledu_jobs/{id}.json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/scheduled_jobs.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/scheduled_jobs/{id}.json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/scheduled_jobs/{id}.json")
  

    
  def cancel_jobs(self, ):
    url = "/api/v2/scheduled_jobs/{id}/cancel_jobs.json"
    obj = http_post(url, None)
    return obj
  

class SystemMetric(BaseObject):
  def from_dict(self, d):
    if 'metric' in d:
      self.metric = d['%!s(MISSING)']
    if 'value' in d:
      self.value = d['%!s(MISSING)']
    if 'timestamp' in d:
      self.timestamp = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['metric'] = self.metric
    d['value'] = self.value
    d['timestamp'] = self.timestamp
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
class User(BaseObject):
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['%!s(MISSING)']
    if 'name' in d:
      self.name = d['%!s(MISSING)']
    if 'surname' in d:
      self.surname = d['%!s(MISSING)']
    if 'email' in d:
      self.email = d['%!s(MISSING)']
    if 'role' in d:
      self.role = d['%!s(MISSING)']
    if 'invited' in d:
      self.invited = d['%!s(MISSING)']
    if 'last_sign_in_at' in d:
      self.last_sign_in_at = d['%!s(MISSING)']
    if 'expiry' in d:
      self.expiry = d['%!s(MISSING)']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['surname'] = self.surname
    d['email'] = self.email
    d['role'] = self.role
    d['invited'] = self.invited
    d['last_sign_in_at'] = self.last_sign_in_at
    d['expiry'] = self.expiry
    return d
  def to_json(self):
    d = self.to_dict
    return json.saves(d)
    
  def update_role(self, role):
    url = "/api/v2/users/update_role.json?role=" + str(role) + ""
    obj = self.http_put(url, nil)
    return obj

