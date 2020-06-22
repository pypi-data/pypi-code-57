import pytest


class TrainedModel:
    def predict_proba(self, x):
        pass


class XTrain:
    pass


@pytest.fixture
def trained_model():
    """ Serialized trained model """
    return "job.joblib"


@pytest.fixture
def training_data():
    """ Data set that the model trained with """
    return XTrain()
