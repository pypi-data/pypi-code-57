import os
import contextlib2
import trafaret as t
from requests_toolbelt import MultipartEncoder

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate


class CustomModelFileItem(APIObject):
    """A file item attached to a DataRobot custom model version.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        id of the file item
    file_name: str
        name of the file item
    file_path: str
        path of the file item
    file_source: str
        source of the file item
    created_at: str, optional
        ISO-8601 formatted timestamp of when the version was created
    """

    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("file_name"): t.String(),
            t.Key("file_path"): t.String(),
            t.Key("file_source"): t.String(),
            t.Key("created", optional=True) >> "created_at": t.String(),
        }
    ).allow_extra("*")

    schema = _converter

    def __init__(
        self,
        id,
        file_name,
        file_path,
        file_source,
        created_at=None,
    ):
        self.id = id
        self.file_name = file_name
        self.file_path = file_path
        self.file_source = file_source
        self.created_at = created_at


class CustomModelVersion(APIObject):
    """A version of a DataRobot custom model.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        id of the custom model version
    custom_model_id: str
        id of the custom model
    version_minor: int
        a minor version number of custom model version
    version_major: int
        a major version number of custom model version
    is_frozen: bool
        a flag if the custom model version is frozen
    items: List[CustomModelFileItem]
        a list of file items attached to the custom model version
    label: str, optional
        short human readable string to label the version
    description: str, optional
        custom model version description
    created_at: str, optional
        ISO-8601 formatted timestamp of when the version was created
    """

    _path = "customModels/{}/versions/"

    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("custom_model_id"): t.String(),
            t.Key("version_minor"): t.Int(),
            t.Key("version_major"): t.Int(),
            t.Key("is_frozen"): t.Bool(),
            t.Key("items"): t.List(CustomModelFileItem.schema),
            t.Key("label", optional=True): t.String(
                max_length=50, allow_blank=True
            ) | t.Null(),
            t.Key("description", optional=True): t.String(
                max_length=10000, allow_blank=True
            ) | t.Null(),
            t.Key("created", optional=True) >> "created_at": t.String(),
        }
    )

    schema = _converter

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return encode_utf8_if_py2(
            u"{}({!r})".format(self.__class__.__name__, self.label or self.id)
        )

    def _set_values(
        self,
        id,
        custom_model_id,
        version_minor,
        version_major,
        is_frozen,
        items,
        label=None,
        description=None,
        created_at=None,
    ):
        self.id = id
        self.custom_model_id = custom_model_id
        self.version_minor = version_minor
        self.version_major = version_major
        self.is_frozen = is_frozen
        self.items = [CustomModelFileItem.from_data(item) for item in items]
        self.label = label
        self.description = description
        self.created_at = created_at

    @classmethod
    def create_clean(
        cls,
        custom_model_id,
        is_major_update=True,
        folder_path=None,
        files=None,
    ):
        """Create a custom model version without files from previous versions.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model
        is_major_update: bool
            the flag defining if a custom model version
            will be a minor or a major version.
            Default to `True`
        folder_path: str, optional
            the path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path
        files: list, optional
            the list of tuples, where values in each tuple are the local filesystem path and
            the path the file should be placed in the model.
            Example:
            [("/home/user/Documents/myModel/file1.txt", "file1.txt"),
            ("/home/user/Documents/myModel/folder/file2.txt", "folder/file2.txt")]

        Returns
        -------
        CustomModelVersion
            created custom model version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        return cls._create('post', custom_model_id, is_major_update, folder_path, files)

    @classmethod
    def create_from_previous(
        cls,
        custom_model_id,
        is_major_update=True,
        folder_path=None,
        files=None,
        files_to_delete=None,
    ):
        """Create a custom model version containing files from a previous version.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model
        is_major_update: bool, optional
            the flag defining if a custom model version
            will be a minor or a major version.
            Default to `True`
        folder_path: str, optional
            the path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path
        files: list, optional
            the list of tuples, where values in each tuple are the local filesystem path and
            the path the file should be placed in the model.
            Example:
            [("/home/user/Documents/myModel/file1.txt", "file1.txt"),
            ("/home/user/Documents/myModel/folder/file2.txt", "folder/file2.txt")]
        files_to_delete: list, optional
            the list of a file items ids to be deleted
            Example: ["5ea95f7a4024030aba48e4f9", "5ea6b5da402403181895cc51"]

        Returns
        -------
        CustomModelVersion
            created custom model version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        if files_to_delete:
            upload_data = [('filesToDelete', file_id) for file_id in files_to_delete]
        else:
            upload_data = None
        return cls._create(
            'patch', custom_model_id, is_major_update, folder_path, files, upload_data
        )

    @classmethod
    def _create(
        cls,
        method,
        custom_model_id,
        is_major_update,
        folder_path=None,
        files=None,
        extra_upload_data=None
    ):
        url = cls._path.format(custom_model_id)

        with contextlib2.ExitStack() as stack:
            upload_data = [('isMajorUpdate', str(is_major_update))]

            if folder_path:
                for root_path, _, file_paths in os.walk(folder_path):
                    for path in file_paths:
                        file_path = os.path.join(root_path, path)
                        file = stack.enter_context(open(file_path, "rb"))

                        upload_data.append(('file', (os.path.basename(file_path), file)))
                        upload_data.append(('filePath', os.path.relpath(file_path, folder_path)))

            if files:
                for file_path, upload_file_path in files:
                    file = stack.enter_context(open(file_path, "rb"))

                    upload_data.append(('file', (os.path.basename(upload_file_path), file)))
                    upload_data.append(('filePath', upload_file_path))

            if extra_upload_data:
                upload_data += extra_upload_data

            encoder = MultipartEncoder(fields=upload_data)
            headers = {'Content-Type': encoder.content_type}
            response = cls._client.request(method, url, data=encoder, headers=headers)
            return cls.from_server_data(response.json())

    @classmethod
    def list(cls, custom_model_id):
        """List custom model versions.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model

        Returns
        -------
        List[CustomModelVersion]
            a list of custom model versions

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = cls._path.format(custom_model_id)
        data = unpaginate(url, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_model_id, custom_model_version_id):
        """Get custom model version by id.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model
        custom_model_version_id: str
            the id of the custom model version to retrieve

        Returns
        -------
        CustomModelVersion
            retrieved custom model version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        url = cls._path.format(custom_model_id)
        path = "{}{}/".format(url, custom_model_version_id)
        return cls.from_location(path)

    def download(self, file_path):
        """Download custom model version.

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
        url = self._path.format(self.custom_model_id)
        path = "{}{}/download/".format(url, self.id)

        response = self._client.get(path)
        with open(file_path, "wb") as f:
            f.write(response.content)

    def update(self, description):
        """Update custom model version properties.

        .. versionadded:: v2.21

        Parameters
        ----------
        description: str
            new custom model version description

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {"description": description}

        url = self._path.format(self.custom_model_id)
        path = "{}{}/".format(url, self.id)

        response = self._client.patch(path, data=payload)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def refresh(self):
        """Update custom model version with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = self._path.format(self.custom_model_id)
        path = "{}{}/".format(url, self.id)

        response = self._client.get(path)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))
