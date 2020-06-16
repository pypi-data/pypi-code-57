import requests
import json
import pytest
import assertions

HOST_URL = "3.85.202.4:31572"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_app_demo_api_v1_deposits(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    req = {
             "data": data,
             "headers": {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_app_demo_api_v1_deposits(req,resp)





