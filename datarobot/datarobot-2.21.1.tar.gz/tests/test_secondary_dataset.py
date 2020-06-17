import pytest
import json
import responses

from datarobot import errors
from tests.utils import request_body_to_json
from datarobot.models.secondary_dataset import (
    DatasetConfiguration,
    SecondaryDataset,
    SecondaryDatasetConfigurations,
)


@pytest.fixture
def ids():
    return {
        'pid': '5a530498d5c1f302d6d17699',
        'graph_id': '5a530498d5c1f302d6d17111',
        'identifier_1': 'test_dataset_1',
        'catalog_version_id_1': '5a530498d5c1f302d6d17121',
        'catalog_id_1': '5a530498d5c1f302d6d17115',
        'identifier_2': 'test_dataset_2',
        'catalog_version_id_2': '6a530498d5c1f302d6d17121',
        'catalog_id_2': '6a530498d5c1f302d6d17115',
    }


@pytest.fixture
def dataset_configurations(ids):
    secondary_dataset_1 = SecondaryDataset(
        identifier=ids['identifier_1'],
        catalog_version_id=ids['catalog_version_id_1'],
        catalog_id=ids['catalog_id_1'],
        snapshot_policy='specified',
    )
    secondary_dataset_2 = SecondaryDataset(
        identifier=ids['identifier_2'],
        catalog_version_id=ids['catalog_version_id_2'],
        catalog_id=ids['catalog_id_2'],
        snapshot_policy='specified',
    )
    return [
        DatasetConfiguration(
            feature_engineering_graph_id=ids['graph_id'],
            secondary_datasets=[secondary_dataset_1, secondary_dataset_2],
        )
    ]


@pytest.fixture
def secondary_dataset_configurations_response(ids):
    return {
        'projectId': ids['pid'],
        'config': [
            {
                'secondaryDatasets': [
                    {
                        'snapshotPolicy': 'specified',
                        'identifier': ids['identifier_1'],
                        'catalogVersionId': ids['catalog_version_id_1'],
                        'catalogId': ids['catalog_id_1'],
                    },
                    {
                        'snapshotPolicy': 'specified',
                        'identifier': ids['identifier_2'],
                        'catalogVersionId': ids['catalog_version_id_2'],
                        'catalogId': ids['catalog_id_2'],
                    },
                ],
                'featureEngineeringGraphId': ids['graph_id'],
            }
        ],
        'id': '5df109112ca582033ff44084',
    }


@responses.activate
def test_create_secondary_dataset_configurations(
    ids, dataset_configurations, secondary_dataset_configurations_response
):
    url = 'https://host_name.com/projects/{}/secondaryDatasetsConfigurations/'.format(
        ids['pid']
    )
    responses.add(
        responses.POST,
        url,
        status=201,
        body=json.dumps(secondary_dataset_configurations_response),
    )

    result = SecondaryDatasetConfigurations.create(ids['pid'], dataset_configurations)

    assert responses.calls[0].request.method == 'POST'

    # verify request payload
    payload = request_body_to_json(responses.calls[0].request)
    conf = payload['conf'][0]
    assert conf['featureEngineeringGraphId'] == ids['graph_id']
    dataset_confs = conf['secondaryDatasets']
    expected_conf_sets = [
        d.to_dict() for d in dataset_configurations[0].secondary_datasets
    ]
    assert len(dataset_confs) == len(expected_conf_sets)
    identifier = dataset_confs[0]['identifier']
    expected_dataset = [d for d in expected_conf_sets if d['identifier'] == identifier][
        0
    ]
    assert dataset_confs[0] == expected_dataset

    # verify response
    assert isinstance(result, SecondaryDatasetConfigurations)
    assert result.project_id == ids['pid']
    dataset_conf = result.config[0]
    assert isinstance(dataset_conf, DatasetConfiguration)
    assert dataset_conf.feature_engineering_graph_id == ids['graph_id']
    dataset = dataset_conf.secondary_datasets[0]
    assert isinstance(dataset, SecondaryDataset)
    identifier = dataset.identifier
    expected_dataset = [d for d in expected_conf_sets if d['identifier'] == identifier][
        0
    ]
    assert dataset.catalog_id == expected_dataset['catalogId']
    assert dataset.catalog_version_id == expected_dataset['catalogVersionId']
    assert dataset.snapshot_policy == expected_dataset['snapshotPolicy']


@responses.activate
def test_failure_in_create_secondary_dataset_configurations__status_error_code(
    ids, dataset_configurations
):
    url = 'https://host_name.com/projects/{}/secondaryDatasetsConfigurations/'.format(
        ids['pid']
    )
    responses.add(responses.POST, url, status=404, body='')

    with pytest.raises(errors.ClientError):
        SecondaryDatasetConfigurations.create(ids['pid'], dataset_configurations)


@responses.activate
def test_secondary_dataset_configurations_retrieve(
    ids, secondary_dataset_configurations_response,
):
    config_id = secondary_dataset_configurations_response['id']
    pid = secondary_dataset_configurations_response['projectId']
    dataset_configurations = secondary_dataset_configurations_response['config']
    url = 'https://host_name.com/projects/{}/secondaryDatasetsConfigurations/{}/'.format(
        pid, config_id
    )
    responses.add(responses.GET, url, json=secondary_dataset_configurations_response)

    secondary_dataset_config = SecondaryDatasetConfigurations(
        id=config_id, project_id=pid
    ).get()

    assert responses.calls[0].request.method == 'GET'
    assert secondary_dataset_config.id == config_id
    assert secondary_dataset_config.project_id == pid
    assert len(secondary_dataset_config.config) == 1

    dataset_conf = secondary_dataset_config.config[0]
    assert isinstance(dataset_conf, DatasetConfiguration)
    assert dataset_conf.feature_engineering_graph_id == ids['graph_id']
    dataset = dataset_conf.secondary_datasets[0]
    assert isinstance(dataset, SecondaryDataset)
    identifier = dataset.identifier
    expected_config = dataset_configurations[0]['secondaryDatasets']
    expected_dataset = [d for d in expected_config if d['identifier'] == identifier][0]
    assert dataset.catalog_id == expected_dataset['catalogId']
    assert dataset.catalog_version_id == expected_dataset['catalogVersionId']
    assert dataset.snapshot_policy == expected_dataset['snapshotPolicy']


@responses.activate
def test_secondary_dataset_configurations_deletion(
    secondary_dataset_configurations_response,
):
    config_id = secondary_dataset_configurations_response['id']
    pid = secondary_dataset_configurations_response['projectId']
    url = 'https://host_name.com/projects/{}/secondaryDatasetsConfigurations/{}/'.format(
        pid, config_id
    )
    responses.add(responses.GET, url, json=secondary_dataset_configurations_response)
    responses.add(responses.DELETE, url)
    secondary_dataset_config = SecondaryDatasetConfigurations(
        id=config_id, project_id=pid
    ).get()
    secondary_dataset_config.delete()
    assert responses.calls[1].request.method == responses.DELETE
    assert responses.calls[1].request.url == url
