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
"""Parsing function to generate layers mapping between Keras and Akida.
Two data classes store the mapping: LayerMapping and ModelMapping.

"""
import tensorflow.keras.layers as layers
from . import quantization_layers as qlayers
from akida import LayerType


class LayerMapping:
    """This data class stores the indices of Keras layers that represent a
    single Akida layer. For example, a 'Convolutional' Akida layer corresponds
    to multiple Keras layers:
    - a QuantizedConv2D layer
    - an optional batch normalization layer
    - an optional pooling layer
    - a discrete ReLU activation (optional if last layer)
    """

    def __init__(self, layer_type, index_neural):
        """Creates a layer map of a single Akida layer from Keras layers.

        Args:
            layer_type (:obj:`akida.LayerType`): the type of the Akida layer.
            index_neural (int): the index of the corresponding Keras
                neural layer.

        """
        self.layer_type = layer_type
        self.index_neural = index_neural
        self.index_pool = None
        self.index_batchnorm = None
        self.index_activation = None


class ModelMapping:
    """This data class maps a Keras model to a future Akida model (not built yet).

    When an instance of ModelMapping is created, it will generate a list of
    LayerMapping objects mapping the Keras model with a succession of Akida
    layers.
    A check is then performed to ensure that the Keras model is compatible with
    Akida.

    Note:
        Note that no Akida model is generated at this step: only a mapping is
        created.

    """

    def __init__(self, model_keras, layer_maps):
        self.model_keras = model_keras
        self.layer_maps = layer_maps


def generate_model_mapping(model, input_is_sparse):
    """Generates a model map between Keras and Akida models.

    This function returns a model map from a Keras model. The model map
    corresponds to the Akida layers mapped from the Keras layers.

    Args:
        model (tf.keras model): the model to parse.
        input_is_sparse (bool): if True, input will be an inputData layer,
            otherwise it will be inputConvolutional.

    Returns:
       :obj:`ModelMapping`: a model map corresponding to the input Keras model.

    """
    for layer in model.layers:
        if hasattr(layer, 'data_format'):
            if layer.data_format == "channels_first":
                raise RuntimeError("unsupported data format channels_first")

    layer_maps = []
    index_unsupported_activations = []

    # First we need to map the input layer
    first_layer = 0
    # If first layer is input layer, skip it
    if isinstance(model.layers[0], layers.InputLayer):
        first_layer = 1
    # Get first Akida layer
    if input_is_sparse:
        layer_ak = LayerMapping(LayerType.InputData, first_layer)
    else:
        layer_ak = LayerMapping(LayerType.InputConvolutional, first_layer)
        first_layer += 1

    # Loop on layers
    neural_layers = (qlayers.QuantizedConv2D, qlayers.QuantizedSeparableConv2D,
                     qlayers.QuantizedDense)
    ignore_list = (layers.Dropout)
    activation_list = (layers.Activation, layers.Softmax)
    for i in range(first_layer, len(model.layers)):
        layer = model.layers[i]
        # If this layer is a neural layer, append the current Akida layer and
        # start a new one
        if isinstance(layer, neural_layers):
            layer_maps.append(layer_ak)
            layer_neural = layer

        # Neural layers
        if isinstance(layer, qlayers.QuantizedConv2D):
            layer_ak = LayerMapping(LayerType.Convolutional, i)
        elif isinstance(layer, qlayers.QuantizedSeparableConv2D):
            layer_ak = LayerMapping(LayerType.SeparableConvolutional, i)
        elif isinstance(layer, qlayers.QuantizedDense):
            layer_ak = LayerMapping(LayerType.FullyConnected, i)

        # Pooling + batchnorm + activation layers
        elif isinstance(layer,
                        (layers.MaxPooling2D, layers.GlobalAveragePooling2D)):
            if layer_ak.index_pool:
                raise RuntimeError(f"Two pooling layers were detected in layer"
                                   f" {layer_neural.name}. Only one pooling "
                                   f"layer is supported.")
            layer_ak.index_pool = i
        elif (isinstance(layer, layers.BatchNormalization) or
              layer.__class__.__name__ == "BatchNormalization"):
            if layer_ak.index_batchnorm:
                raise RuntimeError(f"Two BatchNormalization layers were "
                                   f"detected after layer {layer_neural.name}."
                                   f" Only one BatchNormalization layer is "
                                   f"supported.")
            layer_ak.index_batchnorm = i
        elif isinstance(layer, qlayers.BaseQuantizedActivation):
            if layer_ak.index_activation:
                raise RuntimeError(f"Two quantized activation layers were "
                                   f"detected after layer {layer_neural.name}."
                                   f" Only one activation layer is supported.")
            layer_ak.index_activation = i

        # Allow flatten before a dense layer
        elif isinstance(layer, layers.Flatten):
            try:
                if isinstance(model.layers[i + 1], qlayers.QuantizedDense):
                    continue
            except IndexError:
                pass
            raise RuntimeError("Flatten layer only supported before a Dense "
                               "one")
        # Check Reshape compatibility
        elif isinstance(layer, layers.Reshape):
            _check_reshape_layer(layer)
        # Get unsupported activation index to check compatibility later
        elif isinstance(layer, activation_list):
            index_unsupported_activations.append(i)
        # Allow some other layers useful in keras but that will be discarded
        # or ignored during conversion
        elif isinstance(layer, ignore_list):
            continue
        else:
            # If you got here it means the layer is not recognised: raise an error.
            message = ""
            if layer.__class__.__name__ == 'ReLU':
                message = ("\nYou must use a quantized activation layer, like "
                           "ActivationDiscreteRelu, instead of ReLU.")
            raise RuntimeError(f"Layer {layer.name}: unsupported type "
                               f"{layer.__class__.__name__}." + message)

    # Append last parsed layer if any
    layer_maps.append(layer_ak)

    # Check if the unsupported activation is after the last neural layer (i.e.
    # in the last Akida layer
    for i in index_unsupported_activations:
        index_last = layer_maps[-1].index_neural
        if i < index_last:
            raise RuntimeError(
                "Activation layers other than quantized "
                "activations are not supported before the last "
                "neural layer. Receives activation layer "
                f"'{model.layers[i].name}' before the last neural"
                f" layer '{model.layers[index_last].name}'")
        else:
            print(f"Warning: the activation layer '{model.layers[i].name}' "
                  "will be discarded at conversion. The outputs of the Akida "
                  "model will be the potentials before this activation layer.")

    return ModelMapping(model, layer_maps)


def check_mapping_compatibility(model_map):
    """Checks whether the future model will be compatible with Akida.

    This function must mainly test the incompatibities due to the Keras layers
    and the order of the layers (parameters of the quantized layers have
    already been tested at their creation).

    Args:
        :obj:`ModelMapping`: a model map corresponding to the Keras model to
            check
    """
    layers_k = model_map.model_keras.layers

    # Error if hidden layer without activation
    for layer_map in model_map.layer_maps[:-1]:
        if layer_map.layer_type != LayerType.InputData \
                and not layer_map.index_activation:
            raise RuntimeError("No activation layer detected with layer "
                               f"{layers_k[layer_map.index_neural].name}. "
                               "Activation is required in hidden layers.")

    for layer_map in model_map.layer_maps:
        layer_neural = layers_k[layer_map.index_neural]

        if layer_map.index_batchnorm:
            # Raise error if BatchNormalization 'axis' is different from the last
            # dimension. The 'axis' parameter is a list containing the axes on what
            # the batch normalization is applied.
            layer_BN = layers_k[layer_map.index_batchnorm]
            axis = layer_BN.axis
            if (len(layer_BN.axis) != 1 or
                    layer_BN.axis[0] != len(layer_BN.input_shape) - 1):
                raise RuntimeError(f"The BatchNormalization layer "
                                   f"{layer_BN.name} must be applied on the "
                                   f"last axis. Receives {layer_BN.axis}.")
            # Raise error if a gamma is zero.
            gammas = layer_BN.get_weights()[0]
            if (gammas == 0).any():
                raise RuntimeError(
                    f"The BatchNormalization layer {layer_BN.name} has at least"
                    f" one gamma equal to zero. This case is not supported.")
            # Raise error if BatchNormalization has at least one negative gamma
            # and if a MaxPool2D layer is placed before it.
            if (gammas <= 0).any() and layer_map.index_pool:
                layer_pool = layers_k[layer_map.index_pool]
                if (isinstance(layer_pool, layers.MaxPool2D) and
                    (layer_map.index_pool < layer_map.index_batchnorm)):
                    raise RuntimeError(
                        f"The BatchNormalization layer {layer_BN.name} has at "
                        f"least one negative gamma and a MaxPool2D layer is "
                        f"placed before it. This case is not supported.")

        # Raise error if BatchNormalization is placed after the activation
        if (layer_map.index_batchnorm and layer_map.index_activation and
                layer_map.index_batchnorm > layer_map.index_activation):
            raise RuntimeError(f"In the layer {layer_neural.name}, the batch "
                               "normalization layer must be placed before "
                               "the activation.")

        # Raise error if GlobalAvgPool2D is placed after the activation
        if (layer_map.index_pool and layer_map.index_activation and isinstance(
                layers_k[layer_map.index_pool], layers.GlobalAvgPool2D) and
                layer_map.index_pool > layer_map.index_activation):
            raise RuntimeError(f"In the layer {layer_neural.name}, the global "
                               "average pooling layer must be placed before "
                               "the activation.")

        # Raises error if QuantizedDense input shape is incorrect: supported
        # shapes are (N,) and (1, 1, N). Remember input_shape has the batch
        # size as first element of tuple.
        if isinstance(layer_neural, qlayers.QuantizedDense):
            valid = (  # Input shape is (N,)
                len(layer_neural.input_shape) == 2 or
                # Input shape is (1, 1, N)
                (len(layer_neural.input_shape) == 4 and
                 layer_neural.input_shape[1] == 1 and
                 layer_neural.input_shape[2] == 1))
            if not valid:
                raise RuntimeError("The QuantizedDense layer "
                                   f"{layer_neural.name} must have an input "
                                   "shape of (N,). Receives "
                                   f"{layer_neural.input_shape[1:]}.")

        # Raises error if the padding of MaxPool2D is different from the padding
        # of the neural processing layer.
        if layer_map.index_pool:
            layer_pool = layers_k[layer_map.index_pool]
            if (isinstance(layer_pool, layers.MaxPool2D) and
                    layer_neural.padding != layer_pool.padding):
                raise RuntimeError(f"Pooling layer {layer_pool.name} (padding: "
                                   f"{layer_pool.padding}) must have the same "
                                   f"padding as {layer_neural.name} (padding: "
                                   f"{layer_neural.padding}).")


def _check_reshape_layer(layer):
    """This function checks if the reshape layer is supported.

    In the cnn2snn conversion, a Reshape layer can only be used to transform
    a tensor of shape (N,) to a tensor of shape (1, 1, N), and vice-versa.

    Note that the 'input_shape' and 'output_shape' parameters of a layer has
    the batch size as first element:
        input_shape = (batch_size,) + input_tensor_shape
    The batch size is ignored in the following function.
    """
    in_shape = layer.input_shape
    out_shape = layer.output_shape

    valid = ((  # Reshape from (1,1,N) to (N,)
        len(in_shape) == 4 and in_shape[1] == 1 and in_shape[2] == 1 and
        len(out_shape) == 2 and out_shape[1] == in_shape[3]) or
             # Reshape from (N,) to (1,1,N)
             (len(in_shape) == 2 and len(out_shape) == 4 and
              out_shape[1] == 1 and out_shape[2] == 1 and
              out_shape[3] == in_shape[1]) or
             # Useless Reshape, from X to X
             (in_shape == out_shape))

    if not valid:
        raise RuntimeError(f"The Reshape layer {layer.name} can only be used "
                           "to transform a tensor of shape (N,) to a tensor of "
                           "shape (1, 1, N), and vice-versa. Receives "
                           f"input_shape {in_shape[1:]} and output_shape "
                           f"{out_shape[1:]}.")


def check_model_compatibility(model_keras, input_is_sparse):
    """Checks if a Keras quantized model is compatible for cnn2snn conversion.

    This function doesn't convert the Keras quantized model to an Akida model
    but only checks if the model is compatible. The checks are performed at two
    different levels:

        1. Some checks are done when the Keras model is scanned, during the
           generation of the model map.
        2. Other checks are then done based on the model map.

    Note that this function doesn't check if the quantization bitwidths (weights
    or activations) are supported by the Akida Execution Engine or by the Akida
    NSoC.

    **1. How to build a compatible Keras quantized model?**

    The following lines give details and constraints on how to build a Keras
    model compatible for the conversion to an Akida model.


    **2. General information about layers**

    An Akida layer must be seen as a block of Keras layers starting with a
    processing layer (QuantizedConv2D, QuantizedSeparableConv2D,
    QuantizedDense). All blocks of Keras layers except the last block must have
    exactly one quantized activation layer (ActivationDiscreteRelu). Other
    optional layers can be present in a block such as a pooling layer or a
    batch normalization layer.
    Here are all the supported Keras layers for an Akida-compatible model:

    - Processing layers:

      - cnn2snn.QuantizedConv2D
      - cnn2snn.QuantizedSeparableConv2D
      - cnn2snn.QuantizedDense

    - Activation layers:

      - cnn2snn.ActivationDiscreteRelu
      - any increasing activation function (only for the last block of layers)
        such as softmax, sigmoid set as last layer. This layer must derive from
        tf.keras.layers.Activation, and it will be removed during conversion to
        Akida-compatible model.

    - Pooling layers:

      - MaxPool2D
      - GlobalAvgPool2D

    - BatchNormalization
    - Dropout
    - Flatten
    - Input
    - Reshape

    Example of a block of Keras layers::

          -------------------
          | QuantizedConv2D |
          -------------------
                  ||
                  \/
        ----------------------
        | BatchNormalization |
        ----------------------
                  ||
                  \/
             -------------
             | MaxPool2D |
             -------------
                  ||
                  \/
       --------------------------
       | ActivationDiscreteRelu |
       --------------------------


    **3. Constraints about inputs**

    An Akida model can accept two types of inputs: sparse events or 8-bit
    images. Whatever the input type, the Keras inputs must respect the
    following relation:

        input_akida = scale * input_keras + shift

    where the Akida inputs must be positive integers, the input scale must be
    a float value and the input shift must be an integer. In other words,
    scale * input_keras must be integers.

    Depending on the input type:

    - if the inputs are events (sparse), the first layer of the Keras model can
      be any quantized processing layer. The input shift must be zero.
    - if the inputs are images, the first layer must be a QuantizedConv2D
      layer.


    **4. Constraints about layers' parameters**

    To be Akida-compatible, the Keras layers must observe the following rules:

    - all layers with the 'data_format' parameter must be 'channels_last'
    - all processing quantized layers and ActivationDiscreteRelu must have a
      valid quantization bitwidth
    - a QuantizedDense layer must have an input shape of (N,) or (1, 1, N)
    - a BatchNormalization layer must have 'axis' set to -1 (default)
    - a BatchNormalization layer cannot have negative gammas
    - Reshape layers can only be used to transform a tensor of shape (N,) to a
      tensor of shape (1, 1, N), and vice-versa
    - only one pooling layer can be used in each block
    - a MaxPool2D layer must have the same 'padding' as the corresponding
      processing quantized layer

    **5. Constraints about the order of layers**

    To be Akida-compatible, the order of Keras layers must observe the following
    rules:

    - a block of Keras layers must start with a processing quantized layer
    - where present, a BatchNormalization/GlobalAvgPool2D layer must be placed
      before the activation
    - a Flatten layer can only be used before a QuantizedDense layer
    - an Activation layer other than ActivationDiscreteRelu can only be used
      in the last layer


    Args:
        model (tf.keras model): the model to parse.
        input_is_sparse (bool): if True, input will be an inputData layer,
            otherwise it will be inputConvolutional.
    """
    try:
        model_map = generate_model_mapping(model_keras, input_is_sparse)
        check_mapping_compatibility(model_map)
        return True
    except Exception as e:
        print(
            "The Keras quantized model is not compatible for a conversion "
            "to an Akida model:\n", str(e))
        return False
