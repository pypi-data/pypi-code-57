# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Convenience functions to create model wrappers."""

from .object_detection_model_wrappers import ObjectDetectionModelFactory


def setup_model(model_name=None, number_of_classes=None, **kwargs):
    """Returns model wrapper from name and number of classes.

    :param model_name: Name of model to get
    :type model_name: String
    :param number_of_classes: Number of classes
    :type number_of_classes: Int
    :param kwargs: Optional keyword arguments to define model specifications
    :type kwargs: dict
    :return: Model wrapper containing model
    :rtype: Object derived from BaseObjectDetectionModelWrapper (See object_detection.model.base_model_wrapper)
    """

    model_factory = ObjectDetectionModelFactory()

    return model_factory._get_model_wrapper(model_name=model_name, number_of_classes=number_of_classes,
                                            **kwargs)
