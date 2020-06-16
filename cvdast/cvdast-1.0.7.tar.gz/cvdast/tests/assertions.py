
from dictor import dictor



def assert_for_app_demo_oauth_token(req, resp):
    assert resp.status_code == 200
    assert req['email'] == resp['user.user.email']
    assert req['email'] == resp['user.user.user_detail.email']


def assert_for_app_demo_api_v1_transfers(req, resp):
    assert resp.status_code == 200
    assert req['beneficiary_id'] == resp['transfer.beneficiary_id']
    assert req['description'] == resp['transfer.description']
    assert req['amount'] == resp['transfer.amount']
    assert req['account_id'] == resp['transfer.account_id']


def assert_for_app_demo_api_v1_deposits(req, resp):
    assert resp.status_code == 200
    assert req['amount'] == resp['deposit.amount']


def assert_for_negative_scenarios(req, resp):
    if resp.status_code != 200:
        print("----------------------")
        print("Request: "+str(req))
        print("Response: "+str(resp))
        print("----------------------")
    assert resp.status_code != 200