import requests
import json
import pytest
import assertions

HOST_URL = "localhost:50000"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_dynconfigContainerGet(feglobalconfigstreamprocessor):
    data = {}
    data["feglobalconfigstreamprocessor"] = feglobalconfigstreamprocessor
    
    req = {
             "data": data,
             "headers": {'Accept': '*/*', 'Content-Length': '285', 'Content-Type': 'application/json', 'User-Agent': 'curl/7.29.0', 'Date': 'Thu, 25 Jun 2020 15:46:10 GMT', 'Set-Cookie-params': None}
          }
    resp = _trigger_requests("POST", "http://localhost:50000/dynconfigContainerGet",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_dynconfigContainerGet(req,resp)





