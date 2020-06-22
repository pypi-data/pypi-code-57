# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Concrete classes for model wrappers."""
from azureml.automl.core.shared.exceptions import ClientException

try:
    from torch import nn
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')

from .base_model_wrapper import BaseModelWrapper
from ..common.constants import ModelNames
from ...common.pretrained_model_utilities import PretrainedModelFactory


class Resnet18Wrapper(BaseModelWrapper):
    """Model wrapper for Resnet18."""

    def __init__(self, num_classes, multilabel=False):
        """
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel or not
        :type multilabel: bool
        """
        model = PretrainedModelFactory.resnet18(pretrained=True)
        num_feats = model.fc.in_features
        model.fc = nn.Linear(num_feats, num_classes)
        # store featurizer
        featurizer = nn.Sequential(*list(model.children())[:-1])
        super().__init__(model=model, multilabel=multilabel, name=ModelNames.RESNET18, featurizer=featurizer)


class Resnet50Wrapper(BaseModelWrapper):
    """Model wrapper for Resnet50."""

    def __init__(self, num_classes, multilabel=False):
        """
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel or not
        :type multilabel: bool
        """
        model = PretrainedModelFactory.resnet50(pretrained=True)
        num_feats = model.fc.in_features
        model.fc = nn.Linear(num_feats, num_classes)
        # store featurizer
        featurizer = nn.Sequential(*list(model.children())[:-1])
        super().__init__(model=model, multilabel=multilabel, name=ModelNames.RESNET50, featurizer=featurizer)


class Mobilenetv2Wrapper(BaseModelWrapper):
    """Model wrapper for mobilenetv2."""

    def __init__(self, num_classes, multilabel=False):
        """
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel or not
        :type multilabel: bool
        """
        model = PretrainedModelFactory.mobilenet_v2(pretrained=True)
        num_feats = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_feats, num_classes)
        # store featurizer
        featurizer = nn.Sequential(*list(model.children())[:-1])
        super().__init__(model=model, multilabel=multilabel, name=ModelNames.MOBILENETV2, featurizer=featurizer)


class SeresnextWrapper(BaseModelWrapper):
    """Model wrapper for seresnext."""

    def __init__(self, num_classes, multilabel=False):
        """
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel or not
        :type multilabel: bool
        """
        model = PretrainedModelFactory.se_resnext50_32x4d(num_classes=1000, pretrained='imagenet')
        num_feats = model.last_linear.in_features
        model.last_linear = nn.Linear(num_feats, num_classes)
        # store featurizer
        featurizer = nn.Sequential(*list(model.children())[:-1])
        super().__init__(model=model, multilabel=multilabel, name=ModelNames.SERESNEXT, featurizer=featurizer)


class ModelFactory:
    """Model factory class for obtaining model wrappers."""
    _models_dict = {
        ModelNames.RESNET18: Resnet18Wrapper,
        ModelNames.RESNET50: Resnet50Wrapper,
        ModelNames.MOBILENETV2: Mobilenetv2Wrapper,
        ModelNames.SERESNEXT: SeresnextWrapper
    }

    @staticmethod
    def get_model_wrapper(model_name, num_classes=None, multilabel=False):
        """
        :param model_name: string name of the model
        :type model_name: str
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel or not
        :type multilabel: bool
        :return: model wrapper
        :rtype: azureml.contrib.automl.dnn.vision.classification.base_model_wrappers.BaseModelWrapper
        """
        if model_name not in ModelFactory._models_dict:
            raise ClientException('Unsupported model name', has_pii=False)
        if num_classes is None:
            raise ClientException('num_classes cannot be None', has_pii=False)

        return ModelFactory._models_dict[model_name](num_classes=num_classes, multilabel=multilabel)
