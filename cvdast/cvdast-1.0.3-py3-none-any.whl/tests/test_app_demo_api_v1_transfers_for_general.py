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


@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/extensions_common.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/medium.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/big.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/mutations_common.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/catala.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/megabeast.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/common.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/admin-panels.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/http_methods.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/euskera.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/test.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/spanish.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_general(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MDY5ODE0MywidGkiOiIxYzJhMTBkZC04MWI3LTQ0NDQtYjE0OC1iY2M1ZjhiYzg2YWMiLCJ1c2VyIjp7ImlkIjoyLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.7GJBDLUT6Wg-HDfvij2c1tJR3xJ7Tno7pWmlTyRMOzzd_SmbRpQ7NviOxlHzw-OF0hKLCtEIu1aMrJUy7wQcEg', 'Connection': 'keep-alive', 'Content-Length': '94', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Apache-HttpClient/4.5.10 (Java/1.8.0_252)', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Thu, 28 May 2020 21:20:32 GMT', 'Etag': 'W/"65cb88e14d36cbc0b308c53dad711210"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5b8e03bd-ffe8-4051-9e35-6f0102cb1e3c', 'X-Runtime': '0.199287', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = 1
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://3.85.202.4:31572/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)





