from typing import Dict
import yaml

try:
    import lastpass
    import lastpass.account

    HAS_LASTPASS = True
except ImportError:
    HAS_LASTPASS = False


# https://pypi.org/project/lastpass-python/


def __virtual__(hub):
    return HAS_LASTPASS


def get_profile(hub, account: lastpass.account.Account) -> Dict[str, str]:
    # The profile will be the account name
    profile = {}

    # Read in the profile data from the notes
    for line in account.notes.splitlines():
        line = line.decode()

        # Substitute key words for certain values
        try:
            line = line.format(id=account.id)
        except KeyError:
            pass
        try:
            line = line.format(password=account.password.decode())
        except KeyError:
            pass
        try:
            line = line.format(username=account.username.decode())
        except KeyError:
            pass
        try:
            line = line.format(url=account.url.decode())
        except KeyError:
            pass

        profile.update(yaml.safe_load(line))

    return profile


def unlock(
        hub,
        username: str,
        password: str,
        folder_key: str,
        blob_filename: str = None,
        multifactor_password: str = None,
        client_id: str = None,
) -> Dict[str, Dict[str, Dict[str, str]]]:
    if blob_filename is not None:
        vault = lastpass.Vault.open_local(
            blob_filename=blob_filename, username=username, password=password
        )
    else:
        vault = lastpass.Vault.open_remote(
            username=username,
            password=password,
            multifactor_password=multifactor_password,
            client_id=client_id,
        )

    ret = {}
    for account in vault.accounts:
        # The provider will be the account group
        provider = account.group.decode()
        profile = account.name.decode()
        if not provider.startswith(folder_key):
            # Only look at lastpass data we are meant to see
            continue
        else:
            provider = provider.replace(folder_key, "")
        if not provider:
            continue
        if not profile:
            continue

        if provider not in ret:
            ret[provider] = {}

        ret[provider][profile] = hub.acct.lastpass.get_profile(account)

    return ret
