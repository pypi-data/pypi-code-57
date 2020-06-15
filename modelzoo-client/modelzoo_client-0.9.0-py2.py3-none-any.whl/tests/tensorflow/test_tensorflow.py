import pathlib
import tensorflow as tf

import modelzoo
from modelzoo import tensorflow

from tests.mock_api_server import mock_api_server


def create_tf_model():
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(512, activation="relu", input_shape=(784,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model


def test_tensorflow_deploy() -> None:
    model = create_tf_model()
    img_path = pathlib.Path(__file__).parent.parent.joinpath("fixtures/cybertruck.jpg")

    with mock_api_server():
        assert tensorflow.deploy(model, model_name="test", api_key="test") == "test"

        modelzoo.list(api_key="test")
        modelzoo.info("test-model", api_key="test")
        modelzoo.stop("test-model", api_key="test")
        modelzoo.start("test-model", api_key="test")
        modelzoo.predict("test-model", {"inputs": 1.0}, api_key="test")

        tensorflow.predict("test", [0], api_key="test")
        tensorflow.predict_image("test", str(img_path), api_key="test")
