import akida.core as ak


def serialize_learning_type(learning_type):
    if learning_type == ak.LearningType.NoLearning:
        return "none"
    if learning_type == ak.LearningType.AkidaUnsupervised:
        return "akidaUnsupervised"


def deserialize_parameters(params):
    type = str()
    params_dict = {}
    for item in params:
        if item == "layerType":
            type = str(params[item])
        elif item == "inputWidth":
            params_dict["input_width"] = params[item]
        elif item == "inputHeight":
            params_dict["input_height"] = params[item]
        elif item == "convolutionMode":
            if params[item] == "valid":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Valid
            elif params[item] == "same":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Same
            elif params[item] == "full":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Full
            else:
                raise ValueError("'convolutionMode' should be 'valid', "
                                 "'same' or 'full'")
        elif item == "kernelWidth":
            params_dict["kernel_width"] = params[item]
        elif item == "kernelHeight":
            params_dict["kernel_height"] = params[item]
        elif item == "kernelSize":
            params_dict["kernel_width"] = params[item]
            params_dict["kernel_height"] = params[item]
        elif item == "strideX":
            params_dict["stride_x"] = params[item]
        elif item == "strideY":
            params_dict["stride_y"] = params[item]
        elif item == "stride":
            params_dict["stride_x"] = params[item]
            params_dict["stride_y"] = params[item]
        elif item == "poolingWidth":
            params_dict["pooling_width"] = params[item]
        elif item == "poolingHeight":
            params_dict["pooling_height"] = params[item]
        elif item == "poolingSize":
            params_dict["pooling_width"] = params[item]
            params_dict["pooling_height"] = params[item]
        elif item == "poolingType":
            if params[item] == "none":
                params_dict["pooling_type"] = ak.PoolingType.NoPooling
            elif params[item] == "max":
                params_dict["pooling_type"] = ak.PoolingType.Max
            elif params[item] == "average":
                params_dict["pooling_type"] = ak.PoolingType.Average
            else:
                raise ValueError("'poolingType' should be 'none', 'max' "
                                 "or 'average'")
        elif item == "poolStrideX":
            params_dict["pooling_stride_x"] = params[item]
        elif item == "poolStrideY":
            params_dict["pooling_stride_y"] = params[item]
        elif item == "numNeurons":
            params_dict["num_neurons"] = params[item]
        elif item == "weightsBits":
            params_dict["weights_bits"] = params[item]
        elif item == "learningType":
            if params[item] == "none":
                params_dict["learning_type"] = ak.LearningType.NoLearning
            elif params[item] == "akidaUnsupervised":
                params_dict["learning_type"] = ak.LearningType.AkidaUnsupervised
            else:
                raise ValueError(
                    "'learningType' should be 'none' or 'akidaUnsupervised'")
        elif item == "numWeights":
            params_dict["num_weights"] = params[item]
        elif item == "numClasses":
            params_dict["num_classes"] = params[item]
        elif item == "initialPlasticity":
            params_dict["initial_plasticity"] = params[item]
        elif item == "learningCompetition":
            params_dict["learning_competition"] = params[item]
        elif item == "minPlasticity":
            params_dict["min_plasticity"] = params[item]
        elif item == "plasticityDecay":
            params_dict["plasticity_decay"] = params[item]
        elif item == "activations":
            if params[item] == "none":
                params_dict["activations_enabled"] = False
            elif params[item] == "true":
                pass  # activations are enabled by default
            else:
                raise ValueError("'activations' should be 'none' or 'true'")
        elif item == "thresholdFire":
            params_dict["threshold_fire"] = params[item]
        elif item == "thresholdFireStep":
            params_dict["threshold_fire_step"] = params[item]
        elif item == "thresholdFireBits":
            params_dict["threshold_fire_bits"] = params[item]
        elif item == "inputFeatures":
            params_dict["input_channels"] = params[item]
        elif item == "paddingValue":
            params_dict["padding_value"] = params[item]
        elif item == "inputChannels":
            params_dict["input_channels"] = params[item]
        else:
            raise ValueError("Unknown parameter: " + item + ": " +
                             str(params[item]))
    return type, params_dict
