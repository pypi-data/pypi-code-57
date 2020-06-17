import csv
import io
import json
import six
import tempfile

import pandas as pd
import pytest
import responses
import trafaret

from datarobot import TrainingPredictions
from datarobot.models.training_predictions import TrainingPredictionsRow


def _write_csv(lines):

    if six.PY2:

        buf = io.BytesIO()
        wr = csv.writer(buf)
        wr.writerows(lines)
        return buf.getvalue()

    buf = io.StringIO()
    wr = csv.writer(buf)
    wr.writerows(lines)
    return buf.getvalue().encode('utf-8')


@pytest.fixture
def prediction_id():
    return '59d92fe8962d7464ca8c6bd6'


@responses.activate
def test_get__no_requests_made(project_id, prediction_id):
    TrainingPredictions.get(project_id, prediction_id)
    assert len(responses.calls) == 0


@responses.activate
def test_list__ok(project_id, model_id, prediction_id):
    training_prediction_stub = {
        'url': 'https://host_name.com/projects/{}/trainingPredictions/{}//'.format(
            project_id,
            prediction_id,
        ),
        'id': prediction_id,
        'modelId': model_id,
        'dataSubset': 'all',
    }
    responses.add(
        responses.GET,
        'https://host_name.com/projects/{}/trainingPredictions/'.format(
            project_id,
        ),
        status=200,
        body=json.dumps({'data': [training_prediction_stub]}),
    )

    training_predictions_list = TrainingPredictions.list(project_id)

    assert len(training_predictions_list) == 1
    training_prediction = training_predictions_list[0]
    assert training_prediction.project_id == project_id
    assert training_prediction.model_id == model_id
    assert training_prediction.prediction_id == prediction_id


@responses.activate
def test_list__no_url_in_api_response__error(project_id, model_id, prediction_id):
    training_prediction_stub = {
        'url': '',
        'id': prediction_id,
        'modelId': model_id,
        'trainingPredictionSet': 'all',
    }
    responses.add(
        responses.GET,
        'https://host_name.com/projects/{}/trainingPredictions/'.format(
            project_id,
        ),
        status=200,
        body=json.dumps({'data': [training_prediction_stub]}),
    )

    with pytest.raises(trafaret.DataError):
        TrainingPredictions.list(project_id)


@responses.activate
def test_iterate_rows__empty_predictions__ok(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response = {'data': [], 'next': '{}?offset=100&limit=100'.format(url)}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)

    assert list(obj.iterate_rows()) == []


@responses.activate
def test_iterate_rows__malfromed_predictions__data_error(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    items = [{
        'row_id': 'wrong-id',
        'partition_id': 'holdout',
        'prediction': 0.42,
        'prediction_values': [],
    }]
    response = {'data': items, 'next': '{}?offset=100&limit=100'.format(url)}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    with pytest.raises(trafaret.DataError):
        obj = TrainingPredictions.get(project_id, prediction_id)
        it = obj.iterate_rows()
        next(it)


@responses.activate
def test_iterate_rows__extra_fields__ignored(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    items = [{
        'row_id': 1,
        'partition_id': 2,
        'prediction': 0.42,
        'prediction_values': [{
            'label': 'test-label',
            'value': 0.42,
            'extra-prediction': 'you are going to win a lottery for sure',
        }]},
    ]
    response = {'data': items, 'next': '{}?offset=100&limit=100'.format(url), 'prev': None}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    assert list(obj.iterate_rows()) == [TrainingPredictionsRow(
        row_id=1,
        partition_id=2,
        prediction=0.42,
        prediction_values=[{
            'label': 'test-label',
            'value': 0.42,
        }],
        timestamp=None,
        forecast_point=None,
        forecast_distance=None,
        series_id=None,
    )]


@responses.activate
def test_iterate_rows__all_rows_at_once__ok(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    items = [
        {'row_id': 1, 'partition_id': 2, 'prediction': 0.42, 'prediction_values': []},
        {'row_id': 2, 'partition_id': 2, 'prediction': 0.22, 'prediction_values': []},
        {'row_id': 3, 'partition_id': 2, 'prediction': 0.82, 'prediction_values': []},
    ]
    response = {'data': items, 'next': None, 'prev': None}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    assert len(list(obj.iterate_rows(batch_size=3))) == 3


@responses.activate
def test_iterate_rows__one_prediction__ok(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    items = [
        {'row_id': 1, 'partition_id': 2, 'prediction': 0.42, 'prediction_values': []},
    ]
    response = {'data': items, 'next': '{}?offset=100&limit=100'.format(url)}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)

    assert list(obj.iterate_rows()) == [
        TrainingPredictionsRow(
            row_id=1,
            partition_id=2,
            prediction=0.42,
            prediction_values=[],
            timestamp=None,
            forecast_point=None,
            forecast_distance=None,
            series_id=None,
        ),
    ]
    assert len(responses.calls) == 1


@responses.activate
def test_iterate_rows__two_predictions_with_limit_equals_one__three_requests_were_made(
        project_id, prediction_id,
):
    items = [
        {'row_id': 1, 'partition_id': 2, 'prediction': 0.42, 'prediction_values': []},
        {'row_id': 2, 'partition_id': 2, 'prediction': 0.22, 'prediction_values': []},
    ]
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    body = {'data': items[:1], 'next': '{}?offset=1&limit=1'.format(url)}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(body),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)

    it = obj.iterate_rows(batch_size=1)

    assert next(it, None) == TrainingPredictionsRow(
        row_id=1,
        partition_id=2,
        prediction=0.42,
        prediction_values=[],
        timestamp=None,
        forecast_point=None,
        forecast_distance=None,
        series_id=None,
    )
    assert len(responses.calls) == 1

    body2 = {'data': items[1:], 'next': '{}?offset=2&limit=1'.format(url)}
    responses.reset()
    responses.add(
        responses.GET,
        url,
        body=json.dumps(body2),
        status=200,
        content_type='application/json',
        match_querystring=False,
    )

    assert next(it, None) == TrainingPredictionsRow(
        row_id=2,
        partition_id=2,
        prediction=0.22,
        prediction_values=[],
        timestamp=None,
        forecast_point=None,
        forecast_distance=None,
        series_id=None,
    )
    assert len(responses.calls) == 1

    body = {'data': [], 'next': '{}?offset=3&limit=1'.format(url)}
    responses.reset()
    responses.add(
        responses.GET,
        url,
        body=json.dumps(body),
        status=200,
        content_type='application/json',
    )

    assert next(it, None) is None
    assert len(responses.calls) == 1


@responses.activate
@pytest.mark.parametrize(['serializer', 'response'], [
    pytest.param('json', {
        'body': lambda url: json.dumps({'data': [
            {'row_id': 1, 'partition_id': 2, 'prediction': 0.42, 'prediction_values': []},
            {'row_id': 2, 'partition_id': 2, 'prediction': 0.22, 'prediction_values': []},
        ], 'next': '{}?limit=20'.format(url)}),
        'content_type': 'application/json',
    }, id='json'),
    pytest.param('csv', {
        'body': lambda url: _write_csv([
            ['row_id', 'partition_id', 'prediction'],
            [1, 2, 0.42],
            [2, 2, 0.22],
        ]),
        'content_type': 'text/csv',
        'stream': True,
    }, id='csv')
])
def test_get_all_as_dataframe__regression_two_predictions__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        serializer, response,
):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response['body'] = response['body'](url)
    responses.add(
        responses.GET,
        url,
        status=200,
        **response
    )
    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    data_frame = obj.get_all_as_dataframe(serializer=serializer)

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame.shape == (2, 3)
    assert list(data_frame.columns) == [
        'row_id',
        'partition_id',
        'prediction',
    ]


@responses.activate
@pytest.mark.parametrize(['serializer', 'response'], [
    pytest.param('json', {
        'body': lambda url: json.dumps({'data': [
            {
                'row_id': 1,
                'partition_id': '1960-01-01T00:00:00.000000Z',
                'prediction': 0.42,
                'prediction_values': [],
                'timestamp': '1960-01-01T00:00:00.000000Z',
                'forecast_point': '1959-12-01T00:00:00.000000Z',
                'forecast_distance': 1,
                'series_id': None,
            },
            {
                'row_id': 2,
                'partition_id': '1960-01-01T00:00:00.000000Z',
                'prediction': 0.22,
                'prediction_values': [],
                'timestamp': '1959-11-01T00:00:00.000000Z',
                'forecast_point': '1959-12-01T00:00:00.000000Z',
                'forecast_distance': 2,
                'series_id': None,
            },
        ], 'next': '{}?limit=20'.format(url)}),
        'content_type': 'application/json',
    }, id='json'),
    pytest.param('csv', {
        'body': lambda url: _write_csv([
            [
                'row_id', 'partition_id', 'prediction', 'timestamp',
                'forecast_point', 'forecast_distance', 'series_id'
            ],
            [
                1,
                '1960-01-01T00:00:00.000000Z',
                0.42,
                '1960-01-01T00:00:00.000000Z',
                '1959-12-01T00:00:00.000000Z',
                1,
                None,
            ],
            [
                2,
                '1960-01-01T00:00:00.000000Z',
                0.22,
                '1959-11-01T00:00:00.000000Z',
                '1959-12-01T00:00:00.000000Z',
                2,
                None,
            ],
        ]),
        'content_type': 'text/csv',
        'stream': True,
    }, id='csv')
])
def test_get_all_as_dataframe__timeseries_predictions__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        serializer, response,
):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response['body'] = response['body'](url)
    responses.add(
        responses.GET,
        url,
        status=200,
        **response
    )
    project_data = json.loads(project_with_target_json)
    project_data['partition']['use_time_series'] = True
    responses.add(
        responses.GET,
        project_url,
        body=json.dumps(project_data),
        status=200,
        content_type='application/json'
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    data_frame = obj.get_all_as_dataframe(serializer=serializer)

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame.shape == (2, 7)
    assert set(data_frame.columns) == {
        'row_id', 'partition_id', 'prediction', 'timestamp',
        'forecast_point', 'forecast_distance', 'series_id'
    }

    assert len(data_frame) == 2
    assert None not in data_frame.timestamp.unique()
    assert None not in data_frame.forecast_point.unique()
    assert all(isinstance(value, int) for value in data_frame.forecast_distance)


@responses.activate
@pytest.mark.parametrize(['serializer', 'response'], [
    pytest.param('json', {
        'body': lambda url: json.dumps({'data': [
            {'row_id': 1, 'partition_id': 2, 'prediction': 0.42, 'prediction_values': []},
            {'row_id': 2, 'partition_id': 2, 'prediction': 0.22, 'prediction_values': []},
        ], 'next': '{}?limit=20'.format(url)}),
        'content_type': 'application/json',
    }, id='json'),
    pytest.param('csv', {
        'body': lambda url: _write_csv([
            ['row_id', 'partition_id', 'prediction'],
            [1, 2, 0.42],
            [2, 2, 0.22],
        ]),
        'content_type': 'text/csv',
        'stream': True,
    }, id='csv')
])
def test_download_to_csv__two_regression_predictions__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        serializer, response,
):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response['body'] = response['body'](url)
    responses.add(
        responses.GET,
        url,
        status=200,
        **response
    )
    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    with tempfile.NamedTemporaryFile(mode='r') as a_file:
        obj.download_to_csv(a_file.name, serializer=serializer)
        data_frame = pd.read_csv(a_file.name)

    assert data_frame.shape == (2, 3)
    assert set(data_frame.columns) == {'row_id', 'partition_id', 'prediction'}


@responses.activate
def test_iterate_rows__one_classification_prediction__ok(project_id, prediction_id):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    items = [
        {
            'row_id': 1,
            'partition_id': 2,
            'prediction': 0.42,
            'prediction_values': [
                {'label': 'good', 'value': 0.8},
                {'label': 'bad', 'value': 0.2},
            ],
        },
    ]
    response = {'data': items, 'next': '{}?offset=100&limit=100'.format(url)}
    responses.add(
        responses.GET,
        url,
        body=json.dumps(response),
        status=200,
        content_type='application/json',
    )

    obj = TrainingPredictions.get(project_id, prediction_id)

    assert list(obj.iterate_rows()) == [
        TrainingPredictionsRow(
            row_id=1,
            partition_id=2,
            prediction=0.42,
            prediction_values=[
                {'label': 'good', 'value': 0.8},
                {'label': 'bad', 'value': 0.2},
            ],
            timestamp=None,
            forecast_point=None,
            forecast_distance=None,
            series_id=None,
        ),
    ]
    assert len(responses.calls) == 1


@responses.activate
@pytest.mark.parametrize(['serializer', 'response'], [
    pytest.param('json', {
        'body': lambda url: json.dumps({'data': [{
            'row_id': 1,
            'partition_id': 2,
            'prediction': 0.42,
            'prediction_values': [
                {'label': 'good', 'value': 0.8},
                {'label': 'bad', 'value': 0.2},
            ],
        }], 'next': '{}?limit=20'.format(url)}),
        'content_type': 'application/json',
    }, id='json'),
    pytest.param('csv', {
        'body': lambda url: _write_csv([
            ['row_id', 'partition_id', 'prediction', 'foo_good', 'foo_bad'],
            [1, 2, 0.42, 0.8, 0.2],
        ]),
        'content_type': 'text/csv',
        'stream': True,
    }, id='csv')
])
def test_get_all_as_dataframe__one_classification_prediction__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        serializer, response,
):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response['body'] = response['body'](url)
    responses.add(
        responses.GET,
        url,
        status=200,
        **response
    )

    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    data_frame = obj.get_all_as_dataframe(
        class_prefix='foo_',
        serializer=serializer,
    )

    assert isinstance(data_frame, pd.DataFrame)
    assert data_frame.shape == (1, 5)
    assert set(data_frame.columns) == {
        'row_id', 'partition_id', 'prediction', 'foo_good', 'foo_bad'
    }


@responses.activate
@pytest.mark.parametrize(['serializer', 'response'], [
    pytest.param('json', {
        'body': lambda url: json.dumps({'data': [{
            'row_id': 1,
            'partition_id': 2,
            'prediction': 0.42,
            'prediction_values': [
                {'label': 'good', 'value': 0.3},
                {'label': 'bad', 'value': 0.2},
                {'label': 'ugly', 'value': 0.2},
                {'label': 'none', 'value': 0.0},
            ],
        }], 'next': '{}?limit=20'.format(url)}),
        'content_type': 'application/json',
    }, id='json'),
    pytest.param('csv', {
        'body': lambda url: _write_csv([
            [
                'row_id', 'partition_id', 'prediction', 'class_good', 'class_bad',
                'class_ugly', 'class_none',
            ],
            [1, 2, 0.42, 0.3, 0.2, 0.2, 0.0],
        ]),
        'content_type': 'text/csv',
        'stream': True,
    }, id='csv')
])
def test_download_to_csv__multiclass_project__prediction__ok(
        project_id, prediction_id,
        project_url, project_with_target_json,
        serializer, response,
):
    url = 'https://host_name.com/projects/{}/trainingPredictions/{}/'.format(
        project_id,
        prediction_id,
    )
    response['body'] = response['body'](url)
    responses.add(
        responses.GET,
        url,
        status=200,
        **response
    )

    responses.add(
        responses.GET,
        project_url,
        body=project_with_target_json,
        status=200,
        content_type='application/json'
    )

    obj = TrainingPredictions.get(project_id, prediction_id)
    with tempfile.NamedTemporaryFile(mode='r') as a_file:
        obj.download_to_csv(a_file.name, serializer=serializer)
        data_frame = pd.read_csv(a_file.name)

    assert data_frame.shape == (1, 7)
    assert set(data_frame.columns) == {
        'row_id', 'partition_id', 'prediction', 'class_good', 'class_bad',
        'class_ugly', 'class_none',
    }
