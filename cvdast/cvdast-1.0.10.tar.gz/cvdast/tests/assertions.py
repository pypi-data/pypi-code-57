
from dictor import dictor

ANOMALY_THRESHOLD = 1.07142



def assert_for_dynconfigContainerGet(req, resp):
    assert resp.status_code == 200


def assert_for_dynconfigEndpointStore(req, resp):
    assert resp.status_code == 200
    assert req['data.server.type'] == resp['type']
    assert req['data.type'] == resp['type']


def assert_for_negative_scenarios(req, resp):
    if resp.status_code != 200:
        print("----------------------")
        print("Request: "+str(req))
        print("Response: "+str(resp))
        print("----------------------")
    assert resp.status_code != 200

def assert_for_anomalies(pattern_observed):
    status_codes = list(set(pattern_observed["status_code"]))
    if len(status_codes) == 1:
        print("No anomalies observed in status codes")
        assert 1
    else:
        counter = 0
        num = status_codes[0]

        for i in status_codes:
            curr_frequency = status_codes.count(i)
            if curr_frequency > counter:
                counter = curr_frequency
                num = i

        indexes = [i for i, x in enumerate(pattern_observed["status_code"]) if x == num]
        for _ in indexes:
            print("\n ------------ To regenerate the request for "+str(pattern_observed["fuzz_type"])+":\n\n"+
                                                                            str(pattern_observed["request"][_]))
            print("--------" * 20)
        print("anomalies observed in status codes")
        assert 0

    min_resp_size = min(pattern_observed["resp_size"])
    resp_codes = [(int(_)/int(min_resp_size)) for _ in pattern_observed["resp_size"]]
    suspicious_responses = []
    for _ in range(len(resp_codes)):
        if resp_codes[_] > ANOMALY_THRESHOLD:
            suspicious_responses.append(pattern_observed["request"][_])
            print("\n ------------ To regenerate the request for "+str(pattern_observed["fuzz_type"])+":\n\n"+
                                                                            str(suspicious_responses[-1]))
            print("--------"*20)
    if not suspicious_responses:
        print("No anomalies observed in response content length")
        assert 1
    else:
        print("anomalies observed in response content length")
        assert 0