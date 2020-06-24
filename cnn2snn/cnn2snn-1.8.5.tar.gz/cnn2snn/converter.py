#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

import os
from tensorflow import executing_eagerly
from . import utils
from .mapping_generator import generate_model_mapping, check_mapping_compatibility
from .model_generator import generate_model
from .weights_ops import set_weights_thresholds
from akida import Model


def convert(model,
            file_path=None,
            input_scaling=(1.0, 0),
            input_is_sparse=False):
    """Simple function to convert a Keras model to an Akida one.

    These steps are performed:

    1) Merge the depthwise+conv layers into a separable_conv one.
    2) Generate an Akida model based on that model.
    3) Convert weights from the Keras model to Akida.

    Note:
        The relationship between Keras and Akida inputs is:
        input_akida = alpha * input_keras + beta, optional

    Args:
        model (:obj:`tf.keras.Model`): a tf.keras model
        file_path (str, optional): destination for the akida model.
            (Default value = None)
        input_scaling (2 elements tuple, optional): value of the input scaling.
            (Default value = (1.0,0))
        input_is_sparse (bool, optional): if True, input will be an InputData layer,
            otherwise it will be InputConvolutional. (Default value = False)

    Returns:
        an Akida model.

    """

    if not executing_eagerly():
        raise SystemError("Tensorflow eager execution is disabled. "
                          "It is required to convert Keras weights to Akida.")

    if not input_scaling[0] > 0:
        raise ValueError("The scale factor 'input_scaling[0]' must be strictly"
                         f" positive. Receives: input_scaling={input_scaling}")

    # Merge separable convolution
    model_sep = utils.merge_separable_conv(model)

    # Generate model mapping
    model_map = generate_model_mapping(model_sep, input_is_sparse)

    # Check compatibility of the model map
    check_mapping_compatibility(model_map)

    # Generate Akida model
    ak_inst = generate_model(model_map, input_scaling)

    # Convert weights
    set_weights_thresholds(model_map, ak_inst, input_scaling)

    # Save model if file_path is given
    if file_path:
        # Create directories
        dir_name, base_name = os.path.split(file_path)
        if base_name:
            file_root, file_ext = os.path.splitext(base_name)
            if not file_ext:
                file_ext = '.fbz'
        else:
            file_root = model.name
            file_ext = '.fbz'

        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        save_path = os.path.join(dir_name, file_root + file_ext)
        ak_inst.save(save_path)

    return ak_inst
