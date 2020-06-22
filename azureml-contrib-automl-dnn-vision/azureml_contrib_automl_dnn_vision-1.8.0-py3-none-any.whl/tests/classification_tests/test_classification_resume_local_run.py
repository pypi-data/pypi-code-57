import os
import tempfile

import pytest
import sys
import time
import pickle
from azureml.contrib.automl.dnn.vision.classification.common.constants import ArtifactsLiterals
import azureml.contrib.automl.dnn.vision.classification.runner as runner


data_folder = 'classification_data/images'
labels_root = 'classification_data/'


def _get_settings(csv_file):
    return {
        # Only run 1 epoch to make the test faster
        'epochs': 1,
        'images_folder': '.',
        'labels_file': csv_file,
        'num_workers': 0,
        'seed': 47,
    }


@pytest.mark.usefixtures('new_clean_dir')
def test_multiclassification_local_run(monkeypatch):

    settings = _get_settings('multiclass.csv')

    with monkeypatch.context() as m:
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
            settings['output_dir'] = tmp_output_dir
            runner.run(settings)
            expected_output = os.path.join(tmp_output_dir, ArtifactsLiterals.MODEL_WRAPPER_PKL)
            assert os.path.exists(expected_output)

            time.sleep(2)
            # support resume
            resume_pkl_file = expected_output
            with open(resume_pkl_file, 'rb') as fp:
                resume_pkl_model = pickle.load(fp)
                optimizer = resume_pkl_model.model_wrapper.optimizer.state_dict()
                assert optimizer is not None
                lr_scheduler = resume_pkl_model.model_wrapper.lr_scheduler.state_dict()
                assert lr_scheduler is not None
                assert len(optimizer['param_groups']) == len(lr_scheduler['base_lrs'])

            # bad path + resume flag should fail
            with pytest.raises(FileNotFoundError):
                settings['resume'] = expected_output + "_random"
                runner.run(settings)

            settings['resume'] = expected_output
            m.setattr(ArtifactsLiterals, 'MODEL_WRAPPER_PKL', ArtifactsLiterals.MODEL_WRAPPER_PKL + "_after_resume")
            expected_output_resume = os.path.join(tmp_output_dir,
                                                  ArtifactsLiterals.MODEL_WRAPPER_PKL)
            runner.run(settings)
            assert os.path.exists(expected_output_resume)
