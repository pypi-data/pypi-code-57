import pytest
import uuid
from azureml.contrib.automl.dnn.vision.classification.io.read.dataset_wrappers import ImageFolderDatasetWrapper,\
    ImageFolderLabelFileDatasetWrapper, OverSamplingDatasetWrapper, AmlDatasetWrapper
from azureml.contrib.automl.dnn.vision.common.utils import _save_image_df
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from .aml_dataset_mock import AmlDatasetMock, WorkspaceMock, DataflowMock, DataflowStreamMock
import os
import pandas as pd


@pytest.mark.usefixtures('new_clean_dir')
class TestImageFolderDatasetWrapper:
    def test_generate_labels_files_from_imagefolder(self):
        dataset_wrapper = ImageFolderDatasetWrapper(
            'classification_data/image_folder_format')
        assert len(dataset_wrapper) == 4
        # check whether all images are in
        labels = []
        for _, label in dataset_wrapper:
            labels.append(label)

        assert len(set(labels)) == 2
        assert dataset_wrapper.num_classes == 2


@pytest.mark.usefixtures('new_clean_dir')
class TestImageFolderLabelFileDatasetWrapper:
    def test_get_labels(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )
        assert len(dataset_wrapper) == 4
        labels = []
        for _, label in dataset_wrapper:
            labels.extend(label)

        assert len(set(labels)) == 2

    def test_valid_dataset(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )

        valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/valid_labels.csv',
            all_labels=dataset_wrapper.labels,
            multilabel=True
        )

        assert valid_dataset_wrapper.labels == dataset_wrapper.labels

    def test_labels_with_tabs(self):
        labels_file = str(uuid.uuid4())[:7] + '.txt'
        with open(labels_file, 'w') as fp:
            fp.write('crack_1.jpg\t"label_1\t"')

        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file=labels_file
        )

        assert dataset_wrapper.labels == ['label_1\t']

    def test_labels_with_commas(self):
        labels_file = str(uuid.uuid4())[:7] + '.txt'
        with open(labels_file, 'w') as fp:
            fp.write('"crack_1.jpg"\t\'label_1,label_2\', label_3')

        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file=labels_file,
            multilabel=True
        )

        assert set(dataset_wrapper.labels) == set(['label_1,label_2', 'label_3'])

    def test_missing_labels_in_validation(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )

        valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/invalid_labels.txt',
            all_labels=dataset_wrapper.labels,
            multilabel=True
        )

        assert set(dataset_wrapper.labels).issubset(set(valid_dataset_wrapper.labels))

        dataset_wrapper.reset_labels(valid_dataset_wrapper.labels)

        assert dataset_wrapper.labels == valid_dataset_wrapper.labels

    def test_oversampling_dataset_wrappers(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=False
        )

        oversampling_wrapper = OverSamplingDatasetWrapper(dataset_wrapper)

        assert len(oversampling_wrapper) == 6

        label_sizes = {'label1': 0, 'label2': 0}
        for i in range(len(oversampling_wrapper)):
            label_sizes[oversampling_wrapper.label_at_index(i)] += 1

        assert label_sizes['label1'] == 3
        assert label_sizes['label2'] == 3

    def test_bad_line_in_input_file(self):
        with pytest.raises(AutoMLVisionDataException):
            ImageFolderLabelFileDatasetWrapper(
                'classification_data/images',
                input_file='classification_data/multiclass_bad_line.csv',
                ignore_data_errors=False
            )

        dataset = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_bad_line.csv',
            ignore_data_errors=True
        )

        assert len(dataset) == 3

    def test_missing_images_in_input_file(self):
        with pytest.raises(AutoMLVisionDataException):
            ImageFolderLabelFileDatasetWrapper(
                'classification_data/images',
                input_file='classification_data/multiclass_missing_image.csv',
                ignore_data_errors=False
            )

        dataset = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_missing_image.csv',
            ignore_data_errors=True
        )

        assert len(dataset) == 3


@pytest.mark.usefixtures('new_clean_dir')
class TestAmlDatasetDatasetWrapper:

    def test_aml_dataset_wrapper_default(self):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'd7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'd7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = 'cat'
        test_label1 = 'dog'
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': [test_label0, test_label1]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        datasetwrapper = AmlDatasetWrapper(test_dataset_id, workspace=mockworkspace, datasetclass=AmlDatasetMock)

        assert datasetwrapper.label_at_index(0) == test_label0, "Test label 0"
        assert datasetwrapper.label_at_index(1) == test_label1, "Test label 1"

        labels = datasetwrapper.labels
        labels.sort()
        assert labels == [test_label0, test_label1], "Labels"
        assert not datasetwrapper.multilabel, "Multilabel"
        assert len(datasetwrapper) == 2, "len"

        assert os.path.exists(test_file0)
        assert os.path.exists(test_file1)

        os.remove(test_file0)
        os.remove(test_file1)

    def test_aml_dataset_wrapper_properties(self):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701914'
        test_file0 = 'd7c014ec-474a-49f4-8ae3-09049c701914-1.txt'
        test_file1 = 'd7c014ec-474a-49f4-8ae3-09049c701914-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = 'cat'
        test_label1 = 'dog'
        properties = {'_Image_Column:Image_': {'Column': 'f',
                      'DetailsColumn': 'image_details'},
                      '_Label_Column:Label_': {'Column': 'x', 'Type': 'Classification'}}
        label_dataset_data = {
            'f': test_files,
            'x': [test_label0, test_label1]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'f')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        datasetwrapper = AmlDatasetWrapper(test_dataset_id, workspace=mockworkspace, datasetclass=AmlDatasetMock)

        assert datasetwrapper.label_at_index(0) == test_label0, "Test label 0"
        assert datasetwrapper.label_at_index(1) == test_label1, "Test label 1"

        labels = datasetwrapper.labels
        labels.sort()
        assert labels == [test_label0, test_label1], "Labels"
        assert not datasetwrapper.multilabel, "Multilabel"
        assert len(datasetwrapper) == 2, "len"

        assert os.path.exists(test_file0)
        assert os.path.exists(test_file1)

        os.remove(test_file0)
        os.remove(test_file1)

    def test_aml_dataset_wrapper_multilabel(self):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701915'
        test_file0 = 'd7c014ec-474a-49f4-8ae3-09049c701915-1.txt'
        test_file1 = 'd7c014ec-474a-49f4-8ae3-09049c701915-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = ['cat', 'white']
        test_label1 = ['dog', 'black']
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': [test_label0, test_label1]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        datasetwrapper = AmlDatasetWrapper(test_dataset_id, multilabel=True, workspace=mockworkspace,
                                           datasetclass=AmlDatasetMock)

        assert datasetwrapper.label_at_index(0) == test_label0, "Test label 0"
        assert datasetwrapper.label_at_index(1) == test_label1, "Test label 1"

        labels = datasetwrapper.labels
        labels.sort()
        assert labels == ['black', 'cat', 'dog', 'white'], "Labels"
        assert datasetwrapper.multilabel, "Multilabel"
        assert len(datasetwrapper) == 2, "len"

        assert os.path.exists(test_file0)
        assert os.path.exists(test_file1)

        os.remove(test_file0)
        os.remove(test_file1)

    def test_aml_dataset_wrapper_ignore_missing(self):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701916'
        test_file0 = 'd7c014ec-474a-49f4-8ae3-09049c701916-1.txt'
        test_file1 = 'd7c014ec-474a-49f4-8ae3-09049c701916-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = 'cat'
        test_label1 = 'dog'
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': [test_label0, test_label1]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock([test_file1])
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        datasetwrapper = AmlDatasetWrapper(test_dataset_id, workspace=mockworkspace,
                                           ignore_data_errors=True,
                                           datasetclass=AmlDatasetMock)

        assert datasetwrapper.label_at_index(0) == test_label1, "Test label 0"

        assert datasetwrapper.labels == [test_label1], "Labels"
        assert not datasetwrapper.multilabel, "Multilabel"
        assert len(datasetwrapper) == 1, "len"

        assert os.path.exists(test_file1)

        os.remove(test_file1)

    def test_aml_dataset_wrapper_train_test_split(self):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'd7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'd7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        test_label0 = 'cat'
        test_label1 = 'dog'
        properties = {}
        label_dataset_data = {
            'image_url': test_files,
            'label': [test_label0, test_label1]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'image_url')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        try:
            datasetwrapper = AmlDatasetWrapper(test_dataset_id, workspace=mockworkspace, datasetclass=AmlDatasetMock)
            train_dataset_wrapper, valid_dataset_wrapper = datasetwrapper.train_val_split()
            _save_image_df(train_df=train_dataset_wrapper._images_df, val_df=valid_dataset_wrapper._images_df,
                           output_dir='.')

            if train_dataset_wrapper.labels != valid_dataset_wrapper.labels:
                all_labels = list(set(train_dataset_wrapper.labels + valid_dataset_wrapper.labels))
                train_dataset_wrapper.reset_labels(all_labels)
                valid_dataset_wrapper.reset_labels(all_labels)

            num_train_files = len(train_dataset_wrapper._CommonImageDatasetWrapper__files)
            num_valid_files = len(valid_dataset_wrapper._CommonImageDatasetWrapper__files)
            assert len(datasetwrapper._CommonImageDatasetWrapper__files) == num_train_files + num_valid_files
            assert sorted(datasetwrapper.labels) == sorted(all_labels)

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
