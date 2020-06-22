# py.tests  -v --junitxml="result.xml"

import pytest
import yaml

from willowlabs.company_information.client import CompanyInformationClient


# import mock
# from pytest_mock import mocker


def tmp_client():
    with open(r"config-dev.yaml") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)
    client = CompanyInformationClient(config["client_config_path"])
    return client


@pytest.fixture
def client():
    with open(r"config-dev.yaml") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)
    client = CompanyInformationClient(config["client_config_path"])
    return client


def test_get_basic_company_information_failure_1(client):
    organisation_number = 1
    company_basic_results = client.get_basic_company_information(organisation_number)
    assert company_basic_results.bad_request


def test_get_basic_company_information_beaufort_1(client):
    organisation_number = 923710809
    company_basic_results = client.get_basic_company_information(organisation_number)
    print(company_basic_results)
    assert (
        company_basic_results.basic_company_information.company_name
        == "BEAUFORT SOLUTIONS AS"
    )
    print(company_basic_results.basic_company_information.company_name)


def test_get_company_ownership_beaufort_failure_1(client):
    organisation_number = 1
    record_year = 2018
    company_ownership_results = client.get_company_ownership(
        organisation_number, record_year
    )
    assert company_ownership_results.bad_request


def test_get_company_ownership_beaufort_success(client):
    record_year = 2018
    organisation_number = 923710809
    company_ownership_results = client.get_company_ownership(
        organisation_number, record_year
    )
    assert not company_ownership_results.bad_request


def test_get_company_ownership_beaufort_struture_ok_1(client):
    record_year = 2018
    organisation_number = 913174054
    cutoff = 1
    depth = 2
    company_ownership_results = client.get_company_ownership(
        organisation_number, record_year, depth, cutoff
    )
    print(company_ownership_results)
    print(type(company_ownership_results))
    print(len(company_ownership_results.company_shares[0].individual_owners))
    assert len(company_ownership_results.company_shares[0].individual_owners) == 2


def test_get_company_power_of_attorney_ok_1(client):
    # record_year = 2018
    organisation_number = 913174054
    company_poa_results = client.get_company_power_of_attorney(organisation_number)
    print(company_poa_results)
    assert (
        company_poa_results.authorized_signatures[0].signatory_text_en
        == "Board chairman alone"
    )


test_get_company_power_of_attorney_ok_1(tmp_client())
