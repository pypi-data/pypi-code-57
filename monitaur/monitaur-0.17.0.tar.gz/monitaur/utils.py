import base64
import pickle
from pathlib import Path, PurePath

import boto3
import dill
import joblib
import numpy as np

from monitaur.virgil.alibi.tabular import AnchorTabular

from monitaur.exceptions import (  # noqa isort:skip
    ClientValidationError,
    CustomInfluencesError,
    FileError,
)


def get_influences(model_set_id, version, features, aws_credentials):
    """
    Downloads trained model and respective influences from s3.
    Then calculates influences based on the features

    Args:
        model_set_id: A UUID string for the monitaur model set.
        version: Monitaur model version.
        features: key/value pairs of the feature names and values.
        aws_credentials: dict of aws credentials

    Returns:
        dict of influences
    """

    influence_threshold = 0.95

    client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_key"],
        region_name=aws_credentials["aws_region"],
    )

    anchors_filename = f"{model_set_id}.anchors"
    s3_object = f"{model_set_id}/{version}/{anchors_filename}"

    with open(anchors_filename, "wb") as f:
        client.download_fileobj(aws_credentials["aws_bucket_name"], s3_object, f)

    with open(anchors_filename, "rb") as f:
        explainer = dill.load(f)
        # determine influences for transaction
        inputs = list(features.values())
        reshaped_inputs = np.asarray(inputs).reshape(1, len(inputs))
        influences = explainer.explain(reshaped_inputs, threshold=influence_threshold)

    if Path(anchors_filename).exists():
        Path(anchors_filename).unlink()

    return influences["names"]


def valid_model(extension, model_class):
    """
    Validates a trained model based on the model_class.

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        model_class: 'tabular' or 'image'.

    Returns:
        True if valid
    """

    if model_class == "tabular" and extension not in [".joblib", ".pickle"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.pickle'.")
    if model_class == "image" and extension not in [".joblib", ".tar", ".h5"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.tar', '.h5'.")

    return True


def generate_anchors(
    extension, trained_model, feature_names, training_data, model_set_id
) -> str:
    """
    Generate anchor file

    Args:
        extension: File extension for the serialized model (.joblib, .pickle).
        trained_model: Instantiated model (.joblib, .pickle).
        feature_names: Model inputs.
        training_data: Training data (x training).
        model_set_id: A UUID string for the monitaur model set received from the API.

    Returns:
        anchor file path (.anchors)
    """

    if extension == ".joblib":
        trained_model_file = joblib.load(trained_model)
    else:
        trained_model_file = pickle.load(trained_model)

    predict_fn = lambda x: trained_model_file.predict_proba(x)  # NOQA
    explainer = AnchorTabular(predict_fn, feature_names)
    explainer.fit(training_data)

    filename_anchors = f"{model_set_id}.anchors"

    with open(filename_anchors, "wb") as f:
        dill.dump(explainer, f)

    return filename_anchors


def add_image(image):
    image_path = Path(image)

    if not image_path.exists():
        raise ClientValidationError("Image File path not valid")

    # Check the file extension
    extension = image_path.suffix
    if extension not in (".png", ".jpg", ".jpeg"):
        raise ClientValidationError("Invalid Image provided")

    file_size = float(image_path.stat().st_size) / (1024.0 ** 2)
    if file_size > 1:
        raise ClientValidationError(
            "Image Size greater than One (1) Megabyte. Choose a file with a lesser size"
        )

    with open(image, "rb") as img:
        image_byte = (base64.b64encode(img.read())).decode("utf-8")

    return image_byte


def validate_influences(model_influences, model_class, custom_influences):
    if model_influences == "custom-dict":
        if not isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is custom-dict, custom_influences must be a dict"
            )
    if model_influences == "custom-image":
        if not isinstance(custom_influences, PurePath):
            raise CustomInfluencesError(
                "When model.influences is custom-image, custom_influences must be a file path"
            )
    if model_influences == "anchors":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is anchors, custom_influences must be None"
            )
    if model_influences == "grad-cam":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is grad-cam, custom_influences must be None"
            )
    if not model_influences:
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is None, custom_influences must be None"
            )

    return True


def upload_file_to_s3(
    model_set_id, version, filepath, aws_credentials, filename=None
) -> bool:
    """
    Uploads file to s3

    Args:
        model_set_id: A UUID string for the monitaur model set received from the API.
        version: Monitaur model version.
        filepath: Instantiated model file path
        aws_credentials: dict of aws credentials
        filename: optional name for the s3 object

    Returns:
        bool
    """

    client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_key"],
        region_name=aws_credentials["aws_region"],
    )

    if filename:
        s3_filename = filename
    else:
        s3_filename = filepath

    with open(filepath, "rb") as f:
        client.upload_fileobj(
            f,
            aws_credentials["aws_bucket_name"],
            f"{model_set_id}/{version}/{s3_filename}",
        )

    if Path(filepath).exists():
        Path(filepath).unlink()

    return True
