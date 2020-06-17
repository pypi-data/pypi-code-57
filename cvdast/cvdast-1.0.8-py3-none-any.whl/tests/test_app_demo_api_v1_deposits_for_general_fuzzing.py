import requests
import json
import pytest
import assertions
import curlify

HOST_URL = "54.236.47.36:31236"

responses_recieved = []

def _prep_data_for_fuzzing(file, params_list):
    fuzz_values = []
    with open(file, encoding="iso-8859-15") as fobj:
        values = [str(_).replace("\n","") for _ in fobj.readlines()]
    no_of_params = len(params_list)
    for _ in values:
        fuzz_values.append([_]*no_of_params)
    print("Fuzz values for "+str(file)+": "+str(fuzz_values))
    return fuzz_values

def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)

def _create_curl_request(url,method,headers,payloads):
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    data = ""
    if payloads:
        payloads = json.loads(payloads)
        payload_list = ['"{0}":"{1}"'.format(k,v) for k,v in payloads.items()]
        data = " -d '{" + ", ".join(payload_list) + "}'"
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    return command.format(method=method, headers=header, data=data, uri=url)


@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/extensions_common.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/medium.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/big.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/mutations_common.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/catala.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/megabeast.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/common.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/admin-panels.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/http_methods.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/euskera.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/test.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/spanish.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI2MzE0MjRkYi05MGM5LTRiNTYtYWNjYy0xY2ExM2Y1NjcxYzQiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.Tvz6Ifof3xD6XrWwizSoFmwNwt-nGLsuvG_qHrky-LLm0YSZyB1qo_E8d5hv7PaMrkpzYCHuA1DdpU6FGR6oqg', 'Connection': 'keep-alive', 'Content-Length': '71', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:13 GMT', 'Etag': 'W/"cdaf873a92e67e0dc348cec53c961d47"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '0dab70e0-1397-4f22-b390-b92bab345258', 'X-Runtime': '0.053542', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)


def test_for_anomalies():
    pattern_observed = {"status_code": [], "resp_size": [], "request":[], "fuzz_type": "general"}
    for resp in responses_recieved:
        pattern_observed["status_code"].append(resp.status_code)
        pattern_observed["resp_size"].append(len(resp.content))
        #pattern_observed["request"].append(_create_curl_request(resp.request.url,resp.request.method,resp.request.headers,resp.request.body))
        pattern_observed["request"].append(curlify.to_curl(resp.request))
    assertions.assert_for_anomalies(pattern_observed)

