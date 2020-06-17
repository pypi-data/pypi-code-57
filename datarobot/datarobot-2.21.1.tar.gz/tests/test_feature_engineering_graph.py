import datetime

import pytest
import responses
from tests.utils import request_body_to_json

from datarobot import FeatureEngineeringGraph, SharingAccess


@pytest.fixture
def create_feature_engineering_graph_items():
    return [
        {
            'identifier': 'user',
            'catalogVersionId': '5c88a37770fc42a2fcc62759',
            'snapshotPolicy': 'latest'
        },
        {
            'identifier': 'transaction',
            'catalogVersionId': '5c88a37770fc42a2fcc62760',
            'primaryTemporalKey': 'date',
            'snapshotPolicy': 'latest'
        },
    ]


@pytest.fixture
def create_feature_engineering_graph_relationships():
    return [
        {
            'table2Identifier': 'user',
            'table1Keys': ['user_id', 'dept_id'],
            'table2Keys': ['user_id', 'dept_id'],
        },
        {
            'table1Identifier': 'user',
            'table2Identifier': 'transaction',
            'table1Keys': ['user_id'],
            'table2Keys': ['user_id'],
        },
    ]


@pytest.fixture
def feature_engineering_graph_response(create_feature_engineering_graph_items,
                                       create_feature_engineering_graph_relationships):
    """ Payload to create a Feature Source via API
    """
    return {
        'id': '5a530498d5c1f302d6d176c8',
        'name': 'Customer Features',
        'description': 'Credit card customer features (using activity in last 2 months)',
        'tableDefinitions': create_feature_engineering_graph_items,
        'relationships': create_feature_engineering_graph_relationships,
        'featureDerivationWindowStart': -14,
        'featureDerivationWindowEnd': -1,
        'timeUnit': 'DAY',
        'created': '2016-07-26T02:29:58.546312Z',
        'lastModified': '2016-07-26T02:29:58.546312Z',
        'creatorFullName': 'abc@datarobot.com',
        'modifierFullName': 'abc@datarobot.com',
        'creatorUserId': '5a530498d5c1f302d6d176c5',
        'lastModifiedUserId': '5a530498d5c1f302d6d176c5',
        'numberOfProjects': 2,
        'linkageKeys': ['user_id', 'dept_id'],
    }


@pytest.fixture
def list_feature_engineering_graph_response(create_feature_engineering_graph_items,
                                            create_feature_engineering_graph_relationships):
    return {
        'data': [
            {
                'id': '5a530498d5c1f302d6d176c8',
                'name': 'Customer Features',
                'description': 'Credit card customer features (using activity in last 2 months)',
                'tableDefinitions': create_feature_engineering_graph_items,
                'relationships': create_feature_engineering_graph_relationships,
                'featureDerivationWindowStart': -14,
                'featureDerivationWindowEnd': -1,
                'timeUnit': 'DAY',
                'created': '2016-07-26T02:29:58.546312Z',
                'lastModified': '2016-07-26T02:29:58.546312Z',
                'creatorFullName': 'abc@datarobot.com',
                'modifierFullName': 'abc@datarobot.com',
                'creatorUserId': '5a530498d5c1f302d6d176c5',
                'lastModifiedUserId': '5a530498d5c1f302d6d176c5',
                'numberOfProjects': 2,
                'linkageKeys': ['user_id', 'dept_id'],
            },
            {
                'id': '5a530498d5c1f302d6d175c8',
                'name': 'Profile Features',
                'description': 'Profile feature',
                'tableDefinitions': create_feature_engineering_graph_items,
                'relationships': create_feature_engineering_graph_relationships,
                'featureDerivationWindowStart': -10,
                'featureDerivationWindowEnd': -1,
                'timeUnit': 'HOUR',
                'created': '2016-07-26T02:29:58.546312Z',
                'lastModified': '2016-07-26T02:29:58.546312Z',
                'creatorFullName': 'abc@datarobot.com',
                'modifierFullName': 'abc@datarobot.com',
                'creatorUserId': '5a530498d5c1f302d6d176c5',
                'lastModifiedUserId': '5a530498d5c1f302d6d176c5',
                'numberOfProjects': 2,
                'linkageKeys': ['user_id', 'p_id'],
            },
        ]
    }


@responses.activate
def test_feature_engineering_graph_creation(feature_engineering_graph_response,
                                            create_feature_engineering_graph_items,
                                            create_feature_engineering_graph_relationships):
    responses.add(responses.POST,
                  'https://host_name.com/featureEngineeringGraphs/',
                  json=feature_engineering_graph_response)

    feature_engineering_graph = FeatureEngineeringGraph()
    description = 'Credit card customer features (using activity in last 2 months)'
    created_feg = feature_engineering_graph.create(
        name='Customer Features',
        description=description,
        table_definitions=create_feature_engineering_graph_items,
        relationships=create_feature_engineering_graph_relationships,
        time_unit='DAY',
        feature_derivation_window_start=-14,
        feature_derivation_window_end=-1)
    assert responses.calls[0].request.method == 'POST'
    assert created_feg.feature_engineering_graph_id == '5a530498d5c1f302d6d176c8'
    assert created_feg.name == 'Customer Features'
    assert created_feg.description == description
    assert len(created_feg.table_definitions) == 2
    assert len(created_feg.relationships) == 2
    assert created_feg.time_unit == feature_engineering_graph_response['timeUnit']
    assert created_feg.feature_derivation_window_start == -14
    assert created_feg.feature_derivation_window_end == -1
    assert isinstance(created_feg.created, datetime.datetime)
    assert isinstance(created_feg.last_modified, datetime.datetime)
    assert isinstance(created_feg.created, datetime.datetime)


@responses.activate
def test_feature_engineering_graph_replace(feature_engineering_graph_response,
                                           create_feature_engineering_graph_items,
                                           create_feature_engineering_graph_relationships):
    responses.add(responses.PUT,
                  'https://host_name.com/featureEngineeringGraphs/F-ID/',
                  status=200,
                  json=feature_engineering_graph_response)

    feature_engineering_graph = FeatureEngineeringGraph()
    description = 'Credit card customer features (using activity in last 2 months)'
    updated_feg = feature_engineering_graph.replace(
        id='F-ID',
        name='Customer Features',
        description=description,
        table_definitions=create_feature_engineering_graph_items,
        relationships=create_feature_engineering_graph_relationships,
        time_unit='DAY',
        feature_derivation_window_start=-14,
        feature_derivation_window_end=-1,
        is_draft=False)
    assert responses.calls[0].request.method == 'PUT'
    payload = request_body_to_json(responses.calls[0].request)
    assert payload['name'] == 'Customer Features'
    assert len(payload['tableDefinitions']) == 2
    assert len(payload['relationships']) == 2
    assert payload['timeUnit'] == 'DAY'
    assert payload['featureDerivationWindowStart'] == -14
    assert payload['featureDerivationWindowEnd'] == -1

    assert updated_feg.feature_engineering_graph_id == '5a530498d5c1f302d6d176c8'
    assert updated_feg.name == 'Customer Features'
    assert updated_feg.description == description
    assert len(updated_feg.table_definitions) == 2
    assert len(updated_feg.relationships) == 2
    assert updated_feg.time_unit == 'DAY'
    assert updated_feg.feature_derivation_window_start == -14
    assert updated_feg.feature_derivation_window_end == -1
    assert isinstance(updated_feg.created, datetime.datetime)
    assert isinstance(updated_feg.last_modified, datetime.datetime)


@responses.activate
def test_feature_engineering_graph_updation():
    responses.add(responses.PATCH,
                  'https://host_name.com/featureEngineeringGraphs/F-ID/',
                  status=200,
                  json={'name': 'new-name', 'description': 'new-descrip'})

    feature_engineering_graph = FeatureEngineeringGraph('F-ID')
    feature_engineering_graph.update(
        name='new-name',
        description='new-descrip')

    assert responses.calls[0].request.method == 'PATCH'
    payload = request_body_to_json(responses.calls[0].request)
    assert payload['name'] == 'new-name'
    assert payload['description'] == 'new-descrip'


@responses.activate
def test_feature_engineering_graph_retrieve(feature_engineering_graph_response):
    graph_id = feature_engineering_graph_response['id']
    responses.add(
        responses.GET,
        'https://host_name.com/featureEngineeringGraphs/{}/'.format(graph_id),
        json=feature_engineering_graph_response
    )

    feature_engineering_graph = FeatureEngineeringGraph.get(feature_engineering_graph_id=graph_id)

    assert responses.calls[0].request.method == 'GET'
    assert feature_engineering_graph.feature_engineering_graph_id == graph_id
    assert feature_engineering_graph.name == 'Customer Features'
    assert len(feature_engineering_graph.table_definitions) == 2
    assert len(feature_engineering_graph.relationships) == 2
    assert feature_engineering_graph.time_unit == 'DAY'
    assert feature_engineering_graph.feature_derivation_window_start == -14
    assert feature_engineering_graph.feature_derivation_window_end == -1
    assert isinstance(feature_engineering_graph.created, datetime.datetime)
    assert isinstance(feature_engineering_graph.last_modified, datetime.datetime)
    assert isinstance(feature_engineering_graph.created, datetime.datetime)


@responses.activate
def test_feature_engineering_graph_list(list_feature_engineering_graph_response):
    responses.add(responses.GET,
                  'https://host_name.com/featureEngineeringGraphs/',
                  json=list_feature_engineering_graph_response)

    graphs = FeatureEngineeringGraph.list()

    for graph, server_payload in zip(graphs, list_feature_engineering_graph_response['data']):
        assert graph.feature_engineering_graph_id == server_payload['id']
        assert graph.name == server_payload['name']
        assert graph.description == server_payload['description']
        assert len(graph.table_definitions) == 2
        assert len(graph.relationships) == 2
        fdw = server_payload['featureDerivationWindowStart']
        assert graph.feature_derivation_window_start == fdw
        assert graph.feature_derivation_window_end == server_payload['featureDerivationWindowEnd']
        assert graph.time_unit == server_payload['timeUnit']
        assert graph.creator_full_name == server_payload['creatorFullName']
        assert graph.modifier_full_name == server_payload['modifierFullName']
        assert graph.number_of_projects == server_payload['numberOfProjects']
        assert graph.linkage_keys == server_payload['linkageKeys']


@responses.activate
def test_delete(feature_engineering_graph_response):
    graph_id = feature_engineering_graph_response['id']
    responses.add(
        responses.GET,
        'https://host_name.com/featureEngineeringGraphs/{}/'.format(graph_id),
        json=feature_engineering_graph_response
    )
    delete_url = 'https://host_name.com/featureEngineeringGraphs/{}/'.format(graph_id)
    responses.add(responses.DELETE, delete_url)

    feature_engineering_graph = FeatureEngineeringGraph.get(graph_id)
    feature_engineering_graph.delete()

    assert responses.calls[1].request.method == responses.DELETE
    assert responses.calls[1].request.url == delete_url


@responses.activate
def test_share(feature_engineering_graph_response):
    graph = FeatureEngineeringGraph.from_server_data(feature_engineering_graph_response)
    request = SharingAccess('me@datarobot.com', 'EDITOR')
    responses.add(responses.PATCH,
                  'https://host_name.com/featureEngineeringGraphs/{}/accessControls/'.
                  format(graph.feature_engineering_graph_id),
                  status=200)

    graph.share([request])

    actual_payload = request_body_to_json(responses.calls[0].request)
    assert actual_payload == {'permissions': [{'username': 'me@datarobot.com', 'role': 'EDITOR'}]}


@responses.activate
def test_remove(feature_engineering_graph_response):
    graph = FeatureEngineeringGraph.from_server_data(feature_engineering_graph_response)
    request = SharingAccess('me@datarobot.com', None)
    responses.add(responses.PATCH,
                  'https://host_name.com/featureEngineeringGraphs/{}/accessControls/'.
                  format(graph.feature_engineering_graph_id),
                  status=200)

    graph.share([request])

    actual_payload = request_body_to_json(responses.calls[0].request)
    assert actual_payload == {'permissions': [{'username': 'me@datarobot.com', 'role': None}]}


@responses.activate
def test_get_access_list(feature_engineering_graph_response):
    graph = FeatureEngineeringGraph.from_server_data(feature_engineering_graph_response)
    access_list = {
        'data': [
            {'username': 'me@datarobot.com',
             'userId': '1234deadbeeffeeddead4321',
             'role': 'OWNER',
             'canShare': True
             }
        ],
        'count': 1,
        'previous': None,
        'next': None
    }

    access_record = access_list['data'][0]
    responses.add(responses.GET,
                  'https://host_name.com/featureEngineeringGraphs/{}/accessControls/'.
                  format(graph.feature_engineering_graph_id),
                  json=access_list)

    response = graph.get_access_list()
    assert len(response) == 1

    share_info = response[0]
    assert share_info.username == access_record['username']
    assert share_info.user_id == access_record['userId']
    assert share_info.role == access_record['role']
    assert share_info.can_share == access_record['canShare']
