
import json
import pytest
import random
import os
from pytest_cases import fixture_plus

def get_params_from_file(param):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"params_captured.json")) as fobj:
        params = json.load(fobj)
    for api, params_info in params.items():
        if param in params_info:
            values = params[api][param]
            if None in values:
                values.remove(None)
            #return random.choice(values)
            return values


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("client_secret"))
def client_secret(request):
    return request.param
    # return get_params_from_file("client_secret")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("email"))
def email(request):
    return request.param
    # return get_params_from_file("email")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("password"))
def password(request):
    return request.param
    # return get_params_from_file("password")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("grant_type"))
def grant_type(request):
    return request.param
    # return get_params_from_file("grant_type")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("client_id"))
def client_id(request):
    return request.param
    # return get_params_from_file("client_id")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("dummy"))
def dummy(request):
    return request.param
    # return get_params_from_file("dummy")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("beneficiary_id"))
def beneficiary_id(request):
    return request.param
    # return get_params_from_file("beneficiary_id")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("amount"))
def amount(request):
    return request.param
    # return get_params_from_file("amount")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("description"))
def description(request):
    return request.param
    # return get_params_from_file("description")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("user_id"))
def user_id(request):
    return request.param
    # return get_params_from_file("user_id")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("account_id"))
def account_id(request):
    return request.param
    # return get_params_from_file("account_id")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("user_id1"))
def user_id1(request):
    return request.param
    # return get_params_from_file("user_id1")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("account_id1"))
def account_id1(request):
    return request.param
    # return get_params_from_file("account_id1")


