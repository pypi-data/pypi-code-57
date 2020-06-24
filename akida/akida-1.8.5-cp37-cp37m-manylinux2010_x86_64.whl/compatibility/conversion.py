import akida
import numpy as np
import copy
from . import common


def _get_weights_params_identity(layer):
    """
    Creates an 'identity' convolutional layer parameters and its weights.
    """
    out_dims = layer.output_dims
    nb_chan = out_dims[2]
    dw_weights = np.zeros((3, 3, nb_chan, 1), dtype=np.int8)
    pw_weights = np.zeros((1, 1, nb_chan, nb_chan), dtype=np.int8)
    for i in range(nb_chan):
        dw_weights[1, 1, i, 0] = 1
        pw_weights[0, 0, i, i] = 1

    # create a layer to have default parameters
    identity_layer = akida.SeparableConvolutional(
        name=f"{layer.name}_pooling",
        kernel_width=3,
        kernel_height=3,
        num_neurons=nb_chan,
        threshold_fire=0,
        threshold_fire_bits=layer.parameters.activations_params.
        threshold_fire_bits,
        threshold_fire_step=1)
    return copy.copy(identity_layer.parameters), dw_weights, pw_weights


def _copy_layer_variables(layer, copied_layer):
    for var in copied_layer.get_variable_names():
        layer.set_variable(var, copied_layer.get_variable(var))


def _copy_layer(model, layer):
    new_layer = akida.Layer(layer.parameters, layer.name)
    model.add(new_layer)
    _copy_layer_variables(new_layer, layer)


def _add_identity_cnp_after_max_pooling(model, layer):
    """
    Adds the layer and an identity CNP to the model
    """
    ident_params, ident_dw_weights, ident_pw_weights = _get_weights_params_identity(
        layer)
    identity_layer = akida.Layer(ident_params, f"{layer.name}_identity")
    model.add(identity_layer)
    identity_layer.set_variable("weights", ident_dw_weights)
    identity_layer.set_variable("weights_pw", ident_pw_weights)


def _cnp_max_pooling(layer):
    return layer.parameters.layer_type in [
        akida.LayerType.Convolutional, akida.LayerType.SeparableConvolutional
    ] and layer.parameters.pooling_type == akida.PoolingType.Max


def _cnp_pooling_needs_identity_cnp(model, layer_index):
    """
    Returns True if the layer is CNP with max pooling not followed by another
    CNP, and we can add an identity CNP layer after it without altering result
    """
    result = False
    layer = model.get_layer(layer_index)
    if _cnp_max_pooling(layer):
        # if it is not the last layer, check the layer is not followed by another cnp
        if layer_index != model.get_layer_count() - 1:
            next_layer = model.get_layer(layer_index + 1)
            if next_layer.parameters.layer_type not in [
                    akida.LayerType.Convolutional,
                    akida.LayerType.SeparableConvolutional
            ]:
                result = True
        # if it is the last layer, we can add an identity layer only if it has activations enabled
        elif layer.parameters.activations_params.activations_enabled:
            result = True
    return result


def _cnp_max_pooling_split(model, layer):
    """
    Splits a CNP with max pooling into 2 CNPs:
        - one performing the convolution
        - the other one performing the pooling
    """
    # 1st layer is the conv without pooling
    conv_params = copy.copy(layer.parameters)
    conv_params.pooling_type = akida.PoolingType.NoPooling
    conv_params.pooling_width = -1
    conv_params.pooling_height = -1
    conv_params.pooling_stride_x = -1
    conv_params.pooling_stride_y = -1
    layer_conv = akida.Layer(conv_params, f"{layer.name}_conv")
    model.add(layer_conv)
    _copy_layer_variables(layer_conv, layer)
    # 2nd layer is an identity conv with pooling
    pool_params, pool_dw_weights, pool_pw_weights = _get_weights_params_identity(
        layer)
    pool_params.pooling_type = akida.PoolingType.Max
    pool_params.pooling_width = layer.parameters.pooling_width
    pool_params.pooling_height = layer.parameters.pooling_height
    pool_params.pooling_stride_x = layer.parameters.pooling_stride_x
    pool_params.pooling_stride_y = layer.parameters.pooling_stride_y
    pool_layer = akida.Layer(pool_params, f"{layer.name}_pooling")
    model.add(pool_layer)
    pool_layer.set_variable("weights", pool_dw_weights)
    pool_layer.set_variable("weights_pw", pool_pw_weights)


def create_from_model(model, version=None):
    """Tries to create a HW compatible model from an incompatible one

    Tries to create a HW compatible model from an incompatible one, using SW
    workarounds for known limitations. It returns a converted model that is not
    guaranteed to be HW compatible, depending if workaround have been found.

    Args:
        model (:obj:`Model`): a Model object to convert

    Returns:
        :obj:`Model`: a new Model with no guarantee that it is HW compatible.
    """
    new_model = akida.Model(backend=model.backend.type)
    nb_layers = model.get_layer_count()
    for i in range(nb_layers):
        layer = model.get_layer(i)
        if _cnp_max_pooling(layer):
            # On nsoc-v1, if CNP has max pooling, it must be split into 2 CNPs:
            # - one performing the convolution
            # - the other one performing the pooling
            if common.is_v1(version) and not common.cnp_is_identity(layer):
                _cnp_max_pooling_split(new_model, layer)
            else:
                _copy_layer(new_model, layer)
            # If CNP has max pooling and is not followed by another CNP, we can add
            # an identity CNP layer
            if _cnp_pooling_needs_identity_cnp(model, i):
                _add_identity_cnp_after_max_pooling(new_model, layer)
            continue

        # if no particular case is found, copy the layer into the new model
        _copy_layer(new_model, layer)

    return new_model
