import json
import requests


REAL_TIME_LOG_BASE_URL = 'https://realtimelog.herokuapp.com:443/'


class Client():
  """REAL-TIME log client."""


  def __init__(self, app_id):
    h = REAL_TIME_LOG_BASE_URL
    if app_id:
      self.url = h + app_id
    else:
      res = requests.get(h)
      self.url = res.url


  def get_url(self):
    return self.url


  def msg(self, data):
    requests.post(
      self.url,
      headers={'Content-Type': 'application/json'},
      data=json.dumps(data),
    )
