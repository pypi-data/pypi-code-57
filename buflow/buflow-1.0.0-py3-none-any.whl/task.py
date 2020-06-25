import buflow
from urllib import request, parse, error
import json

class Task:
  
  def list():
    return Task.request()
  

  def delete(task_id):
    return Task.request(task_id=task_id, delete=True)

  
  def get(task_id):
    return Task.request(task_id=task_id)

  
  def create(**params):
    task_params = []
    for key, val in params["task_params"].items():
      if isinstance(val, list):
        for v in val:
          task_params.append("task_params[%s][]=%s" % (key, parse.quote(v)))
      else:
        task_params.append("task_params[%s]=%s" % (key, parse.quote(val)))

    
    del params["task_params"]
    task_params = "&".join(task_params)
    data = "%s&%s" % (parse.urlencode(params), task_params)
    resp = Task.request(data=data.encode())
    return json.loads(resp)

  
  def request(task_id=None, data=None, delete=None):
    if not buflow.api_key:
      raise Exception('API_KEY is required')

    url = "%s/tasks" % buflow.api_base
    if task_id:
      url += "/%s" % task_id

    headers = {"Authorization": buflow.api_key}
    req = request.Request(url, headers=headers, data=data)
    
    if delete:
      req.get_method = lambda : 'DELETE'
    
    try:
      resp = request.urlopen(req)
    except error.HTTPError as e:
      raise Exception(e.read().decode())
    content = resp.read()
    return content
