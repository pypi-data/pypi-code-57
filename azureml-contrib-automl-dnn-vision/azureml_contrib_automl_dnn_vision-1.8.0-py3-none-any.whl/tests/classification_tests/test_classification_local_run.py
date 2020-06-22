import os
import tempfile

import pytest
import sys
from azureml.contrib.automl.dnn.vision.classification.common.constants import ArtifactsLiterals
import azureml.contrib.automl.dnn.vision.classification.runner as runner


data_folder = 'classification_data/images'
labels_root = 'classification_data/'


def _get_settings(csv_file):
    return {
        'images_folder': '.',
        'labels_file': csv_file,
        'seed': 47,
        'num_workers': 0,
    }


@pytest.mark.usefixtures('new_clean_dir')
def test_binary_classification_local_run(monkeypatch):
    _test_classifaction_local_run(monkeypatch, 'binary_classification.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multiclassification_local_run(monkeypatch):
    _test_classifaction_local_run(monkeypatch, 'multiclass.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multilabel_local_run(monkeypatch):
    _test_classifaction_local_run(monkeypatch, 'multilabel.csv')


def _test_classifaction_local_run(monkeypatch, csv_file):
    settings = _get_settings(csv_file)

    with monkeypatch.context() as m:
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
            settings['output_dir'] = tmp_output_dir
            runner.run(settings, multilabel=True)
            expected_output = os.path.join(tmp_output_dir, ArtifactsLiterals.MODEL_WRAPPER_PKL)
            assert os.path.exists(expected_output)
