import json

import pandas as pd
import pytest
import responses

from datarobot import Predictions
from datarobot.utils import parse_time


@pytest.fixture
def sample_prediction():
    return {
        u'positiveClass': None,
        u'task': u'Regression',
        u'predictions': [
            {u'positiveProbability': None, u'prediction': 32.0,
             u'rowId': 0},
            {u'positiveProbability': None, u'prediction': 100.0,
             u'rowId': 1},
            {u'positiveProbability': None, u'prediction': 212.0,
             u'rowId': 2}
        ]
    }


@pytest.fixture
def sample_prediction_metadata(prediction_id):
    project_id = '59d92fe8962d7464ca8c6bd6'
    url = 'http://localhost/api/v2/projects/{}/predictions/{}/'.format(
        project_id,
        prediction_id)

    return {
        'projectId': project_id,
        'id': prediction_id,
        'predictionDatasetId': 'a_dataset_id',
        'modelId': 'a_model_id',
        'includesPredictionIntervals': False,
        'predictionIntervalsSize': None,
        'url': url,
        'forecastPoint': '2017-01-01T15:00:00Z',
        'predictionsStartDate': None,
        'predictionsEndDate': None,
    }


@pytest.fixture
def prediction_id():
    return '59d92fe8962d7464ca8c6bd6'


@pytest.fixture
def model_id():
    return "modelid"


@pytest.fixture
def dataset_id():
    return "datasetid"


@responses.activate
def test_get__fetches_metadata(project_id, prediction_id, sample_prediction_metadata):
    metadata_url = 'https://host_name.com/projects/{}/predictionsMetadata/{}/'.format(
        project_id,
        prediction_id,
    )
    responses.add(
        responses.GET,
        metadata_url,
        body=json.dumps(sample_prediction_metadata),
        status=200,
        content_type='application/json',
    )

    preds = Predictions.get(project_id, prediction_id)

    assert preds.project_id == project_id
    assert preds.prediction_id == prediction_id
    assert preds.model_id == sample_prediction_metadata['modelId']
    assert preds.dataset_id == sample_prediction_metadata['predictionDatasetId']
    assert preds.includes_prediction_intervals == (
            sample_prediction_metadata['includesPredictionIntervals']
    )
    assert preds.forecast_point == parse_time(sample_prediction_metadata['forecastPoint'])
    assert preds.predictions_start_date == parse_time(
        sample_prediction_metadata['predictionsStartDate']
    )
    assert preds.predictions_end_date == parse_time(
        sample_prediction_metadata['predictionsEndDate']
    )


@responses.activate
def test_list__ok(project_id, model_id, prediction_id, dataset_id):
    prediction_stub = {
        'url': 'http://localhost/api/v2/projects/{}/predictions/{}/'.format(project_id,
                                                                            prediction_id),
        'id': prediction_id,
        'modelId': model_id,
        'predictionDatasetId': dataset_id,
        'includesPredictionIntervals': False,
        'forecastPoint': '2017-01-01T15:00:00Z',
    }
    responses.add(
        responses.GET,
        'https://host_name.com/projects/{}/predictionsMetadata/'.format(
            project_id,
        ),
        status=200,
        body=json.dumps({'data': [prediction_stub]}),
    )

    predictions_list = Predictions.list(project_id)

    assert len(predictions_list) == 1
    prediction = predictions_list[0]
    assert prediction.project_id == project_id
    assert prediction.model_id == model_id
    assert prediction.dataset_id == dataset_id
    assert prediction.prediction_id == prediction_id
    assert not prediction.includes_prediction_intervals
    assert prediction.prediction_intervals_size is None
    assert prediction.forecast_point == parse_time(prediction_stub['forecastPoint'])
    assert prediction.predictions_start_date is None
    assert prediction.predictions_end_date is None


@responses.activate
def test_get_all_as_dataframe__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        sample_prediction, sample_prediction_metadata
):
    url = 'https://host_name.com/projects/{}/predictions/{}/'.format(
        project_id,
        prediction_id,
    )
    metadata_url = 'https://host_name.com/projects/{}/predictionsMetadata/{}/'.format(
        project_id,
        prediction_id,
    )
    responses.add(
        responses.GET,
        url,
        body=json.dumps(sample_prediction),
        status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        metadata_url,
        body=json.dumps(sample_prediction_metadata),
        status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = Predictions.get(project_id, prediction_id)
    data_frame = obj.get_all_as_dataframe()

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame.shape == (len(sample_prediction['predictions']), 2)
    assert list(data_frame.columns) == [
        'prediction',
        'row_id',
    ]


def test_repr():
    preds = Predictions('project_id', 'prediction_id', 'model_id', 'dataset_id', False)

    assert repr(preds) == "Predictions(prediction_id='prediction_id', project_id='project_id', " \
                          "model_id='model_id', dataset_id='dataset_id', " \
                          "includes_prediction_intervals=False, prediction_intervals_size=None, " \
                          "forecast_point=None, predictions_start_date=None, " \
                          "predictions_end_date=None)"
