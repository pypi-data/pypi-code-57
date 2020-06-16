import requests
import json
import pytest
import assertions

HOST_URL = "3.85.202.4:31572"


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


@pytest.mark.parametrize("description, amount, user_id, account_id1", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/extensions_common.txt", ['description', 'amount', 'user_id', 'account_id1']))
def test_app_demo_api_v1_deposits_for_general(description, amount, user_id, account_id1):
    data = {}
    data["description"] = description
    data["amount"] = amount
    data["user_id"] = user_id
    data["account_id1"] = account_id1
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
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
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '64', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:19:54 GMT', 'Etag': 'W/"fc20d478ca78ae25738f3cafe4c1c504"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '4d83afb1-b784-487d-8038-00e59dbfd87d', 'X-Runtime': '0.125189', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/deposits",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)





