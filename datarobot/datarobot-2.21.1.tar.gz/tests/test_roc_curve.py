import json

import pytest
import responses
from datarobot.errors import ClientError

from datarobot.utils import from_api

from datarobot import Model

from datarobot.models.roc_curve import RocCurve


@pytest.fixture
def roc_curve_validation_data(model_id, roc_curve_data):
    return {
        'source': 'validation',
        'sourceModelId': model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


@pytest.fixture
def roc_curve_parent_model_validation_data(parent_model_id, roc_curve_data):
    return {
        'source': 'validation',
        'sourceModelId': parent_model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


@pytest.fixture
def roc_curve_parent_model_holdout_data(parent_model_id, roc_curve_data):
    return {
        'source': 'holdout',
        'sourceModelId': parent_model_id,
        'rocPoints': roc_curve_data['rocPoints'],
        'negativeClassPredictions': roc_curve_data['negativeClassPredictions'],
        'positiveClassPredictions': roc_curve_data['positiveClassPredictions']
    }


def test_instantiation(roc_curve_validation_data):
    roc = RocCurve.from_server_data(roc_curve_validation_data)

    assert roc.source == roc_curve_validation_data['source']
    assert roc.negative_class_predictions == roc_curve_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == roc_curve_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc.source_model_id == roc_curve_validation_data['sourceModelId']


def test_future_proof(roc_curve_validation_data):
    data_with_future_keys = dict(roc_curve_validation_data, new_key='some future roc data')
    data_with_future_keys['rocPoints'][0]['new_key'] = 'some future bin data'
    RocCurve.from_server_data(data_with_future_keys)


@pytest.fixture
def roc_curve_validation_data_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/validation/'.format(
        project_id,
        model_id
    )


@pytest.fixture
def roc_curve_parent_model_validation_data_url(project_id, parent_model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/validation/'.format(
        project_id,
        parent_model_id
    )


@pytest.fixture
def roc_curve_list_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/'.format(
        project_id,
        model_id
    )


@pytest.fixture
def roc_curve_parent_list_url(project_id, parent_model_id):
    return 'https://host_name.com/projects/{}/models/{}/rocCurve/'.format(
        project_id,
        parent_model_id
    )


@pytest.fixture
def frozen_model_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/frozenModels/{}/'.format(
        project_id,
        model_id
    )


@responses.activate
def test_get_validation_roc_curve(roc_curve_validation_data,
                                  roc_curve_validation_data_url,
                                  project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=200,
        content_type='application/json',
        body=json.dumps(roc_curve_validation_data)
    )
    model = Model(id=model_id, project_id=project_id)
    roc = model.get_roc_curve('validation')

    assert roc.source == roc_curve_validation_data['source']
    assert roc.negative_class_predictions == roc_curve_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == roc_curve_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc.source_model_id == model_id


@responses.activate
def test_get_frozen_validation_roc_curve_no_fallback(roc_curve_validation_data_url,
                                                     project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=404
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    with pytest.raises(ClientError):
        model.get_roc_curve('validation')


@responses.activate
@pytest.mark.usefixtures('known_warning')
def test_get_frozen_validation_roc_curve_with_fallback(
        roc_curve_parent_model_validation_data,
        roc_curve_validation_data_url,
        roc_curve_parent_model_validation_data_url,
        frozen_model_url,
        project_id, model_id, parent_model_id,
        frozen_json):
    responses.add(
        responses.GET,
        roc_curve_validation_data_url,
        status=404
    )
    responses.add(
        responses.GET,
        frozen_model_url,
        body=frozen_json,
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        roc_curve_parent_model_validation_data_url,
        status=200,
        content_type='application/json',
        body=json.dumps(roc_curve_parent_model_validation_data)
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc = model.get_roc_curve('validation', fallback_to_parent_insights=True)

    assert roc.source == roc_curve_parent_model_validation_data['source']
    assert roc.negative_class_predictions == \
        roc_curve_parent_model_validation_data['negativeClassPredictions']
    assert roc.positive_class_predictions == \
        roc_curve_parent_model_validation_data['positiveClassPredictions']
    assert roc.roc_points == from_api(roc_curve_parent_model_validation_data['rocPoints'])
    assert roc.source_model_id == parent_model_id


@responses.activate
def test_get_all_roc_curves(roc_curve_validation_data,
                            roc_curve_list_url,
                            project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    model = Model(id=model_id, project_id=project_id)
    roc_list = model.get_all_roc_curves()

    assert len(roc_list) == 1
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id


@responses.activate
def test_get_frozen_all_roc_curves_no_fallback(roc_curve_validation_data,
                                               roc_curve_list_url,
                                               project_id, model_id):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc_list = model.get_all_roc_curves()

    assert len(roc_list) == 1
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id


@responses.activate
@pytest.mark.usefixtures('known_warning')
def test_get_forzen_all_roc_curves_with_fallback(roc_curve_validation_data,
                                                 roc_curve_parent_model_validation_data,
                                                 roc_curve_parent_model_holdout_data,
                                                 roc_curve_list_url,
                                                 roc_curve_parent_list_url,
                                                 frozen_model_url,
                                                 project_id, model_id,
                                                 parent_model_id,
                                                 frozen_json):
    responses.add(
        responses.GET,
        roc_curve_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_validation_data]})
    )
    responses.add(
        responses.GET,
        frozen_model_url,
        body=frozen_json,
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        roc_curve_parent_list_url,
        status=200,
        content_type='application/json',
        body=json.dumps({'charts': [roc_curve_parent_model_validation_data,
                                    roc_curve_parent_model_holdout_data]})
    )
    model = Model(id=model_id, project_id=project_id, is_frozen=True)
    roc_list = model.get_all_roc_curves(fallback_to_parent_insights=True)

    assert len(roc_list) == 2
    assert roc_list[0].source == roc_curve_validation_data['source']
    assert roc_list[0].negative_class_predictions == roc_curve_validation_data[
        'negativeClassPredictions']
    assert roc_list[0].positive_class_predictions == roc_curve_validation_data[
        'positiveClassPredictions']
    assert roc_list[0].roc_points == from_api(roc_curve_validation_data['rocPoints'])
    assert roc_list[0].source_model_id == model_id

    assert roc_list[1].source == roc_curve_parent_model_holdout_data['source']
    assert roc_list[1].negative_class_predictions == roc_curve_parent_model_holdout_data[
        'negativeClassPredictions']
    assert roc_list[1].positive_class_predictions == roc_curve_parent_model_holdout_data[
        'positiveClassPredictions']
    assert roc_list[1].roc_points == from_api(roc_curve_parent_model_holdout_data['rocPoints'])
    assert roc_list[1].source_model_id == parent_model_id


def test_get_best_f1_threshold(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When calculate recommended threshold
    best_threshold = roc.get_best_f1_threshold()
    # Then f1 score for that threshold maximal from all ROC curve points
    best_f1 = roc.estimate_threshold(best_threshold)['f1_score']
    assert all(best_f1 >= roc_point['f1_score'] for roc_point in roc.roc_points)


def test_estimate_threshold_equal(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When estimating threshold equal to one of precalculated
    threshold = roc_curve_validation_data['rocPoints'][1]['threshold']
    # Then estimate_threshold return valid data
    assert roc.estimate_threshold(threshold)['threshold'] == threshold


def test_estimate_threshold_new(roc_curve_validation_data):
    # Given ROC curve data
    roc = RocCurve.from_server_data(roc_curve_validation_data)
    # When estimating threshold from outside of precalculated
    threshold = roc_curve_validation_data['rocPoints'][1]['threshold'] + 0.1
    # Then estimate_threshold return data for next threshold bigger then requested
    assert roc.estimate_threshold(threshold)['threshold'] > threshold
