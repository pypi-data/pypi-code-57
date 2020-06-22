from pathlib import Path

import boto3
import joblib
import pytest

from monitaur.exceptions import CustomInfluencesError, FileError
from monitaur.virgil.alibi.tabular import AnchorTabular

from monitaur.utils import (  # isort:skip
    generate_anchors,
    upload_file_to_s3,
    valid_model,
    validate_influences,
)


def test_valid_model():
    assert valid_model(".pickle", "tabular")
    assert valid_model(".h5", "image")

    with pytest.raises(FileError) as excinfo:
        valid_model(".h5", "tabular")
    assert (
        "Invalid model. Acceptable files: '.joblib', '.pickle'."
        == excinfo.value.message
    )

    with pytest.raises(FileError) as excinfo:
        valid_model("", "image")
    assert (
        "Invalid model. Acceptable files: '.joblib', '.tar', '.h5'."
        == excinfo.value.message
    )


def test_generate_anchors(mocker, training_data):
    mocker.patch.object(
        joblib, "load", return_value=b"Image-Base-64-encoded-return-data"
    )
    mocker.patch.object(AnchorTabular, "__init__", return_value=None)
    mocker.patch.object(AnchorTabular, "fit")

    assert generate_anchors(
        ".joblib",
        "job.joblib",
        [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeF",
            "Age",
        ],
        training_data,
        1,
    )


def test_upload_file_to_s3(mocker, training_data):
    boto_mock = mocker.patch.object(boto3, "client")
    mocker.patch("builtins.open")

    assert upload_file_to_s3(
        1,
        0.1,
        "job.joblib",
        {
            "aws_access_key": "not real",
            "aws_secret_key": "not real",
            "aws_region": "not real",
            "aws_bucket_name": "not real",
        },
    )

    assert boto_mock.call_count == 1


@pytest.mark.parametrize(
    "model_influences, model_class, custom_influences",
    [
        ("custom-dict", "tabular", {}),
        ("custom-image", "tabular", Path("foo.jpeg")),
        ("anchors", "tabular", None),
        ("grad-cam", "tabular", None),
        (None, "tabular", None),
        ("custom-dict", "image", {}),
        ("custom-image", "image", Path("foo.jpeg")),
        ("anchors", "image", None),
        ("grad-cam", "image", None),
        (None, "image", None),
        ("custom-dict", "nlp", {}),
        ("custom-image", "nlp", Path("foo.jpeg")),
        ("anchors", "nlp", None),
        ("grad-cam", "nlp", None),
        (None, "nlp", None),
    ],
)
def test_validate_influences_valid(model_influences, model_class, custom_influences):
    assert validate_influences(model_influences, model_class, custom_influences)


@pytest.mark.parametrize(
    "model_influences, model_class, custom_influences, value",
    [
        ("custom-dict", "tabular", "foo.png", "a dict"),
        ("custom-image", "tabular", {}, "a file path"),
        ("anchors", "tabular", {}, "None"),
        ("grad-cam", "tabular", {}, "None"),
        (None, "tabular", {}, "None"),
        ("custom-dict", "image", "foo.png", "a dict"),
        ("custom-image", "image", {}, "a file path"),
        ("anchors", "image", {}, "None"),
        ("grad-cam", "image", {}, "None"),
        (None, "image", {}, "None"),
        ("custom-dict", "nlp", "foo.png", "a dict"),
        ("custom-image", "nlp", {}, "a file path"),
        ("anchors", "nlp", {}, "None"),
        ("grad-cam", "nlp", {}, "None"),
        (None, "nlp", {}, "None"),
    ],
)
def test_validate_influences_invalid(
    model_influences, model_class, custom_influences, value
):
    with pytest.raises(CustomInfluencesError) as excinfo:
        validate_influences(model_influences, model_class, custom_influences)
    assert (
        f"When model.influences is {model_influences}, custom_influences must be {value}"
        == excinfo.value.message
    )
