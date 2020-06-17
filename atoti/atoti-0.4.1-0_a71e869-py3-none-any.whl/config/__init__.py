"""Session configuration."""

from __future__ import annotations

import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import Collection, Optional, Union

import yaml

from .._serialization_utils import FromDict
from ..sampling import DEFAULT_SAMPLING_MODE, SamplingMode
from ._auth import Auth
from ._auth_basic import BasicAuthentication, BasicUser
from ._auth_utils import merge_auth, parse_auth
from ._oidc import OidcAuthentication
from ._role import Role, create_role
from ._utils import Mergeable, _get_default_config_path
from ._yaml_utils import EnvVarLoader
from .parsing import ConfigParsingError

DEFAULT_URL_PATTERN = "http://localhost:{port}"


@dataclass(frozen=True)
class SessionConfiguration(FromDict, Mergeable):
    """Configuration of the session."""

    inherit: bool
    port: Optional[int]
    url_pattern: Optional[str]
    metadata_db: Optional[str]
    roles: Optional[Collection[Role]]
    authentication: Optional[Auth]
    sampling_mode: Optional[SamplingMode]
    max_memory: Optional[str]
    java_args: Optional[Collection[str]]

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        if "roles" in data:
            if not isinstance(data["roles"], Collection):
                raise ConfigParsingError("roles must be a collection.")
            roles = [Role._from_dict(role) for role in data["roles"]]
        else:
            roles = None
        auth = parse_auth(data["authentication"]) if "authentication" in data else None
        sampling_mode = (
            SamplingMode._from_dict(data["sampling_mode"])
            if "sampling_mode" in data
            else None
        )
        return SessionConfiguration(
            inherit=data.get("inherit", True),
            port=data.get("port"),
            url_pattern=data.get("url_pattern"),
            metadata_db=data.get("metadata_db"),
            roles=roles,
            authentication=auth,
            sampling_mode=sampling_mode,
            max_memory=data.get("max_memory"),
            java_args=data.get("java_args"),
        )

    @classmethod
    def _do_merge(
        cls, instance1: SessionConfiguration, instance2: SessionConfiguration
    ) -> SessionConfiguration:
        """Merge two instances of the class. Second overrides the first one."""
        if instance1.roles is None:
            roles = instance2.roles
        elif instance2.roles is None:
            roles = instance1.roles
        else:
            role_names2 = [role.name for role in instance2.roles]
            roles = list(instance2.roles) + [
                i for i in instance1.roles if i.name not in role_names2
            ]

        return SessionConfiguration(
            inherit=instance1.inherit and instance2.inherit,
            port=instance2.port or instance1.port,
            url_pattern=instance2.url_pattern or instance1.url_pattern,
            metadata_db=instance2.metadata_db or instance1.metadata_db,
            roles=roles,
            authentication=merge_auth(
                instance1.authentication, instance2.authentication
            ),
            sampling_mode=instance2.sampling_mode or instance1.sampling_mode,
            max_memory=instance2.max_memory or instance1.max_memory,
            java_args=instance2.java_args or instance1.java_args,
        )

    def _complete_with_default(self) -> SessionConfiguration:
        """Copy the config into a new one with the default values.

        These values should only be set if None is provided.
        They are not set when creating the configuration to able clean merging.
        """
        return SessionConfiguration(
            inherit=self.inherit,
            port=self.port,
            url_pattern=self.url_pattern or DEFAULT_URL_PATTERN,
            metadata_db=self.metadata_db,
            roles=self.roles,
            authentication=self.authentication,
            sampling_mode=self.sampling_mode or DEFAULT_SAMPLING_MODE,
            max_memory=self.max_memory,
            java_args=self.java_args,
        )


def parse_yaml_to_config(path: Path) -> SessionConfiguration:
    """Parse a YAML config file."""
    config_data = yaml.load(open(path), Loader=EnvVarLoader)  # nosec
    return SessionConfiguration._from_dict(config_data)


def create_config(
    *,
    inherit: bool = True,
    port: Optional[int] = None,
    url_pattern: Optional[str] = None,
    metadata_db: Optional[str] = None,
    roles: Optional[Collection[Role]] = None,
    authentication: Optional[Auth] = None,
    sampling_mode: Optional[SamplingMode] = None,
    max_memory: Optional[str] = None,
    java_args: Optional[Collection[str]] = None,
) -> SessionConfiguration:
    """Create a configuration.

    Args:
        inherit: Whether this config should be merged with the default config if it exists.
        port: The port on which the session will be exposed. Defaults to a random available port.
        url_pattern: The pattern of the public URL of the session.
            The ``{host}`` and ``{port}`` placeholders will be replaced with, respectively,
            the actual host address and port number.
            If ``None``, defaults to ``http://localhost:{port}``.
        metadata_db: The description of the database where the session's metadata will be stored.
            It is the path to a file, which will be created if needed.
        roles: The roles and their restrictions.
        authentication: The authentication used by the server.
        sampling_mode: The sampling mode describing how files are loaded into the stores.
            It's faster to build the data model when only part of the data is loaded.

            Modes are available in :mod:`atoti.sampling`.

            If :data:`atoti.sampling.FULL` isn't passed, call :meth:`load_all_data`
            to load everything once the model definition is done.
        max_memory: Max memory allocated to each session.
            Actually sets the ``-Xmx`` JVM parameter.
            The format is a string containing a number followed by a unit among ``G``, ``M`` and ``K``.
            For instance: ``64G``.
            Defaults to the JVM default memory which is 25% of the machine memory.
        java_args: Collection of additional arguments to pass to the Java process.
            For instance: ``["-verbose:gc", "-Xms1g", "-XX:+UseG1GC"]``.
    """
    return SessionConfiguration(
        inherit=inherit,
        port=port,
        url_pattern=url_pattern,
        metadata_db=metadata_db,
        roles=roles,
        authentication=authentication,
        sampling_mode=sampling_mode,
        max_memory=max_memory,
        java_args=java_args,
    )


def _get_merged_config(
    provided_config: Optional[Union[SessionConfiguration, Path, str]]
) -> SessionConfiguration:
    """Get the config merged from the provided one and the default one.

    Args:
        provided_config: the config provided to the user. Either the object or a path.
        merge: Whether to merge the provided config with the default one.

    Returns:
        The configuration, merged with the default if necessary.

    """
    if isinstance(provided_config, str):
        provided_config = Path(provided_config)
    if isinstance(provided_config, Path):
        provided_config = parse_yaml_to_config(provided_config)
    if provided_config is not None and provided_config.inherit is False:
        return provided_config
    default_path = _get_default_config_path()
    if default_path is None or not os.path.isfile(default_path):
        merged = provided_config
    else:
        merged = SessionConfiguration.merge(
            parse_yaml_to_config(default_path), provided_config
        )
    return merged if merged is not None else create_config()


__all__ = [
    SessionConfiguration.__name__,
    create_config.__name__,
    create_role.__name__,
    BasicUser.__name__,
    BasicAuthentication.__name__,
    OidcAuthentication.__name__,
]
