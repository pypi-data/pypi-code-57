# -*- coding: utf-8 -*-
"""
D-Bus Secret Service Backend for Acct

.. versionadded:: SOMEVERSIONHERE

:depends: `secretstorage==3.1.2 <https://pypi.org/project/SecretStorage/>`_
:configuration: Get secrets from the local machine's D-Bus Secret Service API
    that is supported by GNOME Keyring (since version 2.30) and KSecretsService.

    Example:

    .. code-block:: yaml

        acct-backend:
            secretstorage:
                designator: "acct-provider-"

    To use this backend, configure your supported operating system keyring with
    a new password keyring which starts with the string denoted in the
    ``designator`` parameter. The default is shown in the example above. The
    following string can be either the acct provider the credentials are for
    (such as "azurerm" or "vultr") or a dash-separated combination of the
    provider and the profile name. This allows for several profiles for the same
    provider.

    Example password keyring names:

    ``acct-provider-azurerm``

    ``acct-provider-azurerm-myprofile``

    The first keyring name will be stored as the default profile for the
    "azurerm" provider, while the second will be a profile named "myprofile"
    for that same provider.

    Stored passwords can be saved inside of the keyring which will end up being
    key-value pairs under the profile. The label/description will be the key and
    the password/secret will be the value.

"""

# Python libs
from typing import Dict

# Third-party libs
try:
    from secretstorage.exceptions import LockedException
    import secretstorage

    HAS_SECRETSTORAGE = True
except ImportError:
    HAS_SECRETSTORAGE = False


def __virtual__(hub):
    return HAS_SECRETSTORAGE


def unlock(
    hub, designator: str = "acct-provider-"
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    .. versionadded:: SOMEVERSIONHERE

    Get secrets from the local machine's D-Bus Secret Service API that is
    supported by GNOME Keyring (since version 2.30) and KSecretsService.

    Example:

    .. code-block:: yaml

        acct-backend:
            secretstorage:
                designator: "acct-provider-"

    """
    ret = {}

    connection = secretstorage.dbus_init()
    collections = secretstorage.get_all_collections(connection)

    for coll in collections:
        fullname = coll.get_label()
        hub.log.debug(f"acct found secretstorage collection {fullname}.")
        if fullname.startswith(designator):
            fullname = fullname.replace(designator, "")
            parts = fullname.split("-")

            try:
                provider = parts[0]
            except IndexError:
                continue
            hub.log.debug(f"acct found provider {provider} via secretstorage.")

            try:
                profile = "-".join(parts[1:]) or "default"
            except IndexError:
                profile = "default"
            hub.log.debug(f"acct found profile {profile} for provider {provider}.")

            ret[provider] = {}
            ret[provider][profile] = {}

            if coll.is_locked():
                coll.unlock()

            items = coll.get_all_items()
            for item in items:
                name = item.get_label()
                hub.log.debug(
                    f"acct found parameter {name} in profile {profile} for {provider}."
                )

                try:
                    secret = item.get_secret()
                except LockedException as exc:
                    hub.log.error(f"{coll.get_label()} {exc}")

                if isinstance(secret, bytes):
                    secret = secret.decode("utf-8")
                ret[provider][profile][name] = secret

    return ret
