# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines literals and constants for the classification part of the package."""

try:
    import torch
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')
from ...common.constants import SettingsLiterals


class ArtifactsLiterals:
    """Filenames for artifacts."""
    MODEL_WRAPPER_PKL = 'model_wrapper.pkl'
    ONNX_MODEL_FILE_NAME = 'model.onnx'
    LABEL_FILE_NAME = 'labels.json'
    CONDA_YML = 'conda_dependencies.yml'
    SCORE_SCRIPT = 'score_script.py'
    FEATURIZE_SCRIPT = 'featurize_script.py'
    OUTPUT_DIRECTORY = 'train_artifacts'


class MetricsLiterals:
    """String key names for metrics."""
    ACCURACY = 'accuracy'
    PRECISION = 'precision'
    RECALL = 'recall'
    AVERAGE_PRECISION = 'average_precision'
    ACCURACY_TOP5 = 'accuracy_top5'
    SKLEARN_METRICS = 'sklearn_metrics'
    IOU = 'iou'
    AVERAGE_SAMPLE_F1_SCORE = 'average_sample_f1_score'
    AVERAGE_SAMPLE_F2_SCORE = 'average_sample_f2_score'
    AVERAGE_CLASS_PRECISION = 'average_class_precision'
    AVERAGE_CLASS_RECALL = 'average_class_recall'
    AVERAGE_CLASS_F1_SCORE = 'average_class_f1_score'
    AVERAGE_CLASS_F2_SCORE = 'average_class_f2_score'


class PredictionLiterals:
    """Strings that will be keys in the output json during prediction."""
    FEATURE_VECTOR = 'feature_vector'
    FILENAME = 'filename'
    LABELS = 'labels'
    PROBS = 'probs'
    PREDICTION_FILE_NAME = 'predictions.txt'
    FEATURE_FILE_NAME = 'features.txt'


class TrainingLiterals:
    """String keys for training parameters."""
    BATCH_SIZE = 'batch_size'
    # Report detailed metrics like per class/sample f1, f2, precision, recall scores.
    DETAILED_METRICS = 'detailed_metrics'
    DIFF_LR = 'diff_lr'
    EARLY_STOPPING_PATIENCE = 'early_stopping_patience'
    FIT_LAST = 'fit_last'
    # data imbalance ratio (#data from largest class /#data from smallest class)
    IMBALANCE_RATE_THRESHOLD = "imbalance_rate_threshold"
    LAST_LAYER_LR = 'last_layer_lr'
    LR = 'lr'
    MODEL_NAME = 'model_name'
    MOMENTUM = 'momentum'
    NUM_EPOCHS = 'epochs'
    # allow oversampling from small classes when imbalance_rate above IMBALANCE_RATE_THRESHOLD
    OVERSAMPLE = 'oversample'
    PARAMS = 'params'
    PRIMARY_METRIC = 'primary_metric'
    STEP_LR_GAMMA = 'step_lr_gamma'
    STEP_LR_STEP_SIZE = 'step_lr_step_size'
    STRATEGY = 'strategy'
    TEST_RATIO = 'test_ratio'
    WEIGHT_DECAY = 'weight_decay'
    # applying rescaling class-level weights for CrossEntropyLoss()
    WEIGHTED_LOSS = 'weighted_loss'


class LoggingLiterals:
    """Literals that help logging and correlating different training runs."""
    PROJECT_ID = 'project_id'
    VERSION_NUMBER = 'version_number'
    TASK_TYPE = 'task_type'


class ModelNames:
    """Currently supported model names."""
    RESNET18 = 'resnet18'
    RESNET50 = 'resnet50'
    MOBILENETV2 = 'mobilenetv2'
    SERESNEXT = 'seresnext'


class PackageInfo:
    """Contains package details."""
    PYTHON_VERSION = '3.6'
    CONDA_PACKAGE_NAMES = ['pip']
    PIP_PACKAGE_NAMES = ['azureml-contrib-automl-dnn-vision']


base_training_settings_defaults = {
    TrainingLiterals.MODEL_NAME: ModelNames.SERESNEXT,
    TrainingLiterals.STRATEGY: TrainingLiterals.DIFF_LR,
    SettingsLiterals.LABELS_FILE_ROOT: '',
    SettingsLiterals.DATA_FOLDER: '',
    TrainingLiterals.BATCH_SIZE: 80,
    SettingsLiterals.DEVICE: torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
    TrainingLiterals.EARLY_STOPPING_PATIENCE: 5,
    SettingsLiterals.IGNORE_DATA_ERRORS: True,
    TrainingLiterals.IMBALANCE_RATE_THRESHOLD: 2,
    SettingsLiterals.MULTILABEL: False,
    TrainingLiterals.NUM_EPOCHS: 15,
    SettingsLiterals.OUTPUT_DIR: ArtifactsLiterals.OUTPUT_DIRECTORY,
    TrainingLiterals.OVERSAMPLE: True,
    TrainingLiterals.TEST_RATIO: 0.2,
    TrainingLiterals.WEIGHTED_LOSS: False,
    TrainingLiterals.DETAILED_METRICS: True,
    TrainingLiterals.WEIGHT_DECAY: 1e-4,
    TrainingLiterals.MOMENTUM: 0.9,
    SettingsLiterals.NUM_WORKERS: 8
}

multiclass_training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: MetricsLiterals.ACCURACY,
    TrainingLiterals.LR: 0.001,
    TrainingLiterals.LAST_LAYER_LR: 0.01,
    TrainingLiterals.STEP_LR_STEP_SIZE: 5,
    TrainingLiterals.STEP_LR_GAMMA: 0.5
}

multilabel_training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: MetricsLiterals.IOU,
    TrainingLiterals.LR: 0.07,
    TrainingLiterals.LAST_LAYER_LR: 0.45,
    TrainingLiterals.STEP_LR_STEP_SIZE: 5,
    TrainingLiterals.STEP_LR_GAMMA: 0.35
}

scoring_settings_defaults = {
    SettingsLiterals.NUM_WORKERS: 8
}

featurization_settings_defaults = {
    SettingsLiterals.NUM_WORKERS: 8
}
