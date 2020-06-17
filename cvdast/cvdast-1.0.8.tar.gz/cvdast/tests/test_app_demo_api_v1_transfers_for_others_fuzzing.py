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


@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/others/names.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_others(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI5MmM5ZWJlMi0xYjBkLTRjOTUtYjNjYi1kNDg3NmJhODM2NTAiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.C8BZ3vZW3heVdMPXnynYBHD-NPw3o5M36TIgdkaXXxuoScZhLGnBhMzpH5iPSP-v10M3-4INuJB8iqNzzumhyQ', 'Connection': 'keep-alive', 'Content-Length': '92', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:12 GMT', 'Etag': 'W/"f21d0acb657593909d7dc1dad0f31408"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5cb20a88-dbbf-46c5-8a9f-87e0538f5895', 'X-Runtime': '0.188602', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)

@pytest.mark.parametrize("user_id1, beneficiary_id, description, amount, account_id", _prep_data_for_fuzzing("/Users/balak/PycharmProjects/tools-new/cv-DAST/cvdast/wfuzz/wordlist/others/common_pass.txt", ['user_id1', 'beneficiary_id', 'description', 'amount', 'account_id']))
def test_app_demo_api_v1_transfers_for_others(user_id1, beneficiary_id, description, amount, account_id):
    data = {}
    data["user_id1"] = user_id1
    data["beneficiary_id"] = beneficiary_id
    data["description"] = description
    data["amount"] = amount
    data["account_id"] = account_id
    
    headers = {'Accept': 'application/vnd.demoapp.com; version=1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZW1vYXBwLWFwaSIsImlhdCI6MTU5MjM1MzYzMiwidGkiOiI5MmM5ZWJlMi0xYjBkLTRjOTUtYjNjYi1kNDg3NmJhODM2NTAiLCJ1c2VyIjp7ImlkIjozLCJlbWFpbCI6ImpvaG5AZGVtb2FwcC5jb20ifX0.C8BZ3vZW3heVdMPXnynYBHD-NPw3o5M36TIgdkaXXxuoScZhLGnBhMzpH5iPSP-v10M3-4INuJB8iqNzzumhyQ', 'Connection': 'keep-alive', 'Content-Length': '92', 'Content-Type': 'application/json; charset=utf-8', 'Origin': 'http://34.238.148.157:31380', 'Referer': 'http://34.238.148.157:31380/profile', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36', 'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD', 'Access-Control-Allow-Origin': '*', 'Access-Control-Expose-Headers': '', 'Access-Control-Max-Age': '1728000', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Date': 'Wed, 17 Jun 2020 00:27:12 GMT', 'Etag': 'W/"f21d0acb657593909d7dc1dad0f31408"', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Server': 'nginx/1.17.10', 'Set-Cookie-params': None, 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Frame-Options': 'SAMEORIGIN', 'X-Permitted-Cross-Domain-Policies': 'none', 'X-Request-Id': '5cb20a88-dbbf-46c5-8a9f-87e0538f5895', 'X-Runtime': '0.188602', 'X-Xss-Protection': '1; mode=block'}
    headers["cv-fuzzed-event"] = "1"
    req = {
             "data": data,
             "headers": headers
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/api/v1/transfers",
                      header=req["headers"],
                      data=json.dumps(data))
    responses_recieved.append(resp)
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_negative_scenarios(req,resp)


def test_for_anomalies():
    pattern_observed = {"status_code": [], "resp_size": [], "request":[], "fuzz_type": "others"}
    for resp in responses_recieved:
        pattern_observed["status_code"].append(resp.status_code)
        pattern_observed["resp_size"].append(len(resp.content))
        #pattern_observed["request"].append(_create_curl_request(resp.request.url,resp.request.method,resp.request.headers,resp.request.body))
        pattern_observed["request"].append(curlify.to_curl(resp.request))
    assertions.assert_for_anomalies(pattern_observed)

