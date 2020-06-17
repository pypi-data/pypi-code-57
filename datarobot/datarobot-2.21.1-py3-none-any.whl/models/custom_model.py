import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT, TARGET_TYPE
from datarobot.models import CustomModelVersion

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class _CustomModelBase(APIObject):
    _path = "customModels/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("description"): t.String(allow_blank=True),
            t.Key("supports_binary_classification"): t.Bool(),
            t.Key("supports_regression"): t.Bool(),
            t.Key("latest_version"): CustomModelVersion.schema,
            t.Key("deployments_count"): t.Int(),
            t.Key("created_by"): t.String(),
            t.Key("updated") >> "updated_at": t.String(),
            t.Key("created") >> "created_at": t.String(),
        }
    ).allow_extra("*")

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return encode_utf8_if_py2(
            u"{}({!r})".format(self.__class__.__name__, self.name or self.id)
        )

    def _set_values(
            self,
            id,
            name,
            description,
            supports_binary_classification,
            supports_regression,
            latest_version,
            deployments_count,
            created_by,
            updated_at,
            created_at,
    ):
        self.id = id
        self.name = name
        self.description = description

        if supports_binary_classification:
            self.target_type = TARGET_TYPE.BINARY
        elif supports_regression:
            self.target_type = TARGET_TYPE.REGRESSION
        else:
            raise ValueError('Model should support only 1 target type')

        self.latest_version = CustomModelVersion(**latest_version)
        self.deployments_count = deployments_count
        self.created_by = created_by
        self.updated_at = updated_at
        self.created_at = created_at

    @classmethod
    def _check_model_type(cls, data):
        return data['customModelType'] == cls._model_type

    @classmethod
    def list(
        cls,
        is_deployed=None,
        order_by=None,
        search_for=None
    ):
        payload = {
            "custom_model_type": cls._model_type,
            "is_deployed": is_deployed,
            "order_by": order_by,
            "search_for": search_for,
        }
        data = unpaginate(cls._path, payload, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_model_id):
        path = "{}{}/".format(cls._path, custom_model_id)
        data = cls._client.get(path).json()
        if not cls._check_model_type(data):
            raise Exception("Requested model is not a learning model")
        return cls.from_server_data(data)

    def download_latest_version(self, file_path):
        path = "{}{}/download/".format(self._path, self.id)

        response = self._client.get(path)
        with open(file_path, "wb") as f:
            f.write(response.content)

    @classmethod
    def create(
        cls,
        name,
        target_type,
        description,
        **kwargs
    ):
        payload = dict(
            custom_model_type=cls._model_type,
            name=name,
            description=description,
            **kwargs
        )
        if target_type == TARGET_TYPE.BINARY:
            payload['supports_binary_classification'] = True
        elif target_type == TARGET_TYPE.REGRESSION:
            payload['supports_regression'] = True
        else:
            raise ValueError('Unsupported target_type. Only {} and {} are supported.'.format(
                TARGET_TYPE.BINARY, TARGET_TYPE.REGRESSION
            ))

        response = cls._client.post(cls._path, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def copy_custom_model(
        cls,
        custom_model_id,
    ):
        path = "{}fromCustomModel/".format(cls._path)
        response = cls._client.post(path, data={'custom_model_id': custom_model_id})
        return cls.from_server_data(response.json())

    def update(
        self,
        name,
        description,
        **kwargs
    ):
        payload = dict(
            name=name,
            description=description,
            **kwargs
        )
        url = "{}{}/".format(self._path, self.id)
        response = self._client.patch(url, data=payload)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def refresh(self):
        url = self._path.format(self.id)
        path = "{}{}/".format(url, self.id)

        response = self._client.get(path)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def delete(self):
        url = "{}{}/".format(self._path, self.id)
        self._client.delete(url)


class CustomInferenceModel(_CustomModelBase):
    """A custom inference model.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        id of the custom model
    name: str
        name of the custom model
    language: str
        programming language of the custom model.
        Can be "python", "r", "java" or "other"
    description: str
        description of the custom model
    target_type: datarobot.TARGET_TYPE
        custom model target type.
        Can be `datarobot.TARGET_TYPE.BINARY` or `datarobot.TARGET_TYPE.REGRESSION`
    latest_version: datarobot.CustomModelVersion
        latest version of the custom model
    deployments_count: int
        number of a deployments of the custom models
    target_name: str
        custom model target name
    positive_class_label: str
        for binary classification projects, a label of a positive class
    negative_class_label: str
        for binary classification projects, a label of a negative class
    prediction_threshold: float
        for binary classification projects, a threshold used for predictions
    training_data_assignment_in_progress: bool
        flag describing if training data assignment is in progress
    training_dataset_id: str, optional
        id of a dataset assigned to the custom model
    training_dataset_version_id: str, optional
        id of a dataset version assigned to the custom model
    training_data_file_name: str, optional
        name of assigned training data file
    training_data_partition_column: str, optional
        name of a partition column in a training dataset assigned to the custom model
    created_by: str
        username of a user who user who created the custom model
    updated_at: str
        ISO-8601 formatted timestamp of when the custom model was updated
    created_at: str
        ISO-8601 formatted timestamp of when the custom model was created
    """

    _model_type = "inference"
    _converter = (
        _CustomModelBase._converter + {
            t.Key("language"): t.String(allow_blank=True),
            t.Key("target_name"): t.String(),
            t.Key("training_dataset_id", optional=True): t.String(),
            t.Key("training_dataset_version_id", optional=True): t.String(),
            t.Key("training_data_assignment_in_progress"): t.Bool(),
            t.Key("positive_class_label"): t.String(),
            t.Key("negative_class_label"): t.String(),
            t.Key("prediction_threshold"): t.Float(),
            t.Key("training_data_file_name", optional=True): t.String(),
            t.Key("training_data_partition_column", optional=True): t.String(),
        }
    ).allow_extra("*")

    def __init__(self, *args, **kwargs):
        super(CustomInferenceModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return super(CustomInferenceModel, self).__repr__()

    def _set_values(
            self,
            language,
            target_name,
            training_data_assignment_in_progress,
            positive_class_label,
            negative_class_label,
            prediction_threshold,
            training_dataset_id=None,
            training_dataset_version_id=None,
            training_data_file_name=None,
            training_data_partition_column=None,
            **custom_model_kwargs
    ):
        super(CustomInferenceModel, self)._set_values(**custom_model_kwargs)

        self.language = language
        self.target_name = target_name
        self.training_dataset_id = training_dataset_id
        self.training_dataset_version_id = training_dataset_version_id
        self.training_data_assignment_in_progress = training_data_assignment_in_progress
        self.positive_class_label = positive_class_label
        self.negative_class_label = negative_class_label
        self.prediction_threshold = prediction_threshold
        self.training_data_file_name = training_data_file_name
        self.training_data_partition_column = training_data_partition_column

    @classmethod
    def list(
        cls,
        is_deployed=None,
        search_for=None,
        order_by=None,
    ):
        """List custom inference models available to the user.

        .. versionadded:: v2.21

        Parameters
        ----------
        is_deployed: bool, optional
            flag for filtering custom inference models.
            If set to `True`, only deployed custom inference models are returned.
            If set to `False`, only not deployed custom inference models are returned
        search_for: str, optional
            string for filtering custom inference models - only custom
            inference models that contain the string in name or description will
            be returned.
            If not specified, all custom models will be returned
        order_by: str, optional
            property to sort custom inference models by.
            Supported properties are "created" and "updated".
            Prefix the attribute name with a dash to sort in descending order,
            e.g. order_by='-created'.
            By default, the order_by parameter is None which will result in
            custom models being returned in order of creation time descending

        Returns
        -------
        List[CustomInferenceModel]
            a list of custom inference models.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        return super(CustomInferenceModel, cls).list(is_deployed, order_by, search_for)

    @classmethod
    def get(cls, custom_model_id):
        """Get custom inference model by id.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            id of the custom inference model

        Returns
        -------
        CustomInferenceModel
            retrieved custom inference model

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        return super(CustomInferenceModel, cls).get(custom_model_id)

    def download_latest_version(self, file_path):
        """Download the latest custom inference model version.

        .. versionadded:: v2.21

        Parameters
        ----------
        file_path: str
            path to create a file with custom model version content

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        super(CustomInferenceModel, self).download_latest_version(file_path)

    @classmethod
    def create(
        cls,
        name,
        target_type,
        target_name,
        language=None,
        description=None,
        positive_class_label=None,
        negative_class_label=None,
        prediction_threshold=None,
    ):
        """Create a custom inference model.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: str
            name of the custom inference model
        target_type: datarobot.TARGET_TYPE
            target type of the custom inference model.
            Can be `datarobot.TARGET_TYPE.BINARY` or `datarobot.TARGET_TYPE.REGRESSION`
        language: str, optional
            programming language of the custom learning model
        description: str, optional
            description of the custom learning model
        positive_class_label: str, optional
            custom inference model positive class label
        negative_class_label: str, optional
            custom inference model negative class label
        prediction_threshold: float, optional
            custom inference model prediction threshold

        Returns
        -------
        CustomInferenceModel
            created a custom inference model

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        return super(CustomInferenceModel, cls).create(
            name,
            target_type,
            description,
            language=language,
            target_name=target_name,
            positive_class_label=positive_class_label,
            negative_class_label=negative_class_label,
            prediction_threshold=prediction_threshold,
        )

    @classmethod
    def copy_custom_model(
        cls,
        custom_model_id,
    ):
        """Create a custom inference model by copying existing one.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            id of the custom inference model to copy

        Returns
        -------
        CustomInferenceModel
            created a custom inference model

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        return super(CustomInferenceModel, cls).copy_custom_model(custom_model_id)

    def update(
        self,
        name=None,
        language=None,
        description=None,
        target_name=None,
        positive_class_label=None,
        negative_class_label=None,
        prediction_threshold=None,
    ):
        """Update custom inference model properties.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: str, optional
            new custom inference model name
        language: str, optional
            new custom inference model programming language
        description: str, optional
            new custom inference model description
        target_name: str, optional
            new custom inference model target name
        positive_class_label: str, optional
            new custom inference model positive class label
        negative_class_label: str, optional
            new custom inference model negative class label
        prediction_threshold: float, optional
            new custom inference model prediction threshold

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        super(CustomInferenceModel, self).update(
            name,
            description,
            language=language,
            target_name=target_name,
            positive_class_label=positive_class_label,
            negative_class_label=negative_class_label,
            prediction_threshold=prediction_threshold,
        )

    def refresh(self):
        """Update custom inference model with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        super(CustomInferenceModel, self).refresh()

    def delete(self):
        """Delete custom inference model.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        super(CustomInferenceModel, self).delete()

    def assign_training_data(self, dataset_id, partition_column=None, max_wait=DEFAULT_MAX_WAIT):
        """Assign training data to the custom inference model.

        .. versionadded:: v2.21

        Parameters
        ----------
        dataset_id: str
            the id of the training dataset to be assigned
        partition_column: str, optional
            name of a partition column in the training dataset
        max_wait: int, optional
            max time to wait for a training data assignment.
            If set to None - method will return without waiting.
            Defaults to 10 min

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {'dataset_id': dataset_id, 'partition_column': partition_column}

        path = "{}{}/trainingData/".format(self._path, self.id)

        response = self._client.patch(path, data=payload)

        if max_wait is not None:
            wait_for_async_resolution(self._client, response.headers['Location'], max_wait)

        self.refresh()
