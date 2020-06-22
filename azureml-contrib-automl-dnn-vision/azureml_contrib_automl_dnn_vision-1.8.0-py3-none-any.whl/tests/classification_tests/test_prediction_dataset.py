import pytest
from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from .aml_dataset_mock import AmlDatasetMock, WorkspaceMock, DataflowMock, DataflowStreamMock
import os
import pandas as pd


@pytest.mark.usefixtures('new_clean_dir')
class TestPredictionDataset:

    def test_prediction_dataset(self):
        test_dataset_id = 'e7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'e7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'e7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        properties = {}
        label_dataset_data = {
            'Path': ['/' + f for f in test_files]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'Path')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        datasetwrapper = PredictionDataset(input_dataset_id=test_dataset_id, ws=mockworkspace,
                                           datasetclass=AmlDatasetMock)

        file_names = datasetwrapper._files
        file_names.sort()
        assert file_names == [test_file0, test_file1], "File Names"
        assert len(datasetwrapper) == 2, "len"

        assert os.path.exists(test_file0)
        assert os.path.exists(test_file1)

        os.remove(test_file0)
        os.remove(test_file1)
