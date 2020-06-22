import os
import pandas as pd
import pytest
import shutil
import torch.utils.data as data
from azureml.contrib.automl.dnn.vision.object_detection.data.datasets import FileObjectDetectionDatasetWrapper, \
    AmlDatasetObjectDetectionWrapper
from azureml.contrib.automl.dnn.vision.common.utils import _save_image_df
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from .aml_dataset_mock import AmlDatasetMock, WorkspaceMock, DataflowMock, DataflowStreamMock


@pytest.mark.usefixtures('new_clean_dir')
class TestCommonObjectDetectionDatasetWrapper:
    def test_missing_images(self):
        data_root = 'object_detection_data'
        image_root = os.path.join(data_root, 'images')
        annotation_file = os.path.join(data_root, 'missing_image_annotations.json')
        with pytest.raises(AutoMLVisionDataException):
            FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                              image_folder=image_root,
                                              ignore_data_errors=False)

        dataset = FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                                    image_folder=image_root,
                                                    ignore_data_errors=True)

        assert len(dataset) == 1

        # create missing image
        new_path = 'missing_image.jpg'
        shutil.copy(os.path.join(image_root, "000001517.png"), new_path)
        dataset = FileObjectDetectionDatasetWrapper(annotations_file=annotation_file, image_folder=image_root,
                                                    ignore_data_errors=True)
        os.remove(new_path)

        total_size = 0
        for images, targets, info in data.DataLoader(dataset, batch_size=100, num_workers=0):
            total_size += images.shape[0]

        assert total_size == 1

    def test_bad_annotations(self):
        data_root = 'object_detection_data'
        annotation_file = os.path.join(data_root, 'annotation_bad_line.json')
        image_folder = os.path.join(data_root, 'images')
        with pytest.raises(AutoMLVisionDataException):
            FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                              image_folder=image_folder,
                                              ignore_data_errors=False)

        dataset = FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                                    image_folder=image_folder,
                                                    ignore_data_errors=True)

        assert len(dataset) == 1


@pytest.mark.usefixtures('new_clean_dir')
class TestAmlDatasetObjectDetectionWrapper:

    def test_aml_dataset_object_detection_default(self):
        test_dataset_id = 'a7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'a7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'a7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = [{'label': 'cat', 'topX': 0.1, 'topY': 0.9, 'bottomX': 0.2, 'bottomY': 0.8},
                       {'label': 'dog', 'topX': 0.5, 'topY': 0.5, 'bottomX': 0.6, 'bottomY': 0.4}]
        test_label1 = [{'label': 'fish', 'topX': 0.3, 'topY': 0.4, 'bottomX': 0.5, 'bottomY': 0.2}]
        test_labels = [test_label0, test_label1]
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': test_labels
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        try:
            datasetwrapper = AmlDatasetObjectDetectionWrapper(test_dataset_id,
                                                              workspace=mockworkspace,
                                                              datasetclass=AmlDatasetMock)

            for a, t in zip(datasetwrapper._annotations.values(), test_labels):
                for a_label, t_label in zip(a, t):
                    assert a_label._label == t_label['label'], "Test _label"
                    assert a_label._x0_percentage == t_label['topX'], "Test _x0_percentage"
                    assert a_label._y0_percentage == t_label['topY'], "Test _y0_percentage"
                    assert a_label._x1_percentage == t_label['bottomX'], "Test label name"
                    assert a_label._y1_percentage == t_label['bottomY'], "Test label name"

            assert os.path.exists(test_file0)
            assert os.path.exists(test_file1)

        finally:
            os.remove(test_file0)
            os.remove(test_file1)

    def test_aml_dataset_object_detection_train_test_split(self):
        test_dataset_id = 'a7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'a7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'a7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = [{'label': 'cat', 'topX': 0.1, 'topY': 0.9, 'bottomX': 0.2, 'bottomY': 0.8},
                       {'label': 'dog', 'topX': 0.5, 'topY': 0.5, 'bottomX': 0.6, 'bottomY': 0.4}]
        test_label1 = [{'label': 'fish', 'topX': 0.3, 'topY': 0.4, 'bottomX': 0.5, 'bottomY': 0.2}]
        test_labels = [test_label0, test_label1]
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': test_labels
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        try:
            datasetwrapper = AmlDatasetObjectDetectionWrapper(test_dataset_id, is_train=True,
                                                              workspace=mockworkspace,
                                                              datasetclass=AmlDatasetMock)
            train_dataset_wrapper, valid_dataset_wrapper = datasetwrapper.train_val_split()
            _save_image_df(train_df=datasetwrapper.get_images_df(),
                           train_index=train_dataset_wrapper._indices,
                           val_index=valid_dataset_wrapper._indices, output_dir='.')

            assert train_dataset_wrapper._is_train
            assert not valid_dataset_wrapper._is_train
            assert train_dataset_wrapper.classes == valid_dataset_wrapper.classes

            num_train_images = len(train_dataset_wrapper._indices)
            num_valid_images = len(valid_dataset_wrapper._indices)
            assert len(datasetwrapper._image_urls) == num_train_images + num_valid_images

            assert os.path.exists(test_file0)
            assert os.path.exists(test_file1)
            # it's train_df.csv and val_df.csv files created from _save_image_df function
            assert os.path.exists('train_df.csv')
            assert os.path.exists('val_df.csv')

        finally:
            os.remove(test_file0)
            os.remove(test_file1)
            os.remove('train_df.csv')
            os.remove('val_df.csv')
