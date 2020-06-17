import json
from six.moves.urllib.parse import urljoin

from datarobot import enums

import pytest
import responses


@pytest.fixture
def model_url(project_url, model_id):
    return urljoin(project_url, "models/{}/".format(model_id))


@pytest.fixture
def feature_impact_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/featureImpact/'.format(project_id, model_id)


@pytest.fixture
def multiclass_feature_impact_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/multiclassFeatureImpact/'.format(
        project_id, model_id)


@pytest.fixture
def feature_impact_job_creation_response(feature_impact_url, job_url):
    responses.add(
        responses.POST,
        feature_impact_url,
        body='',
        status=202,
        adding_headers={'Location': job_url})


@pytest.fixture
def multiclass_feature_impact_server_data():
    return {
        'ranRedundancyDetection': False,
        'classFeatureImpacts': [
            {'featureImpacts': [
                {'featureName': 'Petal Width',
                 'redundantWith': None,
                 'impactUnnormalized': 0.157,
                 'impactNormalized': 0.701},
                {'featureName': 'Petal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.121,
                 'impactNormalized': 0.539},
                {'featureName': 'Sepal Width',
                 'redundantWith': None,
                 'impactUnnormalized': 0.225,
                 'impactNormalized': 1.0},
                {'featureName': 'Sepal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.057,
                 'impactNormalized': 0.257}],
                'class': 'setosa'},
            {'featureImpacts': [
                {'featureName': 'Petal Width',
                 'redundantWith': None,
                 'impactUnnormalized': 0.302,
                 'impactNormalized': 1.0},
                {'featureName': 'Petal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.229,
                 'impactNormalized': 0.758},
                {'featureName': 'Sepal Width',
                 'redundantWith': None,
                 'impactUnnormalized': 0.221,
                 'impactNormalized': 0.730},
                {'featureName': 'Sepal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.073,
                 'impactNormalized': 0.241}],
                'class': 'versicolor'},
            {'featureImpacts': [
                {'featureName': 'Petal Width',
                 'redundantWith': None,
                 'impactUnnormalized': 0.273,
                 'impactNormalized': 1.0},
                {'featureName': 'Petal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.174,
                 'impactNormalized': 0.640},
                {'featureName': 'Sepal Width',
                 'redundantWith': None,
                 'impactUnnormalized': -0.001,
                 'impactNormalized': -0.006},
                {'featureName': 'Sepal Length',
                 'redundantWith': None,
                 'impactUnnormalized': 0.018,
                 'impactNormalized': 0.067}],
                'class': 'virginica'}
        ]
    }


@pytest.fixture
def feature_impact_response(feature_impact_server_data, feature_impact_url):
    body = json.dumps(feature_impact_server_data)
    responses.add(
        responses.GET,
        feature_impact_url,
        status=200,
        content_type='application/json',
        body=body
    )


@pytest.fixture
def multiclass_feature_impact_response(multiclass_feature_impact_server_data,
                                       multiclass_feature_impact_url):
    body = json.dumps(multiclass_feature_impact_server_data)
    responses.add(
        responses.GET,
        multiclass_feature_impact_url,
        status=200,
        content_type='application/json',
        body=body
    )


@pytest.fixture
def feature_impact_job_running_server_data(base_job_running_server_data):
    return dict(base_job_running_server_data, jobType='featureImpact')


@pytest.fixture
def feature_impact_job_finished_server_data(base_job_completed_server_data):
    return dict(base_job_completed_server_data, jobType='featureImpact')


@pytest.fixture
def approximate_job_running_server_data(base_job_running_server_data):
    return dict(base_job_running_server_data, jobType=enums.JOB_TYPE.PRIME_RULESETS)


@pytest.fixture
def approximate_job_finished_server_data(base_job_completed_server_data):
    return dict(base_job_completed_server_data, jobType=enums.JOB_TYPE.PRIME_RULESETS)


@pytest.fixture
def prime_validation_job_running_server_data(base_job_running_server_data):
    return dict(base_job_running_server_data, jobType=enums.JOB_TYPE.PRIME_VALIDATION)


@pytest.fixture
def prime_validation_job_finished_server_data(base_job_completed_server_data):
    return dict(base_job_completed_server_data, jobType=enums.JOB_TYPE.PRIME_VALIDATION)


@pytest.fixture
def feature_impact_completed_response(feature_impact_job_finished_server_data,
                                      job_url, feature_impact_url):
    """
    Loads a response that the given job is a featureImpact job, and is in completed
    """
    responses.add(responses.GET,
                  job_url,
                  body=json.dumps(feature_impact_job_finished_server_data),
                  status=303,
                  adding_headers={'Location': feature_impact_url},
                  content_type='application/json')


@pytest.fixture
def feature_impact_previously_ran_response(project_url, model_id, job_id):
    """
    Loads a response that the given model has already ran its feature impact
     """
    body = {
        'message': 'Feature Impact is in progress for this model.',
        'errorName': 'JobAlreadyAdded',
        'jobId': job_id
        }
    responses.add(responses.POST,
                  '{}models/{}/featureImpact/'.format(project_url, model_id),
                  body=json.dumps(body),
                  status=422,
                  content_type='application/json')


@pytest.fixture
def feature_impact_running_response(feature_impact_job_running_server_data, job_url):
    """
    Loads a response that the given job is a featureImpact job, and is running
    """
    responses.add(responses.GET,
                  job_url,
                  body=json.dumps(feature_impact_job_running_server_data),
                  status=200,
                  content_type='application/json')


@pytest.fixture
def approximate_job_creation_response(project_url, model_id, job_url):
    responses.add(responses.POST,
                  '{}models/{}/primeRulesets/'.format(project_url, model_id),
                  body='',
                  status=202,
                  adding_headers={'Location': job_url})


@pytest.fixture
def approximate_completed_response(approximate_job_finished_server_data, job_url,
                                   project_url, model_id,
                                   ruleset_without_model_server_data,
                                   ruleset_with_model_server_data):
    rulesets_url = '{}models/{}/primeRulesets/'.format(project_url, model_id)
    responses.add(responses.GET, job_url, body=json.dumps(approximate_job_finished_server_data),
                  status=303,
                  adding_headers={'Location': rulesets_url},
                  content_type='application/json')
    responses.add(responses.GET, rulesets_url,
                  body=json.dumps([ruleset_with_model_server_data,
                                   ruleset_without_model_server_data]),
                  content_type='application/json')


@pytest.fixture
def prime_validation_job_creation_response(project_url, job_url):
    responses.add(responses.POST, '{}primeFiles/'.format(project_url), body='', status=202,
                  adding_headers={'Location': job_url})


@pytest.fixture
def prime_validation_job_completed_response(prime_validation_job_finished_server_data,
                                            job_url, project_url, prime_file_server_data):
    file_url = '{}primeFiles/{}/'.format(project_url, prime_file_server_data['id'])
    responses.add(responses.GET, job_url,
                  body=json.dumps(prime_validation_job_finished_server_data),
                  status=303, adding_headers={'Location': file_url},
                  content_type='application/json')
    responses.add(responses.GET, file_url, body=json.dumps(prime_file_server_data),
                  content_type='application/json')


@pytest.fixture
def mocked_execution_environment_versions():
    return {
        "count": 3,
        "totalCount": 3,
        "next": None,
        "previous": None,
        "data": [
            {
                "id": "5cf4d3f5f930e26daac18a1a",
                "environmentId": "5cf4d3f5f930e26daac18a1xx",
                "label": "Version 1",
                "description": "",
                "buildStatus": "success",
                "created": "2019-09-28T15:19:26.587583Z",
            },
            {
                "id": "5cf4d3f5f930e26daac18a2a",
                "environmentId": "5cf4d3f5f930e26daac18a1xx",
                "label": "Version 1",
                "description": "",
                "buildStatus": "processing",
                "created": "2019-09-28T15:19:26.587583Z",
            },
            {
                "id": "5cf4d3f5f930e26daac18a3a",
                "environmentId": "5cf4d3f5f930e26daac18a1xx",
                "label": "Version 1",
                "description": "some description",
                "buildStatus": "failed",
                "created": "2019-09-28T15:19:26.587583Z",
            },
        ],
    }


@pytest.fixture
def mocked_execution_environment_version(mocked_execution_environment_versions):
    return mocked_execution_environment_versions["data"][0]


@pytest.fixture
def mocked_execution_environments(mocked_execution_environment_version):
    return {
        "count": 2,
        "totalCount": 2,
        "next": None,
        "previous": None,
        "data": [
            {
                "id": "5cf4d3f5f930e26daac18a1a",
                "name": "env1",
                "description": "some description",
                "programmingLanguage": "python",
                "isPublic": True,
                "created": "2019-09-28T15:19:26.587583Z",
                "latestVersion": mocked_execution_environment_version,
            },
            {
                "id": "5cf4d3f5f930e26daac18a1a",
                "name": "env2",
                "description": "",
                "programmingLanguage": "other",
                "isPublic": False,
                "created": "2019-09-28T15:19:26.587583Z",
                "latestVersion": None,
            },
        ],
    }


@pytest.fixture
def mocked_execution_environment(mocked_execution_environments):
    return mocked_execution_environments["data"][0]


@pytest.fixture
def mocked_versions():
    return {
        "count": 2,
        "totalCount": 2,
        "next": None,
        "previous": None,
        "data": [
            {
                "id": "5cf4d3f5f930e26daac18a1a",
                "customModelId": "5cf4d3f5f930e26daac18a1xx",
                "label": "Version 1",
                "description": "",
                "versionMinor": 0,
                "versionMajor": 1,
                "isFrozen": False,
                "items": [
                    {
                        "id": "5cf4d3f5f930e26daac18xxx",
                        "fileName": "name",
                        "filePath": "path",
                        "fileSource": "source",
                        "created": "2019-09-28T15:19:26.587583Z",
                    }
                ],
                "created": "2019-09-28T15:19:26.587583Z",
            },
            {
                "id": "5cf4d3f5f930e26daac18aBB",
                "customModelId": "5cf4d3f5f930e26daac18a1BB",
                "label": "Version 2",
                "description": "ss",
                "versionMinor": 2,
                "versionMajor": 3,
                "isFrozen": True,
                "items": [],
                "created": "2019-09-28T15:19:26.587583Z",
            },
        ],
    }


@pytest.fixture
def mocked_custom_model_version(mocked_versions):
    return mocked_versions['data'][0]


@pytest.fixture
def mocked_custom_model_version2(mocked_versions):
    return mocked_versions['data'][1]


@pytest.fixture
def shap_impact_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/shapImpact/'.format(project_id, model_id)


@pytest.fixture
def shap_impact_job_creation_response(shap_impact_url, job_url):
    responses.add(
        responses.POST,
        shap_impact_url,
        body='',
        status=202,
        adding_headers={'Location': job_url}
    )


@pytest.fixture
def shap_impact_response(shap_impact_server_data, shap_impact_url):
    body = json.dumps(shap_impact_server_data)
    responses.add(
        responses.GET,
        shap_impact_url,
        status=200,
        content_type='application/json',
        body=body
    )


@pytest.fixture
def shap_impact_job_running_server_data(base_job_running_server_data):
    return dict(base_job_running_server_data, jobType='shapImpact')


@pytest.fixture
def shap_impact_job_finished_server_data(base_job_completed_server_data):
    return dict(base_job_completed_server_data, jobType='shapImpact')


@pytest.fixture
def shap_impact_running_response(shap_impact_job_running_server_data, job_url):
    responses.add(
        responses.GET,
        job_url,
        body=json.dumps(shap_impact_job_running_server_data),
        status=200,
        content_type='application/json'
    )


@pytest.fixture
def shap_impact_completed_response(shap_impact_job_finished_server_data, job_url, shap_impact_url):
    responses.add(
        responses.GET,
        job_url,
        body=json.dumps(shap_impact_job_finished_server_data),
        status=303,
        adding_headers={'Location': shap_impact_url},
        content_type='application/json'
    )


@pytest.fixture
def shap_impact_previously_ran_response(project_url, model_id, job_id, job_url):
    body = {
        'message': 'SHAP impact already exists.',
        'errorName': 'JobAlreadyAdded',
        'jobId': job_id
        }
    responses.add(
        responses.POST,
        '{}models/{}/shapImpact/'.format(project_url, model_id),
        body=json.dumps(body),
        status=202,
        content_type='application/json',
        adding_headers={'Location': job_url}
    )
