# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines literals and constants for the object detection part of the package."""
import torch

from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals


class ArtifactLiterals:
    """Filenames for artifacts."""
    MODEL_FILE_NAME = "model.pth"
    ONNX_MODEL_FILE_NAME = "model.onnx"
    LABEL_FILE_NAME = "labels.json"
    PICKLE_FILE_NAME = "model_wrapper.pkl"
    OUTPUT_DIR = "train_artifacts"
    SCORE_SCRIPT = "score_script.py"


class CriterionNames:
    """String names for different loss functions."""
    FASTER_RCNN = "FASTER_RCNN"


class DataLoaderParameters:
    """Default parameters for dataloaders."""
    DEFAULT_BATCH_SIZE = 4
    DEFAULT_SHUFFLE = True


class DatasetFieldLabels:
    """Keys for input datasets."""
    X_0_PERCENT = "topX"
    Y_0_PERCENT = "topY"
    X_1_PERCENT = "bottomX"
    Y_1_PERCENT = "bottomY"
    IS_CROWD = "isCrowd"
    IMAGE_URL = "imageUrl"
    IMAGE_DETAILS = "imageDetails"
    IMAGE_LABEL = "label"
    CLASS_LABEL = "label"
    WIDTH = "width"
    HEIGHT = "height"


class LearningParameters:
    """Default learning parameters."""
    SGD_DEFAULT_LEARNING_RATE = 0.005
    SGD_DEFAULT_MOMENTUM = 0.9
    SGD_DEFAULT_WEIGHT_DECAY = 0.0001


class LRSchedulerNames:
    """String names for scheduler parameters."""
    DEFAULT_LR_SCHEDULER = "STEP"
    STEP = "STEP"


class ModelNames:
    """String names for model backbones."""
    FASTER_RCNN_RESNET50_FPN = "fasterrcnn_resnet50_fpn"
    FASTER_RCNN_RESNET18_FPN = "fasterrcnn_resnet18_fpn"
    FASTER_RCNN_MOBILENETV2 = "fasterrcnn_mobilenet_v2"


class OutputFields:
    """Keys for the outputs of the object detection network."""
    BOXES_LABEL = "boxes"
    CLASSES_LABEL = "labels"
    SCORES_LABEL = "scores"


class OptimizerNames:
    """String names and defaults for optimizers."""
    DEFAULT_OPTIMIZER = "SGD"
    SGD = "SGD"


class RCNNBackbones:
    """String keys for the different faster rcnn backbones."""
    RESNET_50_FPN_BACKBONE = "resnet50fpn"
    RESNET_18_FPN_BACKBONE = "resnet18fpn"
    RESNET_152_FPN_BACKBONE = "resnet152fpn"
    MOBILENET_V2_BACKBONE = "mobilenet_v2"


class RCNNSpecifications:
    """String keys for different faster rcnn speficiations"""
    BACKBONE = "backbone"
    DEFAULT_BACKBONE = RCNNBackbones.RESNET_50_FPN_BACKBONE
    RESNET_FPN_BACKBONES = [RCNNBackbones.RESNET_18_FPN_BACKBONE,
                            RCNNBackbones.RESNET_50_FPN_BACKBONE,
                            RCNNBackbones.RESNET_152_FPN_BACKBONE]
    CNN_BACKBONES = [RCNNBackbones.MOBILENET_V2_BACKBONE]


class SchedulerParameters:
    """Default learning rate scheduler parameters."""
    DEFAULT_STEP_LR_STEP_SIZE = 3
    DEFAULT_STEP_LR_GAMMA = 0.5


class TrainingParameters:
    """Default training parameters."""
    DEFAULT_NUMBER_EPOCHS = 15
    DEFAULT_TRAINING_BATCH_SIZE = 2
    DEFAULT_VALIDATION_BATCH_SIZE = 1
    DEFAULT_PATIENCE_ITERATIONS = 3
    DEFAULT_PRIMARY_METRIC = "mean_average_precision"


class TrainingLiterals:
    """String keys for training parameters."""
    PRIMARY_METRIC = "primary_metric"
    MODEL_NAME = "model_name"
    NUMBER_OF_EPOCHS = "number_of_epochs"
    MAX_PATIENCE_ITERATIONS = "max_patience_iterations"
    ENABLE_COCO_VALIDATION = "enable_coco_validation"
    LEARNING_RATE = "learning_rate"
    MOMENTUM = "momentum"
    WEIGHT_DECAY = "weight_decay"
    STEP_SIZE = "step_size"
    GAMMA = "gamma"
    TRAINING_BATCH_SIZE = "training_batch_size"
    VALIDATION_BATCH_SIZE = "validation_batch_size"


training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: TrainingParameters.DEFAULT_PRIMARY_METRIC,
    SettingsLiterals.DEVICE: "cuda:0" if torch.cuda.is_available() else "cpu",
    SettingsLiterals.IGNORE_DATA_ERRORS: True,
    TrainingLiterals.MODEL_NAME: ModelNames.FASTER_RCNN_RESNET50_FPN,
    SettingsLiterals.NUM_WORKERS: 2
}


class ScoringParameters:
    """Default scoring parameters."""
    DEFAULT_SCORING_BATCH_SIZE = 2
    DEFAULT_NUM_WORKERS = 4


class FasterRCNNLiterals:
    """String keys for FasterRCNN parameters."""
    MIN_SIZE = "min_size"
    BOX_SCORE_THRESH = "box_score_thresh"
    BOX_NMS_THRESH = "box_nms_thresh"
    BOX_DETECTIONS_PER_IMG = "box_detections_per_img"


class FasterRCNNParameters:
    """Default FasterRCNN parameters."""
    DEFAULT_MIN_SIZE = 600
    DEFAULT_BOX_SCORE_THRESH = 0.3
    DEFAULT_BOX_NMS_THRESH = 0.5
    DEFAULT_BOX_DETECTIONS_PER_IMG = 100


class PredefinedLiterals:
    """Predefined string literals"""
    BG_LABEL = "--bg--"
