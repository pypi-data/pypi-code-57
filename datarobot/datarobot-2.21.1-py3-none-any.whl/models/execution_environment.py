import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.execution_environment_version import ExecutionEnvironmentVersion
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate


class ExecutionEnvironment(APIObject):
    """An execution environment entity.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        the id of the execution environment
    name: str
        the name of the execution environment
    description: str, optional
        the description of the execution environment
    programming_language: str, optional
        the programming language of the execution environment.
        Can be "python", "r", "java" or "other"
    is_public: bool, optional
        public accessibility of environment, visible only for admin user
    created_at: str, optional
        ISO-8601 formatted timestamp of when the execution environment version was created
    latest_version: ExecutionEnvironmentVersion, optional
        the latest version of the execution environment
    """

    _path = "executionEnvironments/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(max_length=255),
            t.Key("description", optional=True): t.String(
                max_length=10000, allow_blank=True
            ) | t.Null(),
            t.Key("programming_language", optional=True): t.String(),
            t.Key("is_public", optional=True): t.Bool(),
            t.Key("created", optional=True) >> "created_at": t.String(),
            t.Key("latest_version", optional=True): ExecutionEnvironmentVersion.schema,
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
        description=None,
        programming_language=None,
        is_public=None,
        created_at=None,
        latest_version=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.programming_language = programming_language
        self.is_public = is_public
        self.created_at = created_at

        if latest_version is not None:
            latest_version.pop("image_id", None)  # "image_id" is being removed in RAPTOR-2460
            self.latest_version = ExecutionEnvironmentVersion(**latest_version)
        else:
            self.latest_version = None

    @classmethod
    def create(cls, name, description=None, programming_language=None):
        """Create an execution environment.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: str
            execution environment name
        description: str, optional
            execution environment description
        programming_language: str, optional
            programming language of the environment to be created.
            Can be "python", "r", "java" or "other". Default value - "other"

        Returns
        -------
        ExecutionEnvironment
            created execution environment

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {
            "name": name,
            "description": description,
            "programming_language": programming_language,
        }
        response = cls._client.post(cls._path, data=payload)
        environment_id = response.json()["id"]
        return cls.get(environment_id)

    @classmethod
    def list(cls, search_for=None):
        """List execution environments available to the user.

        .. versionadded:: v2.21

        Parameters
        ----------
        search_for: str, optional
            the string for filtering execution environment - only execution
            environments that contain the string in name or description will
            be returned.

        Returns
        -------
        List[ExecutionEnvironment]
            a list of execution environments.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(cls._path, {"search_for": search_for}, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, execution_environment_id):
        """Get execution environment by it's id.

        .. versionadded:: v2.21

        Parameters
        ----------
        execution_environment_id: str
            ID of the execution environment to retrieve

        Returns
        -------
        ExecutionEnvironment
            retrieved execution environment

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}{}/".format(cls._path, execution_environment_id)
        return cls.from_location(path)

    def delete(self):
        """Delete execution environment.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = "{}{}/".format(self._path, self.id)
        self._client.delete(url)

    def update(self, name=None, description=None):
        """Update execution environment properties.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: str, optional
            new execution environment name
        description: str, optional
            new execution environment description

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {"name": name, "description": description}

        url = "{}{}/".format(self._path, self.id)
        response = self._client.patch(url, data=payload)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def refresh(self):
        """Update execution environment with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = "{}{}/".format(self._path, self.id)
        response = self._client.get(url)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))
