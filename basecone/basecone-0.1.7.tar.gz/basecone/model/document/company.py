import json

class Company():
  def __init__(self, id, code):
    self.id = id
    self.code = code

  @classmethod
  def from_dict(cls, data):
    return cls(
      id = data['companyId'],
      code = data['companyCode'],
    )