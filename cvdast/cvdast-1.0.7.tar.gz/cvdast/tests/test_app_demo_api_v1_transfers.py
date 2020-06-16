import requests
import json
import pytest
import assertions

HOST_URL = "54.236.47.36:31236"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_app_demo_api_v1_transfers(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    req = {
             "data": data,
             "headers": {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjMyMzU3MiwidGkiOiJmZmRjZGZiNC03OWI3LTQwMjctYWFmZi00MmZiOTNjMjRkMTkiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.U3_uaoWh2pXKIAOwdG1FnnqM1TNDi8IqVn_fEqt1zUsD-P3m8hKsXf_6Q6fIstv7fPmJp5o_C56WXQrd2LImCw', 'Connection': 'keep-alive', 'Content-Length': '92', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Tue, 16 Jun 2020 16:06:13 GMT', 'Etag': 'W/"9c2a8563ebeace750500aaa4da09cf5c"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '1f052a31-e619-400b-8b60-455ce2db3b01', 'X-Runtime': '0.355976', 'X-Xss-Protection': '1; mode=block'}
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_app_demo_api_v1_transfers(req,resp)





