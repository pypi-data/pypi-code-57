import json

import requests

url = "http://localhost:8080/queue/batches/"
task_types = ["say-hello"] * 10
json_datas = [json.dumps({"hello": "world"})] * 10
task_ids = [f"hello-{i}" for i in range(10)]


payload = dict(
    batch_id="batch-test",
    task_types=task_types,
    json_datas=json_datas,
    task_ids=task_ids,
)
r = requests.post(url, data=payload)
