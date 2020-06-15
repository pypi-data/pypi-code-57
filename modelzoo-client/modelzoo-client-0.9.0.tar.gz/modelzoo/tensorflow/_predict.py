#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Any, Dict

import numpy as np
import tensorflow as tf

from modelzoo import predict as base_predict


def predict(model_name: str, payload: Any, *args, **kwargs) -> Dict[str, Any]:
    """
    Send a prediction to a TensorFlow model. Wraps the interface described in
    https://www.tensorflow.org/tfx/serving/api_rest#predict_api, using a
    columnar format.

    Args:
        model_name: String name of the model.
        payload:
            The value that will be specified as "inputs" in columnar format to
            https://www.tensorflow.org/tfx/serving/api_rest#predict_api
        api_key: Will override the environment api key, if present.

    Returns:
        The output prediction
    """

    # Common case: the payload is an numpy.ndarray, which is not JSON
    # serializable by default. Convert it to a list for serialization.
    if isinstance(payload, np.ndarray):
        payload = payload.tolist()

    return base_predict(model_name, {"inputs": payload}, *args, **kwargs).get("outputs")


def predict_image(
    model_name: str, filename: str, target_size=(224, 224), *args, **kwargs
) -> Dict[str, Any]:
    """
    Send a prediction to a TensorFlow model that expects images as input. This
    function does not do any image preprocessing -- for more control
    manipulating the input data, use :py:func:`modelzoo.predict` or
    :py:func:`modelzoo.tensorflow.predict`.

    Args:
        model_name: String name of the model.
        filename:
            The path to an image that exists on the filesystem.
        target_size:
            The size to convert the image into before sending it prediction.
            Default is (224, 224).
        api_key: Will override the environment api key, if present.

    Returns:
        The output prediction
    """
    img = tf.keras.preprocessing.image.load_img(filename, target_size=target_size)
    # TODO: Infer the dtype from the model metadata. For now, assume images
    # are converted to uint8 for TF models.
    array = tf.keras.preprocessing.image.img_to_array(img, dtype=np.uint8)
    array = np.expand_dims(array, axis=0)
    return predict(model_name, array.tolist(), *args, **kwargs)
