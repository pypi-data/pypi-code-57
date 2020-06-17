import json
import pytest
import responses

from datarobot import CustomInferenceModel, TARGET_TYPE
from datarobot.utils import underscorize

from tests.model.utils import assert_custom_model_version


@pytest.fixture
def mocked_models(mocked_custom_model_version, mocked_custom_model_version2):
    return {
        "count": 2,
        "totalCount": 2,
        "next": None,
        "data": [
            {
                "deploymentsCount": 0,
                "updated": "2020-04-30T09:55:38.319786Z",
                "supportsBinaryClassification": False,
                "description": "",
                "language": "",
                "created": "2020-04-30T09:55:38.319558Z",
                "supportsRegression": True,
                "createdBy": "admin@datarobot.com",
                "latestVersion": mocked_custom_model_version,
                "customModelType": "learning",
                "id": "5eaaa09a40240308176cee55",
                "name": "dddd",
            },
            {
                "multiseriesIdColumns": None,
                "supportsRegression": True,
                "trainingDatasetVersionId": "5ea6bbc7402403321d4e1fae",
                "timeSteps": None,
                "latestVersion": mocked_custom_model_version2,
                "targetName": "MEDV",
                "id": "5ea6b5da402403181895cc51",
                "featureDerivationWindowEnd": None,
                "datetimePartitionColumn": None,
                "trainingDatasetId": "5ea6bbc7402403321d4e1fad",
                "trainingDataPartitionColumn": None,
                "positiveClassLabel": "1",
                "customModelType": "inference",
                "updated": "2020-04-27T10:37:14.341673Z",
                "supportsBinaryClassification": False,
                "description": "",
                "negativeClassLabel": "0",
                "createdBy": "admin@datarobot.com",
                "timeUnit": None,
                "predictionThreshold": 0.5,
                "trainingDataFileName": "boston_housing.csv",
                "forecastWindowStart": None,
                "deploymentsCount": 0,
                "name": "ee",
                "language": "",
                "created": "2020-04-27T10:37:14.340932Z",
                "forecastWindowEnd": None,
                "isTimeSeries": False,
                "trainingDataAssignmentInProgress": False,
                "featureDerivationWindowStart": None,
            },
        ],
        "previous": None,
    }


@pytest.fixture
def mocked_learning_model(mocked_models):
    return mocked_models["data"][0]


@pytest.fixture
def mocked_inference_model(mocked_models):
    return mocked_models["data"][1]


def assert_custom_model_common(model, model_json):
    assert model.id == model_json["id"]
    assert model.name == model_json["name"]
    assert model.description == model_json["description"]
    assert (
        (model.target_type == TARGET_TYPE.BINARY) == model_json["supportsBinaryClassification"]
    )
    assert (
        (model.target_type == TARGET_TYPE.REGRESSION) == model_json["supportsRegression"]
    )
    assert_custom_model_version(model.latest_version, model_json["latestVersion"])
    assert model.deployments_count == model_json["deploymentsCount"]
    assert model.created_by == model_json["createdBy"]
    assert model.updated_at == model_json["updated"]
    assert model.created_at == model_json["created"]


def assert_inference_model(model, model_json):
    assert_custom_model_common(model, model_json)
    assert model.language == model_json["language"]
    assert model.target_name == model_json["targetName"]
    assert model.training_dataset_id == model_json["trainingDatasetId"]
    assert model.training_dataset_version_id == model_json["trainingDatasetVersionId"]
    assert model.training_data_file_name == model_json["trainingDataFileName"]
    assert (
        model.training_data_assignment_in_progress == model_json["trainingDataAssignmentInProgress"]
    )
    assert model.positive_class_label == model_json["positiveClassLabel"]
    assert model.negative_class_label == model_json["negativeClassLabel"]
    assert model.prediction_threshold == model_json["predictionThreshold"]
    assert model.training_data_partition_column == model_json["trainingDataPartitionColumn"]


@pytest.fixture
def make_models_url(unittest_endpoint):
    def _make_models_url(model_id=None):
        base_url = "{}/customModels/".format(unittest_endpoint)
        if model_id is not None:
            return "{}{}/".format(base_url, model_id)
        return base_url

    return _make_models_url


def mock_get_response(url, response):
    responses.add(
        responses.GET,
        url,
        status=200,
        content_type="application/json",
        body=json.dumps(response),
    )


class TestCustomInferenceModel(object):
    def test_from_server_data(self, mocked_inference_model):
        model = CustomInferenceModel.from_server_data(mocked_inference_model)
        assert_inference_model(model, mocked_inference_model)

    @responses.activate
    def test_get_version(self, mocked_inference_model, make_models_url):
        # arrange
        url = make_models_url(mocked_inference_model["id"])
        mock_get_response(url, mocked_inference_model)

        # act
        model = CustomInferenceModel.get(mocked_inference_model["id"])

        # assert
        assert_inference_model(model, mocked_inference_model)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_list_versions(self, make_models_url, mocked_inference_model):
        # arrange
        url = make_models_url() + "?customModelType=inference"
        mock_get_response(
            url,
            {
                "count": 1,
                "totalCount": 1,
                "next": None,
                "previous": None,
                "data": [mocked_inference_model],
            },
        )

        # act
        models = CustomInferenceModel.list()

        # assert
        assert len(models) == 1
        assert_inference_model(models[0], mocked_inference_model)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update(self, make_models_url, mocked_inference_model):
        # arrange
        attrs = {"description": "xx", "predictionThreshold": 0.1}

        url = make_models_url(mocked_inference_model["id"])
        mock_get_response(url, mocked_inference_model)

        mocked_inference_model.update(attrs)

        responses.add(
            responses.PATCH,
            url,
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )

        # act
        model = CustomInferenceModel.get(mocked_inference_model["id"])
        model.update(**{underscorize(k): v for k, v in attrs.items()})

        # assert
        assert_inference_model(model, mocked_inference_model)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "PATCH"
        assert responses.calls[1].request.url == url
        assert responses.calls[1].request.body == json.dumps(attrs).encode()

    @responses.activate
    def test_refresh(self, make_models_url, mocked_inference_model):
        # arrange
        url = make_models_url(mocked_inference_model["id"])
        mock_get_response(url, mocked_inference_model)

        mocked_inference_model.update({"description": "xx", "predictionThreshold": 0.1})

        mock_get_response(url, mocked_inference_model)

        # act
        model = CustomInferenceModel.get(mocked_inference_model["id"])
        model.refresh()

        # assert
        assert_inference_model(model, mocked_inference_model)

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == url

    @responses.activate
    def test_delete(self, make_models_url, mocked_inference_model):
        url = make_models_url(mocked_inference_model["id"])

        mock_get_response(url, mocked_inference_model)
        responses.add(
            responses.DELETE, url, status=204, content_type="application/json",
        )

        model = CustomInferenceModel.get(mocked_inference_model["id"])
        model.delete()

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "DELETE"
        assert responses.calls[1].request.url == url

    @responses.activate
    def test_download(self, make_models_url, mocked_inference_model, tmpdir):
        # arrange
        url = make_models_url(mocked_inference_model["id"])
        mock_get_response(url, mocked_inference_model)
        responses.add(
            responses.GET,
            url + "download/",
            status=200,
            content_type="application/json",
            body=b"content",
        )

        downloaded_file = tmpdir.mkdir("sub").join("download")
        downloaded_file_path = str(downloaded_file)

        # act
        model = CustomInferenceModel.get(mocked_inference_model["id"])
        model.download_latest_version(downloaded_file_path)

        # assert
        downloaded_file.read() == b"content"

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == url
        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == url + "download/"

    @responses.activate
    def test_assign_training_data_non_blocking(
        self, unittest_endpoint, make_models_url, mocked_inference_model, tmpdir
    ):
        status_url = '{}/status_url'.format(unittest_endpoint)

        mocked_inference_model["trainingDataAssignmentInProgress"] = False
        responses.add(
            responses.GET,
            make_models_url(mocked_inference_model["id"]),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )
        responses.add(
            responses.PATCH,
            make_models_url(mocked_inference_model["id"]) + "trainingData/",
            status=200,
            content_type="application/json",
            headers={'Location': status_url},
            body=json.dumps({"id": mocked_inference_model["id"]}),
        )
        mocked_inference_model["trainingDataAssignmentInProgress"] = True
        responses.add(
            responses.GET,
            make_models_url(mocked_inference_model["id"]),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )

        model = CustomInferenceModel.get(mocked_inference_model["id"])

        assert not model.training_data_assignment_in_progress
        model.assign_training_data("5ea6bbc7402403321d4e1fae", max_wait=None)

        assert model.training_data_assignment_in_progress

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == make_models_url(
            mocked_inference_model["id"]
        )
        assert responses.calls[1].request.method == "PATCH"
        assert responses.calls[1].request.url == make_models_url(
            mocked_inference_model["id"]
        ) + "trainingData/"
        assert responses.calls[2].request.method == "GET"
        assert responses.calls[2].request.url == make_models_url(
            mocked_inference_model["id"]
        )

    @responses.activate
    def test_assign_training_data_blocking(
        self, unittest_endpoint, make_models_url, mocked_inference_model, tmpdir
    ):
        status_url = '{}/status_url'.format(unittest_endpoint)

        mocked_inference_model["trainingDataAssignmentInProgress"] = False
        responses.add(
            responses.GET,
            make_models_url(mocked_inference_model["id"]),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )
        responses.add(
            responses.PATCH,
            make_models_url(mocked_inference_model["id"]) + "trainingData/",
            status=200,
            content_type="application/json",
            headers={'Location': status_url},
            body=json.dumps({"id": mocked_inference_model["id"]}),
        )
        responses.add(
            responses.GET,
            status_url,
            status=303,
            content_type="application/json",
            headers={'Location': status_url},
        )
        responses.add(
            responses.GET,
            make_models_url(mocked_inference_model["id"]),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )

        model = CustomInferenceModel.get(mocked_inference_model["id"])

        assert not model.training_data_assignment_in_progress
        model.assign_training_data("5ea6bbc7402403321d4e1fae")

        assert not model.training_data_assignment_in_progress

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == make_models_url(
            mocked_inference_model["id"]
        )
        assert responses.calls[1].request.method == "PATCH"
        assert responses.calls[1].request.url == make_models_url(
            mocked_inference_model["id"]
        ) + "trainingData/"
        assert responses.calls[2].request.method == "GET"
        assert responses.calls[2].request.url == status_url
        assert responses.calls[3].request.method == "GET"
        assert responses.calls[3].request.url == make_models_url(
            mocked_inference_model["id"]
        )

    @responses.activate
    def test_create(self, make_models_url, mocked_inference_model):
        responses.add(
            responses.POST,
            make_models_url(),
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )

        model = CustomInferenceModel.create(
            mocked_inference_model["name"],
            TARGET_TYPE.REGRESSION,
            mocked_inference_model["targetName"],
        )
        assert_inference_model(model, mocked_inference_model)

        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == make_models_url()

    @responses.activate
    def test_create_copy(self, make_models_url, mocked_inference_model):
        custom_model_to_copy = "5ea6bbc7402403321d4e1fad"

        url = make_models_url() + "fromCustomModel/"
        responses.add(
            responses.POST,
            url,
            status=200,
            content_type="application/json",
            body=json.dumps(mocked_inference_model),
        )

        model = CustomInferenceModel.copy_custom_model(custom_model_to_copy)
        assert_inference_model(model, mocked_inference_model)

        req = responses.calls[0].request
        assert req.method == "POST"
        assert req.url == url
        assert json.loads(req.body) == {'customModelId': custom_model_to_copy}
