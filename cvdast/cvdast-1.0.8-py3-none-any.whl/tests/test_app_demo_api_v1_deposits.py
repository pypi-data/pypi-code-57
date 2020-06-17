import requests
import json
import pytest
import assertions

HOST_URL = "54.236.47.36:31236"


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
             "headers": {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_app_demo_api_v1_deposits(req,resp)





