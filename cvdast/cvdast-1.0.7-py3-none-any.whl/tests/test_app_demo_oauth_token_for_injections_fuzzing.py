import requests
import json
import pytest
import assertions

HOST_URL = "54.236.47.36:31236"


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


@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/SQL.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/Traversal.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/XML.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/XSS.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/All_attack.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/injections/bad_chars.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_injections(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Content-Length': '249', 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Date': 'Tue, 16 Jun 2020 16:06:12 GMT', 'Etag': 'W/"cfae575c0a48223bba248b6d6983a635"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.379238'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)





