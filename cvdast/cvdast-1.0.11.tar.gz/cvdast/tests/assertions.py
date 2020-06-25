
from dictor import dictor

ANOMALY_THRESHOLD = 0



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

