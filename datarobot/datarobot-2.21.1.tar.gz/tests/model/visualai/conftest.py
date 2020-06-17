import json
from six.moves.urllib.parse import urljoin

import random
import pytest


@pytest.fixture
def visualai_url(project_url):
    return urljoin(project_url, "images/")


@pytest.fixture
def visualai_image_url(visualai_url, visualai_image_id):
    return urljoin(visualai_url, visualai_image_id + "/")


@pytest.fixture
def visualai_image_id():
    return "5e7e562528513130ab237875"


@pytest.fixture
def visualai_embeddings_url(model_url):
    return urljoin(model_url, "imageEmbeddings/")


@pytest.fixture
def visualai_activationmaps_url(model_url):
    return urljoin(model_url, "imageActivationMaps/")


@pytest.fixture(params=["aim", "eda", "eda2", "empty", "modeling"])
def visualai_project(request, project_with_target_json):
    ret = json.loads(project_with_target_json)
    ret["stage"] = request.param
    return ret


@pytest.fixture
def visualai_image():
    return {"width": 256, "height": 256, "imageId": "5e7e562528513130ab237875"}


@pytest.fixture
def visualai_image_file():
    return bytes((random.randint(0, 255) for i in range(32)))


@pytest.fixture
def visualai_sample(visualai_project):
    if visualai_project["stage"] in ["eda2", "modeling"]:
        return {
            "next": None,
            "data": [
                {
                    "imageId": "5e7e562528513130ab237875",
                    "height": 256,
                    "width": 256,
                    "targetBinRowCount": 1000,
                    "targetBinStart": None,
                    "targetBinEnd": None,
                    "targetValue": "fake",
                },
                {
                    "imageId": "5e7e562528513130ab237874",
                    "height": 256,
                    "width": 256,
                    "targetBinRowCount": 1000,
                    "targetBinStart": None,
                    "targetBinEnd": None,
                    "targetValue": "real",
                },
            ],
            "previous": None,
        }

    else:
        return {
            "next": None,
            "data": [
                {"imageId": "5e7e562528513130ab237875", "height": 256, "width": 256},
                {"imageId": "5e7e562528513130ab237874", "height": 256, "width": 256},
            ],
            "previous": None,
        }


@pytest.fixture
def visualai_duplicate():
    return {
        "count": 0,
        "next": None,
        "data": [
            {"imageId": "5e7e562528513130ab237875", "rowCount": 3},
            {"imageId": "5e7e562528513130ab237874", "rowCount": 7},
        ],
        "previous": None,
    }


@pytest.fixture
def visualai_embeddings():
    return {
        "targetValues": ["fake", "real"],
        "targetBins": None,
        "embeddings": [
            {
                "imageId": "5e7e562b28513130ab23792e",
                "positionX": 0.5935041904449463,
                "positionY": 0.6990952491760254,
                "actualTargetValue": "fake",
            },
            {
                "imageId": "5e7e563528513130ab237a6d",
                "positionX": 0.708981454372406,
                "positionY": 0.6228484511375427,
                "actualTargetValue": "fake",
            },
        ],
    }


@pytest.fixture
def visualai_activationmaps():
    return {
        "activationMapWidth": 56,
        "activationMaps": [
            {
                "imageId": "5eaafb57fcdb565e4d778f29",
                "overlayImageId": "5e7e563528513130ab237a6d",
                "predictedTargetValue": "fake",
                "featureName": "image",
                "actualTargetValue": "fake",
                "imageHeight": 256,
                "imageWidth": 256,
                "activationValues": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
            {
                "imageId": "5eaafb58fcdb565e2f7790d0",
                "predictedTargetValue": "real",
                "featureName": "image",
                "actualTargetValue": "real",
                "imageHeight": 256,
                "imageWidth": 256,
                "activationValues": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ],
        "activationMapHeight": 56,
        "targetBins": None,
        "targetValues": ["fake", "real"],
    }
