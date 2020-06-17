from datetime import datetime

import pandas as pd
import pytest
import responses

from datarobot import Deployment
from tests.utils import request_body_to_json


class TestSubmitActuals(object):
    @pytest.fixture()
    def submit_actual_response(self, unittest_endpoint, deployment_data):
        url = '{}/{}/{}/actuals/fromJSON/'.format(
            unittest_endpoint, 'deployments', deployment_data['id'])
        status_url = '{}/STATUS_ID/'.format(unittest_endpoint)
        accuracy_url = '{}/{}/{}/accuracy/'.format(
            unittest_endpoint, 'deployments', deployment_data['id'])
        responses.add(
            responses.POST,
            url,
            status=202,
            headers={'Location': status_url})
        responses.add(
            responses.GET,
            status_url,
            status=303,
            headers={'Location': accuracy_url})

    @responses.activate
    @pytest.mark.usefixtures('deployment_get_response')
    @pytest.mark.parametrize('actuals_data', [None, [], 'abc', pd.DataFrame()])
    def test_bad_data(self, deployment_data, actuals_data):
        """When submitting actuals with bad data, `ValueError` is raised."""
        with pytest.raises(ValueError):
            deployment = Deployment.get(deployment_data['id'])
            deployment.submit_actuals(actuals_data)

    @responses.activate
    @pytest.mark.usefixtures('deployment_get_response', 'submit_actual_response')
    @pytest.mark.parametrize('actuals_data, expected_payload', [
        (
                [{'association_id': 'abc', 'actual_value': 'True'}],
                {'data': [{'associationId': 'abc', 'actualValue': 'True'}]}
        ),
        (
                [{'association_id': 'abc', 'actual_value': 'True'}],
                {'data': [{'associationId': 'abc', 'actualValue': 'True'}]}
        ),
        (
                [{'association_id': 'abc', 'actual_value': 'True', 'was_acted_on': True}],
                {'data': [{'associationId': 'abc', 'actualValue': 'True', 'wasActedOn': True}]}
        ),
        (
                [{
                    'association_id': 'abc', 'actual_value': 'True',
                    'timestamp': datetime(2019, 8, 1, 12, 30)
                }],
                {'data': [
                    {'associationId': 'abc', 'actualValue': 'True',
                     'timestamp': '2019-08-01T12:30:00+00:00'}
                ]})]
        )
    def test_submit(self, deployment_data, actuals_data, expected_payload):
        deployment = Deployment.get(deployment_data['id'])
        deployment.submit_actuals(actuals_data)
        actual_payload = request_body_to_json(responses.calls[1].request)
        assert actual_payload == expected_payload

    @responses.activate
    @pytest.mark.usefixtures('deployment_get_response', 'submit_actual_response')
    def test_submit_with_dataframe(self, deployment_data):
        actuals_data = pd.DataFrame([
            ['a', 1, None, None],
            ['b', 2, True, None],
            ['c', 3, None, datetime(2019, 8, 1, 12, 30)],
            ['d', 4, False, datetime(2019, 8, 1, 12, 30)],
        ], columns=['association_id', 'actual_value', 'was_acted_on', 'timestamp'])
        expected_payload = {
            'data': [
                {'associationId': 'a', 'actualValue': 1},
                {'associationId': 'b', 'actualValue': 2, 'wasActedOn': True},
                {'associationId': 'c', 'actualValue': 3, 'timestamp': '2019-08-01T12:30:00+00:00'},
                {'associationId': 'd', 'actualValue': 4, 'wasActedOn': False,
                 'timestamp': '2019-08-01T12:30:00+00:00'}
            ]
        }

        deployment = Deployment.get(deployment_data['id'])
        deployment.submit_actuals(actuals_data)
        actual_payload = request_body_to_json(responses.calls[1].request)
        assert actual_payload == expected_payload
