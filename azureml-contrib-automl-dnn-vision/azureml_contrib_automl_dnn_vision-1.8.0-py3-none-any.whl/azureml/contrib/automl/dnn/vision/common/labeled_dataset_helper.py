# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common helper class for reading labeled Aml Datasets."""

import json
import os
import uuid
import azureml.dataprep as dprep
from azureml.dataprep.api.functions import get_portable_path
from azureml.core import Dataset as AmlDataset


class AmlLabeledDatasetHelper():
    """Helper for AzureML labeled dataset.

    """

    LABEL_COLUMN_PROPERTY = '_Label_Column:Label_'
    DEFAULT_LABEL_COLUMN_NAME = 'label'
    DEFAULT_LABEL_CONFIDENCE_COLUMN_NAME = 'label_confidence'
    COLUMN_PROPERTY = 'Column'
    IMAGE_COLUMN_PROPERTY = '_Image_Column:Image_'
    DEFAULT_IMAGE_COLUMN_NAME = 'image_url'
    PORTABLE_PATH_COLUMN_NAME = 'PortablePath'
    DATASTORE_PREFIX = 'AmlDatastore://'
    PATH_COLUMN_NAME = 'Path'

    def __init__(self, dataset_id, workspace=None,
                 ignore_data_errors=False, datasetclass=AmlDataset,
                 image_column_name=DEFAULT_IMAGE_COLUMN_NAME):
        """Constructor - This reads the labeled dataset and downloads the images that it contains.

        :param dataset_id: dataset id
        :type dataset_id: str
        :param workspace: workspace object
        :type workspace: azureml.core.Workspace
        :param ignore_data_errors: Setting this ignores and files in the labeled dataset that fail to download.
        :type ignore_data_errors: bool
        :param datasetclass: The source dataset class.
        :type datasetclass: class
        :param image_column_name: The column name for the image file.
        :type image_column_names: str
        """

        self._data_dir = os.getcwd()

        ds = datasetclass.get_by_id(workspace, dataset_id)

        self.label_column_name = AmlLabeledDatasetHelper.DEFAULT_LABEL_COLUMN_NAME
        self.image_column_name = image_column_name

        if AmlLabeledDatasetHelper.LABEL_COLUMN_PROPERTY in ds._properties:
            label_property = ds._properties[AmlLabeledDatasetHelper.LABEL_COLUMN_PROPERTY]
            if AmlLabeledDatasetHelper.COLUMN_PROPERTY in label_property:
                self.label_column_name = label_property[AmlLabeledDatasetHelper.COLUMN_PROPERTY]

        if AmlLabeledDatasetHelper.IMAGE_COLUMN_PROPERTY in ds._properties:
            image_property = ds._properties[AmlLabeledDatasetHelper.IMAGE_COLUMN_PROPERTY]
            if AmlLabeledDatasetHelper.COLUMN_PROPERTY in image_property:
                self.image_column_name = image_property[AmlLabeledDatasetHelper.COLUMN_PROPERTY]

        ds._dataflow.write_streams(self.image_column_name, dprep.LocalFileOutput(self._data_dir)).run_local()
        dflow = ds._dataflow.add_column(get_portable_path(dprep.col(self.image_column_name)),
                                        AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME, self.image_column_name)
        self.images_df = dflow.to_pandas_dataframe(extended_types=True)

        if ignore_data_errors:
            missing_file_indices = []
            for index in self.images_df.index:
                full_path = self.get_image_full_path(index)
                if not os.path.exists(full_path):
                    missing_file_indices.append(index)
            self.images_df.drop(missing_file_indices, inplace=True)
            self.images_df.reset_index(inplace=True, drop=True)

    def get_image_full_path(self, index):
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :return: Full path for the local image file
        :rtype: str
        """
        return AmlLabeledDatasetHelper.get_full_path(index, self.images_df, self._data_dir)

    def get_file_name_list(self):
        """Return a list of the relative file names for the images.

        :return: List of the relative file names for the images
        :rtype: list(str)
        """
        return self.images_df[AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME].tolist()

    def get_full_path(index, images_df, data_dir):
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :param images_df: DataFrame containing images.
        :type images_df: Pandas DataFrame
        :param data_dir: data folder
        :type data_dir: str
        :return: Full path for the local image file
        :rtype: str
        """
        image_rel_path = images_df[AmlLabeledDatasetHelper.PORTABLE_PATH_COLUMN_NAME][index]
        return data_dir + '/' + image_rel_path

    def write_dataset_file_line(fw, image_file_name, confidence, label):
        """Write a line to the dataset file.

        :param fw: The file to write to.
        :type fw: file
        :param image_filename: The image file name with path within the datastore.
        :type image_filename: str
        :param confidence: Label confidence value between 0.0 and 1.0
        :type confidence: float
        :param label: The label name.
        :type label: str
        """

        image_full_path = AmlLabeledDatasetHelper.DATASTORE_PREFIX + image_file_name

        fw.write(
            json.dumps(
                {
                    AmlLabeledDatasetHelper.DEFAULT_IMAGE_COLUMN_NAME: image_full_path,
                    AmlLabeledDatasetHelper.DEFAULT_LABEL_CONFIDENCE_COLUMN_NAME: confidence,
                    AmlLabeledDatasetHelper.DEFAULT_LABEL_COLUMN_NAME: label
                }
            )
        )
        fw.write('\n')

    def create(run, datastore, labeled_dataset_file, target_path,
               task, labeled_dataset_factory,
               dataset_id_property_name='labeled_dataset_id'):
        """Create a labeled dataset file.

        :param run: AzureML Run to write the dataset id to..
        :type run: Run
        :param datastore: The AML datastore to stored the Dataset file.
        :type datastore: Datastore
        :param labeled_dataset_file: The name of the Labeled Dataset file.
        :type labeled_dataset_file: str
        :param target_path: The path for the Labeled Dataset file in Datastore
        :type target_path: str
        :param task: The type of Labeled Dataset
        :type task: str
        :param labeled_dataset_factory: The labeled dataset factory class.
        :type labeled_dataset_factory: _LabeledDatasetFactory
        :param dataset_id_property_name: The name of the dataset id property
        :type dataset_id_property_name: str
        """
        datastore.upload_files(files=[labeled_dataset_file], target_path=target_path, overwrite=True)
        labeled_dataset_path = target_path + '/' + labeled_dataset_file
        dataset = labeled_dataset_factory.from_json_lines(task=task,
                                                          path=datastore.path(labeled_dataset_path))
        run.add_properties({dataset_id_property_name: dataset.id})

    def get_default_target_path():
        """Get the default target path in datastore to be used for Labeled Dataset files.

            :return: The default target path
            :rtype: str
            """
        return 'automl/datasets/' + str(uuid.uuid4())
