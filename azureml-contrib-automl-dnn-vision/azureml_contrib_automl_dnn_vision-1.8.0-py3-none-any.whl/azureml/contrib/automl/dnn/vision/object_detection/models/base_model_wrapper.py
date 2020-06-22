# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper classes that define object detection model behavior."""

from abc import ABC, abstractmethod
import torch
import torchvision
import copy
import logging
import time
from torchvision import transforms
from torchvision.ops._register_onnx_ops import _onnx_opset_version
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from ..common.boundingbox import BoundingBox
from ..common.constants import OutputFields, ArtifactLiterals, FasterRCNNParameters

logger = logging.getLogger(__name__)


class PredictBoundingBoxMixin:
    """Helper mixin to BaseObjectDetectionModelWrapper that adds prediction methods"""

    def predict(self, images):
        """Predicts bounding boxes from images.

        :param inputs: Batch of images
        :type inputs: List[PIL.Image]
        :return: Lists of BoundingBox objects scores
        :rtype: List[azureml.contrib.automl.dnn.vision.object_detection.common.boundingbox.BoundingBox]
        """
        if self.transforms is not None:
            inputs = self.transforms(images)
        else:
            inputs = self._get_tensor(images)

        # move tensors to the same device as model
        inputs = inputs.to(self.device)

        # change training state of model
        orig_state_train = False
        if self.model.training:
            self.model.eval()
            orig_state_train = True

        outputs = self.model(inputs)

        if orig_state_train:
            self.model.train()

        return self._get_lists_of_bounding_boxes(outputs)

    def _get_lists_of_bounding_boxes(self, model_outputs=None):
        """
        :param model_outputs: model output from running the object detection model
        :type model_outputs: List of Dict of lists of boxes, classes and scores
        :return:
        """
        results = []
        for per_image_result in model_outputs:
            boxes = per_image_result[OutputFields.BOXES_LABEL]
            labels = per_image_result[OutputFields.CLASSES_LABEL]
            scores = per_image_result[OutputFields.SCORES_LABEL]

            labels = [self.classes[index] for index in labels]

            results.append(self._get_list_of_bounding_boxes_for_image(boxes, labels, scores))

        return results

    def _get_list_of_bounding_boxes_for_image(self, boxes=None, labels=None, scores=None):
        """
        :param boxes: FloatTensor sized n x 4 where each box is [top_left_x1, top_left_y1, bottom_right_x2,
        bottom_right_y2]
        :type boxes: torch.FloatTensor
        :param labels: Int64Tensor of size n containing predicted labels for each box
        :type labels: torch.Int64Tensor
        :param scores: float tensor of size n containing scores for each prediction
        :type scores: torch.FloatTensor
        :return: list of BoundingBoxes
        :rtype: List[BoundingBox]
        """
        boxes = []
        for box, label, score in zip(boxes, labels, scores):
            boxes.append(BoundingBox(label, box, score))

        return boxes

    def _get_tensor(self, images=None):
        """
        :param images: list of PIL Image objects
        :type images: list[PIL.Image]
        :return: tensor for image batch
        :rtype: torch.Tensor
        """
        return torch.stack([transforms.ToTensor()(im) for im in images], dim=0)


class BaseObjectDetectionModelWrapper(ABC, PredictBoundingBoxMixin):
    """Abstract base class that defines behavior of object detection models."""

    def __init__(self, model=None, number_of_classes=None, specs=None, **kwargs):
        """
        :param model: Model to wrap
        :type model: Pytorch nn.Module
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param specs: Model specifications
        :type specs: Class containing specifications
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        self._transforms = None
        self._model = model
        self._specs = specs
        self._number_of_classes = number_of_classes
        self._classes = None
        self._device = None

    @abstractmethod
    def _create_model(self, number_of_classes, specs, **kwargs):
        """Abstract method defining how to create a model from
        number of classes required and model specific specifications.

        :param number_of_classes: Number of classes
        :type number_of_classes: Int
        :param specs: Model specifications
        :type specs: Class containing specifications
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        pass

    def restore_model(self, model_dict=None, **kwargs):
        """Restores a saved model state.

        :param model_dict (optional): Saved pytorch dict with model weights
        :type model_dict: Pytorch state dict
        """
        self._model = self._create_model(self._number_of_classes, self._specs, **kwargs)

        if model_dict is not None:
            self._model.load_state_dict(model_dict)

    def export_onnx_model_not_in_use(self, file_path=ArtifactLiterals.ONNX_MODEL_FILE_NAME, device=None):
        """
        Export the pytorch model to onnx model file.

        :param file_path: file path to save the exported onnx model.
        :type file_path: str
        :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
        :type device: str
        """
        # TODO: it's NOT working w/ torchvision==0.5.0 -- https://github.com/pytorch/vision/issues/1706
        # p0: device='cuda' is NOT working -- RuntimeError from detection/rpn.py
        # p1: dummy_input on device='cpu' and self._model.to('cpu') is NOT working --
        # RuntimeError: expected device cpu but got device cuda:0 from detection/rpn.py
        # p2: only a batch size of 1 with fixed image size is supported.
        # p3: if image (or, dummy_input) after forward passing when exporting onnx doesn't have output prediction,
        # it always gives empty array for onnx inference
        # p4: if no prediction from onnx inference, it throws onnxruntime error of invalid output shape
        onnx_export_start = time.time()
        dummy_input = torch.randn(1, 3, 200, 300, device=device, requires_grad=False)
        self._model.eval()
        torch.onnx.export(self._model,
                          dummy_input,
                          file_path,
                          do_constant_folding=True,
                          opset_version=_onnx_opset_version,
                          input_names=['input'], output_names=['boxes', 'labels', 'scores'],
                          dynamic_axes={'input': {0: 'batch', 2: 'height', 3: 'width'},
                                        'boxes': {0: 'prediction'},
                                        'labels': {0: 'prediction'},
                                        'scores': {0: 'prediction'}})
        onnx_export_time = time.time() - onnx_export_start
        logger.info('ONNX ({}) export time {:.4f}'.format(file_path, onnx_export_time))

    def export_onnx_model(self, file_path=ArtifactLiterals.ONNX_MODEL_FILE_NAME, device=None):
        """
        Export the pytorch model to onnx model file.

        :param file_path: file path to save the exported onnx model.
        :type file_path: str
        :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
        :type device: str
        """
        # TODO: this is a workaround (only works for the default network of fasterrcnn_resnet50_fpn on cpu)
        onnx_export_start = time.time()
        model_weights = copy.deepcopy(self._model.state_dict())
        num_classes = self._number_of_classes

        min_size = FasterRCNNParameters.DEFAULT_MIN_SIZE
        # model is in 'cpu' by default
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False,
                                                                     pretrained_backbone=False,
                                                                     min_size=min_size,
                                                                     box_score_thresh=0.0)  # to have output prediction
        input_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(input_features, num_classes)
        model.load_state_dict(model_weights)

        dummy_input = torch.randn(1, 3, 600, 800, requires_grad=False)
        model.eval()
        torch.onnx.export(model,
                          dummy_input,
                          file_path,
                          do_constant_folding=True,
                          opset_version=_onnx_opset_version,
                          input_names=['input'], output_names=['boxes', 'labels', 'scores'],
                          dynamic_axes={'input': {0: 'batch'},
                                        'boxes': {0: 'prediction'},
                                        'labels': {0: 'prediction'},
                                        'scores': {0: 'prediction'}})
        onnx_export_time = time.time() - onnx_export_start
        logger.info('ONNX ({}) export time {:.4f}'.format(file_path, onnx_export_time))

    @property
    def device(self):
        """Get device for pytorch model

        :return: device
        :rtype: str
        """
        return self._device

    @device.setter
    def device(self, value):
        """Set device for pytorch model

        :param value: device
        :type value: str
        """
        self._device = value

    @property
    def model(self):
        """Get pytorch model from wrapper

        :return: Model
        :rtype: Pytorch nn.Module
        """
        return self._model

    @model.setter
    def model(self, value):
        """Set pytorch model in wrapper

        :param value: Model to set
        :type value: Pytorch nn.Module
        """
        self._model = value

    @property
    def transforms(self):
        """Get image transforms

        :return: Image transforms
        :rtype: Function
        """
        return self._transforms

    @transforms.setter
    def transforms(self, value):
        """Set image transforms

        :param value: Transforms to apply to image
        :type value: Function
        """
        self._transforms = value

    @property
    def parameters(self):
        """Get model parameters

        :return: Model parameters
        :rtype: Pytorch state dictionary
        """
        return self._model.parameters

    @property
    def classes(self):
        """Get the classes in a list that corresponds to class index

        :return: List of class names. If none is set, will simply return ['0', '1', '2',....]
        :rtype: List of strings
        """
        if self._classes is not None:
            return self._classes
        else:
            numeric_map = [str(i) for i in range(self._number_of_classes)]
            return numeric_map

    @classes.setter
    def classes(self, classes):
        """Set the image classes

        :param classes: Names of the different classes found in image
        :type classes: List of strings
        """
        self._classes = classes

    def to_device(self, device):
        """Send to device.

        :param device: device to which the model should be moved to
        :type device: str
        """
        self.model.to(device)
        self._device = device
