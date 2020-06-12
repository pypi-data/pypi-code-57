import json

class Company():
  def __init__(self, id, name, code, has_access):
    self.id = id
    self.name = name
    self.code = code
    self.has_access = has_access

  @classmethod
  def from_dict(cls, data):
    return cls(
      id = data['id'],
      name = data.get('name'),
      code = data['code'],
      has_access = bool(data.get('hasAccess'))
    )

  def to_json(self):
    return dict(
      id = self.id,
      name = self.name,
      code = self.code,
      has_access = self.has_access
    )