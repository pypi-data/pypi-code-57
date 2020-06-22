import pytest

from azureml.contrib.automl.dnn.vision.classification.models.classification_model_wrappers import ModelFactory, \
    Resnet18Wrapper, Mobilenetv2Wrapper, SeresnextWrapper
from azureml.contrib.automl.dnn.vision.classification.common.constants import ModelNames, \
    base_training_settings_defaults
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.automl.core.shared.exceptions import ClientException


@pytest.mark.usefixtures('new_clean_dir')
class TestModelWrappers:
    def _load_batch_of_pil(self, test_data_image_list):
        raise NotImplementedError

    def test_wrappers(self):
        # right now only initialization and making sure that the model is working
        Resnet18Wrapper(20)
        Mobilenetv2Wrapper(20)
        SeresnextWrapper(20)

        assert True

    def test_wrappers_export_onnx(self):
        # right now only initialization and making sure that the model is working
        device = base_training_settings_defaults[SettingsLiterals.DEVICE]
        res18 = Resnet18Wrapper(20)
        res18.export_onnx_model(device=device)
        mv2 = Mobilenetv2Wrapper(20)
        mv2.export_onnx_model(device=device)
        sn = SeresnextWrapper(20)
        sn.export_onnx_model(device=device)

        assert True

    def test_model_factory(self):
        ModelFactory.get_model_wrapper(ModelNames.RESNET18, 5)
        ModelFactory.get_model_wrapper(ModelNames.MOBILENETV2, 5)
        ModelFactory.get_model_wrapper(ModelNames.SERESNEXT, 5)

        assert True

    def test_model_factory_nonpresent_model(self):
        with pytest.raises(ClientException):
            ModelFactory.get_model_wrapper('nonexistent_model')

    @pytest.mark.skip(reason="not implemented")
    def test_model_predict(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="not implemented")
    def test_model_predict_proba(self):
        raise NotImplementedError
