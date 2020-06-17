"""OpenID Connect authentication."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Collection, Mapping, Optional

from ._auth import Auth
from ._utils import Mergeable
from .parsing import ConfigParsingError

OIDC_AUTH_TYPE = "oidc"


@dataclass(frozen=True)
class OidcAuthentication(Auth, Mergeable):
    """OpenID connect authentication."""

    provider_id: Optional[str] = None
    issuer_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    paths_to_authorities: Optional[Collection[str]] = None
    role_mapping: Optional[Mapping[str, Collection[str]]] = field(default_factory=dict)

    @property
    def _type(self):
        return OIDC_AUTH_TYPE

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        provider_id = data.get("provider_id")
        issuer_url = data.get("issuer_url")
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        paths_to_authorities = data.get("paths_to_authorities")
        role_mapping = data.get("role_mapping")
        if role_mapping is None:
            role_mapping = {}
        if role_mapping is not None and not isinstance(role_mapping, dict):
            raise ConfigParsingError(
                "The OpenID Connect role mappings must be a dict", role_mapping
            )

        return OidcAuthentication(
            provider_id,
            issuer_url,
            client_id,
            client_secret,
            paths_to_authorities,
            role_mapping,
        )

    @classmethod
    def _do_merge(
        cls, instance1: OidcAuthentication, instance2: OidcAuthentication
    ) -> OidcAuthentication:
        """Merge the OpenID Connect authentications."""
        if instance2.provider_id is None:
            provider_id = instance1.provider_id
        elif instance1.provider_id is None:
            provider_id = instance2.provider_id
        elif instance1.provider_id != instance2.provider_id:
            raise ValueError("Cannot merge configurations for two different providers")
        else:
            provider_id = instance1.provider_id
        issuer_url = (
            instance2.issuer_url
            if instance2.issuer_url is not None
            else instance1.issuer_url
        )
        client_id = (
            instance2.client_id
            if instance2.client_id is not None
            else instance1.client_id
        )
        client_secret = (
            instance2.client_secret
            if instance2.client_secret is not None
            else instance1.client_secret
        )
        if instance1.paths_to_authorities is None:
            paths_to_authorities = instance2.paths_to_authorities
        elif instance2.paths_to_authorities is None:
            paths_to_authorities = instance1.paths_to_authorities
        else:
            paths_to_authorities = [
                *instance1.paths_to_authorities,
                *instance2.paths_to_authorities,
            ]
        if instance1.role_mapping is None:
            roles = instance2.role_mapping
        elif instance2.role_mapping is None:
            roles = instance1.role_mapping
        else:
            roles = {**instance1.role_mapping, **instance2.role_mapping}
        return OidcAuthentication(
            provider_id,
            issuer_url,
            client_id,
            client_secret,
            paths_to_authorities,
            roles,
        )
