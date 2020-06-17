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


@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/extensions_common.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/medium.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/big.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/mutations_common.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/catala.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/megabeast.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/common.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/admin-panels.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/http_methods.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/euskera.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/test.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("password, client_id, grant_type, email, client_secret, dummy", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/general/spanish.txt", ['password', 'client_id', 'grant_type', 'email', 'client_secret', 'dummy']))
def test_app_demo_oauth_token_for_general(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
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

