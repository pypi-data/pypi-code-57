import json

import pytest
import responses

from datarobot import Project


@pytest.fixture
def project(project_with_target_data):
    return Project.from_data(project_with_target_data)


@pytest.fixture
def feature_association_details_data():
    return {
        "values": [
            [
                168,
                33,
                0.045
            ],
            [
                1,
                1,
                0.329
            ],
            [
                37,
                17,
                0.005
            ],
            [
                207,
                41,
                0.014
            ],
            [
                178,
                35,
                0.006
            ],
            [
                34,
                16,
                0.032
            ],
            [
                194,
                37,
                0.004
            ]
        ],
        "features": [
            "area1",
            "area2"
        ],
        "types": [
            "N",
            "N"
        ]
    }


@pytest.fixture
def feature_association_featurelists():
    return {
        "featurelists": [
            {
                "featurelistId": "54e510ef8bd88f5aeb02a3ed",
                "hasFam": True,
                "title": "Informative Features"
            }
        ]
    }


@pytest.fixture
def feature_association_list_url(project_id):
    base_url = 'https://host_name.com/projects/{}/featureAssociationMatrixDetails/' \
        .format(project_id)
    base_url += '?feature1=area1&feature2=area2'
    return base_url


@pytest.fixture
def feature_association_featurelist_url(project_id):
    url = 'https://host_name.com/projects/{}/featureAssociationFeaturelists/' \
        .format(project_id)
    return url


@responses.activate
def test_get_feature_association_details(feature_association_details_data,
                                         feature_association_list_url,
                                         project, project_id):
    responses.add(
        responses.GET,
        feature_association_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps(feature_association_details_data)
    )
    feature_values = project.get_association_matrix_details(feature1='area1', feature2='area2')

    assert len(feature_values.keys()) == 3
    assert len(feature_values['values']) == 7
    assert feature_values['features'] == ['area1', 'area2']


@responses.activate
def test_get_feature_association_featurelists(feature_association_featurelists,
                                              feature_association_featurelist_url,
                                              project, project_id):
    responses.add(
        responses.GET,
        feature_association_featurelist_url,
        status=200,
        content_type='application/json',
        body=json.dumps(feature_association_featurelists)
    )
    featurelists = project.get_association_featurelists()

    assert len(featurelists.keys()) == 1
    assert len(featurelists['featurelists']) == 1
    assert featurelists['featurelists'][0]['title'] == 'Informative Features'
