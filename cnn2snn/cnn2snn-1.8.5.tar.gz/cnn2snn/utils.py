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
"""
A set of functions to convert a Keras (tf.keras) model to a new
equivalent model with different characteristics. Then, the new model
can be quantized.

"""
import numpy as np
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.models import Model, load_model, model_from_json
from .quantization_ops import (WeightFloat, WeightQuantizer,
                               TrainableWeightQuantizer)
from .quantization_layers import (QuantizedConv2D, QuantizedDepthwiseConv2D,
                                  QuantizedSeparableConv2D, QuantizedDense,
                                  ActivationDiscreteRelu, QuantizedReLU)

cnn2snn_objects = {
    'WeightFloat': WeightFloat,
    'WeightQuantizer': WeightQuantizer,
    'TrainableWeightQuantizer': TrainableWeightQuantizer,
    'QuantizedConv2D': QuantizedConv2D,
    'QuantizedSeparableConv2D': QuantizedSeparableConv2D,
    'QuantizedDense': QuantizedDense,
    'ActivationDiscreteRelu': ActivationDiscreteRelu,
    'QuantizedReLU': QuantizedReLU
}


def merge_separable_conv(model):
    """Returns a new model where all depthwise conv2d layers followed by conv2d
    layers are merged into single separable conv layers.

    The new model is strictly equivalent to the previous one.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model.

    Returns:
        :obj:`tf.keras.Model`: a tf.keras.Model.

    """
    # If no layers are Depthwise, there is nothing to be done, return.
    if not any([isinstance(l, QuantizedDepthwiseConv2D) for l in model.layers]):
        return model

    if isinstance(model.layers[0], InputLayer):
        x = model.layers[0].output
        i = 1
    else:
        x = model.layers[0].input
        i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]

        if isinstance(layer, QuantizedDepthwiseConv2D):
            # Check layers expected order
            if not isinstance(next_layer, QuantizedConv2D):
                raise AttributeError(f"Layer {layer.name} "
                                     "QuantizedDepthwiseConv2D should be "
                                     "followed by QuantizedConv2D layers.")

            if layer.bias is not None:
                raise AttributeError(f"Unsupported bias in "
                                     "QuantizedDepthwiseConv2D Layer "
                                     "{layer.name} ")

            # Get weights and prepare new ones
            dw_weights = layer.get_weights()[0]
            pw_weights = next_layer.get_weights()[0]
            new_weights = [dw_weights, pw_weights]
            if next_layer.use_bias:
                bias = next_layer.get_weights()[1]
                new_weights.append(bias)

            # Create new layer
            new_name = f'{layer.name}_{next_layer.name}'
            new_layer = QuantizedSeparableConv2D(next_layer.filters,
                                                 layer.kernel_size,
                                                 quantizer=layer.quantizer,
                                                 padding=layer.padding,
                                                 use_bias=next_layer.use_bias,
                                                 name=new_name)
            x = new_layer(x)
            new_layer.set_weights(new_weights)
            i = i + 2

        else:
            x = layer(x)
            i = i + 1

    # Add last layer if not done already
    if i == (len(model.layers) - 1):
        if isinstance(model.layers[-1], QuantizedDepthwiseConv2D):
            raise AttributeError(f"Layer {layer.name} "
                                 "QuantizedDepthwiseConv2D should be followed "
                                 "by QuantizedConv2D layers.")
        x = model.layers[-1](x)

    return Model(inputs=model.input, outputs=[x], name=model.name)


def load_quantized_model(filepath, compile=True):
    """Loads a quantized model saved in TF or HDF5 format.

    If the model was compiled and trained before saving, its training state
    will be loaded as well.
    This function is a wrapper of `tf.keras.models.load_model`.

    Args:
        filepath (string): path to the saved model.
        compile (bool): whether to compile the model after loading.

    Returns:
        :obj:`tensorflow.keras.Model`: a Keras model instance.
    """
    return load_model(filepath, cnn2snn_objects, compile)


def load_partial_weights(dest_model, src_model):
    """Loads a subset of weights from one Keras model to another

    This goes through each layers of the source model, looking for a matching
    layer in the destination model.
    If a layer with the same name is found, then this method assumes that one
    of the two layer has the same set of weights as the other plus some extra
    weights at the end, and loads only the first common weights into the
    destination layer.

    Args:
        dest_model(:obj:`tensorflow.keras.Model`): the destination Model
        src_model(:obj:`tensorflow.keras.Model`): the source Model

    """
    for src_layer in src_model.layers:
        src_weights = src_layer.get_weights()
        dest_layer = dest_model.get_layer(src_layer.name)
        dest_weights = dest_layer.get_weights()
        # Take the minimum of the two lists of weights
        n_weights = min(len(src_weights), len(dest_weights))
        # Only replace the first weights
        dest_weights[0:n_weights] = src_weights[0:n_weights]
        dest_layer.set_weights(dest_weights)


def create_trainable_quantizer_model(quantized_model):
    """Converts a legacy quantized model to a model using trainable quantizers.

    Legacy cnn2snn models have fixed quantization schemes. This method converts
    such a model to an equivalent model using trainable quantizers.

    Args:
        quantized_model(str, :obj:`tensorflow.keras.Model`): a keras Model or a
        path to a keras Model file

    Returns:
        :obj:`tensorflow.keras.Model`: a Keras Model instance.
    """
    if isinstance(quantized_model, str):
        # Load the model at the specified path
        quantized_model = load_quantized_model(quantized_model)
    # Dump model configuration in a JSON string
    json_string = quantized_model.to_json()
    # Edit the model configuration to replace static quantizers by trainable
    # ones
    json_string = json_string.replace("WeightQuantizer",
                                      "TrainableWeightQuantizer")
    json_string = json_string.replace("ActivationDiscreteRelu", "QuantizedReLU")
    # Create a new model from the modified configuration
    new_model = model_from_json(json_string, custom_objects=cnn2snn_objects)
    # Transfer weights to the new model
    load_partial_weights(new_model, quantized_model)
    return new_model
