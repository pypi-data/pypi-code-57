# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for Dataset consumption configuration."""

import re


class DatasetConsumptionConfig:
    """Represent how to deliver the dataset to a compute target.

    :param name: The name of the dataset in the run, which can be different to the registered name.
        The name will be registered as environment variable and can be used in data plane.
    :param dataset: The dataset that will be consumed in the run.
    :type dataset: azureml.core.dataset.Dataset
    :type name: str
    :param mode: Defines how the dataset should be delivered to the compute target. There are three modes:
        1. 'direct': consume the dataset as dataset.
        2. 'download': download the dataset and consume the dataset as downloaded path.
        3. 'mount': mount the dataset and consume the dataset as mount path.
    :type mode: str
    :param path_on_compute: The target path on the compute to make the data available at. The folder structure
            of the source data will be kept, however, we might add prefixes to this folder structure to avoid
            collision. Use ``tabular_dataset.to_path`` to see the output folder structure.
    :type path_on_compute: str
    """

    _SUPPORTED_MODE = {'direct', 'mount', 'download'}

    def __init__(self, name, dataset, mode='direct', path_on_compute=None):
        """Represent how to deliver the dataset to the compute target.

        :param name: The name of the dataset in the run, which can be different to the registered name.
            The name will be registered as environment variable and can be used in data plane.
        :type name: str
        :param dataset: The dataset to be delivered, as a Dataset object or Pipeline Parameter that ingests a Dataset.
        :type dataset: azureml.core.dataset.Dataset or azureml.pipeline.core.PipelineParameter
        :param mode: Defines how the dataset should be delivered to the compute target. There are three modes:
            1. 'direct': consume the dataset as dataset.
            2. 'download': download the dataset and consume the dataset as downloaded path.
            3. 'mount': mount the dataset and consume the dataset as mount path.
        :type mode: str
        :param path_on_compute: The target path on the compute to make the data available at. The folder structure
            of the source data will be kept, however, we might add prefixes to this folder structure to avoid
            collision. We recommend calling `tabular_dataset.to_path` to see the output folder structure.
        :type path_on_compute: str
        """
        mode = mode.lower()
        DatasetConsumptionConfig._validate_mode(dataset, mode)
        self.dataset = self._validate_if_pipeline_parameter(dataset)
        self.name = self._validate_name(name) if name else None
        self.mode = mode
        self.path_on_compute = path_on_compute

    @staticmethod
    def _validate_name(name):
        from azureml.exceptions import UserErrorException

        if re.search(r"^[a-zA-Z_]+[a-zA-Z0-9_]*$", name):
            return name
        raise UserErrorException(
            "Invalid name {}. Dataset input name can only be alphanumeric characters and underscore, ".format(name) +
            "and must not begin with a number."
        )

    @staticmethod
    def _validate_mode(dataset, mode):
        from azureml.data import FileDataset
        from azureml.exceptions import UserErrorException

        if mode not in DatasetConsumptionConfig._SUPPORTED_MODE:
            raise UserErrorException("Invalid mode '{}'. Mode can only be mount, download, or direct".format(mode))

        try:
            # Expose the underlying dataset for validation
            dataset = dataset.default_value
        except AttributeError:
            pass
        if not isinstance(dataset, FileDataset):
            if mode == 'download' or mode == 'mount':
                raise UserErrorException("{} does not support {}. Only FileDataset supports {}".format(
                    type(dataset), mode, mode
                ))

    @staticmethod
    def _validate_if_pipeline_parameter(param):
        from azureml.data import FileDataset, TabularDataset
        from azureml.exceptions import UserErrorException
        try:
            default_value = param.default_value
        except AttributeError:
            # Passed in param is of type Dataset, skip validation
            return param
        if not (isinstance(default_value, FileDataset) or isinstance(default_value, TabularDataset)):
            raise UserErrorException("Invalid PipelineParameter with default value '{}. Default value must be of "
                                     "types: {} or {}".format(default_value, FileDataset.__name__,
                                                              TabularDataset.__name__))
        return param

    def as_download(self, path_on_compute=None):
        """Set the mode to download.

        .. remarks::

            If path_on_compute starts with a /, then it will be treated as an absolute path. If it doesn't start
            with a /, then it will be treated as a relative path relative to the working directory. If you have
            specified an absolute path, please make sure that the job has permission to write to that directory.

        :param path_on_compute: The target path on the compute to make the data available at.
        :type path_on_compute: str
        """
        return DatasetConsumptionConfig(name=self.name, dataset=self.dataset,
                                        mode='download', path_on_compute=path_on_compute)

    def as_mount(self, path_on_compute=None):
        """Set the mode to mount.

        .. remarks::

            If path_on_compute starts with a /, then it will be treated as an absolute path. If it doesn't start
            with a /, then it will be treated as a relative path relative to the working directory. If you have
            specified an absolute path, please make sure that the job has permission to write to that directory.

        :param path_on_compute: The target path on the compute to make the data available at.
        :type path_on_compute: str
        """
        return DatasetConsumptionConfig(name=self.name, dataset=self.dataset,
                                        mode='mount', path_on_compute=path_on_compute)
