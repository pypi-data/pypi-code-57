
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
@fixture_plus(params=get_params_from_file("type"))
def type(request):
    return request.param
    # return get_params_from_file("type")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("name"))
def name(request):
    return request.param
    # return get_params_from_file("name")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("server"))
def server(request):
    return request.param
    # return get_params_from_file("server")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("ttl"))
def ttl(request):
    return request.param
    # return get_params_from_file("ttl")


# @pytest.fixture(scope="session", autouse=True)
@fixture_plus(params=get_params_from_file("environment"))
def environment(request):
    return request.param
    # return get_params_from_file("environment")


