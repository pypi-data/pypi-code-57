# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Dataset for prediction."""

import os
from torch.utils.data import Dataset
from azureml.contrib.automl.dnn.vision.common.utils import _read_image
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.core import Dataset as AmlDataset


class PredictionDataset(Dataset):
    """Dataset file so that score.py can process images in batches.

    """
    def __init__(self, root_dir=None, image_list_file=None, transforms=None, ignore_data_errors=True,
                 input_dataset_id=None, ws=None, datasetclass=AmlDataset):
        """
        :param root_dir: prefix to be added to the paths contained in image_list_file
        :type root_dir: str
        :param image_list_file: path to file containing list of images
        :type image_list_file: str
        :param transforms: function that takes in a pillow image and can generate tensor
        :type transforms: function
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
        :type input_dataset_id: str
        :param ws: The Azure ML Workspace
        :type ws: Workspace
        :param datasetclass: The Azure ML Datset class
        :type datasetclass: Dataset

        """
        self._files = []

        if input_dataset_id is not None:
            dataset_helper = AmlLabeledDatasetHelper(input_dataset_id, ws, ignore_data_errors,
                                                     image_column_name=AmlLabeledDatasetHelper.PATH_COLUMN_NAME,
                                                     datasetclass=datasetclass)
            self._files = dataset_helper.get_file_name_list()
            self._files = [f.strip("/") for f in self._files]
            self._root_dir = dataset_helper._data_dir
        else:
            for filename in open(image_list_file):
                self._files.append(filename.strip())
            # remove blank strings
            self._files = [f for f in self._files if f]
            self._root_dir = root_dir

        self._transform = transforms
        self._ignore_data_errors = ignore_data_errors

    def __len__(self):
        """Size of the dataset."""
        return len(self._files)

    def __getitem__(self, idx):
        """
        :param idx: index
        :type idx: int
        :return: item and label at index idx
        :rtype: tuple[str, image]
        """
        filename = self._files[idx]
        if self._root_dir and filename:
            filename = filename.lstrip('/')
        full_path = os.path.join(self._root_dir, filename)

        image = _read_image(self._ignore_data_errors, full_path)
        if image is not None:
            if self._transform:
                image = self._transform(image)

        return filename, image
