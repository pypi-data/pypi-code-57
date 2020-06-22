# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container class used for passing feature sweeped state around during data transformation."""
from typing import Optional, List, Union

import numpy as np
from sklearn import preprocessing
from sklearn_pandas import DataFrameMapper

from azureml.automl.runtime.data_context import TransformedDataContext
from azureml.automl.runtime.featurization import DataTransformer, TransformerAndMapper
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.automl.core.shared.exceptions import ClientException, InvalidArgumentException


class FeatureSweepedStateContainer:
    """
    Lightweight container class holding a group of objects
    frequently passed around together during data transformation.
    """
    def __init__(self,
                 data_transformer: DataTransformer,
                 transformed_data_context: TransformedDataContext,
                 y_transformer: Optional[preprocessing.LabelEncoder],
                 x: DataInputType,
                 y: np.ndarray):
        """
        Initialize a state container to describe the state of feature sweeping.

        :param data_transformer: The data_transformer generated in feature sweeping.
        :param transformed_data_context: The (unfinished) transformed data context
            that was created during feature sweeping.
        :param y_transformer: The y_transformer object that was created during feature sweeping.
        :param x: The input data used during data transformation.
        :param y: The input data used during data transformation.
        """
        self.data_transformer = data_transformer
        self.transformed_data_context = transformed_data_context
        self.y_transformer = y_transformer
        self.X = x
        self.y = y

    def get_feature_config(self) -> Union[List[TransformerAndMapper], DataFrameMapper]:
        """
        Get the feature config, which is stored in the data transformer.
        This is needed to reconstruct the data transformer in the featurization run.

        :raises InvalidArgumentException: If DataTransformer is missing.
        :return: The list of transformers and mappers to perform full featurization on,
            or the mapper to be used by onnx if it is enabled.
        """
        if self.data_transformer is None:
            raise InvalidArgumentException(exception_message="Attempted to retrieve feature config from missing "
                                                             "data transformer. Feature sweeping likely experienced an"
                                                             " error.", has_pii=False)
        if self.data_transformer._is_onnx_compatible:
            feature_config = self.data_transformer.mapper
        else:
            feature_config = self.data_transformer.transformer_and_mapper_list

        if feature_config is None:
            raise ClientException("Encountered null feature_config. The FeatureSweepedStateContainer should "
                                  "not be used before feature sweeping has finished.", has_pii=False)
        return feature_config

    def get_engineered_feature_names(self) -> _GenerateEngineeredFeatureNames:
        """
        Get the engineered feature names class, which is stored in the data transformer.
        This is needed to reconstruct the data transformer in the featurization run.

        :raises InvalidArgumentException: If DataTransformer is missing.
        :return: The engineered feature names class that is used to generate the engineered feature names.
        """
        if self.data_transformer is None:
            raise InvalidArgumentException(exception_message="Attempted to retrieve feature names from missing "
                                                             "data transformer. Feature sweeping likely experienced an"
                                                             " error.", has_pii=False)

        engineered_feature_names_class = self.data_transformer._engineered_feature_names_class
        if engineered_feature_names_class is None:
            raise ClientException("Unexpectedly encountered null engineered feature names class instance.",
                                  has_pii=False)
        return engineered_feature_names_class
