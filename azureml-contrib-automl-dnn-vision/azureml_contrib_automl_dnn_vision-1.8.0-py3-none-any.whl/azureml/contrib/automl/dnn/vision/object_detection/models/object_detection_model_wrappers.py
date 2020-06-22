# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper functions to build model wrappers."""

from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from .customrcnn import CustomRCNNWrapper, CustomRCNNSpecifications
from ..common.constants import ModelNames, RCNNBackbones
from ...common.pretrained_model_utilities import PretrainedModelFactory


DEFAULT_MODEL = ModelNames.FASTER_RCNN_RESNET50_FPN


class FasterRCNNResnet50FPNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for Faster RCNN with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes=None, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        model = self._create_model(number_of_classes, **kwargs)

        super().__init__(model=model, number_of_classes=number_of_classes)

    def _create_model(self, number_of_classes, specs=None, **kwargs):

        model = PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True, **kwargs)

        if number_of_classes is not None:
            input_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features,
                                                              number_of_classes)

        return model


class FasterRCNNResnet18FPNWrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with Resnet 18 FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.RESNET_18_FPN_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class FasterRCNNMobilenetV2Wrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with MobileNet v2 w/o FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.MOBILENET_V2_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class ObjectDetectionModelFactory:
    """Factory function to create models."""

    _models_dict = {
        ModelNames.FASTER_RCNN_RESNET50_FPN: FasterRCNNResnet50FPNWrapper,
        ModelNames.FASTER_RCNN_RESNET18_FPN: FasterRCNNResnet18FPNWrapper,
        ModelNames.FASTER_RCNN_MOBILENETV2: FasterRCNNMobilenetV2Wrapper
    }

    @staticmethod
    def _get_model_wrapper(number_of_classes=None, model_name=None, **kwargs):

        if model_name is None:
            model_name = DEFAULT_MODEL

        if model_name not in ObjectDetectionModelFactory._models_dict:
            raise ValueError('Unsupported model')

        return ObjectDetectionModelFactory._models_dict[model_name](number_of_classes=number_of_classes, **kwargs)
