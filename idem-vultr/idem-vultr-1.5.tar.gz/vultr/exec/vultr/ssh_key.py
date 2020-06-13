import os
from typing import Any, Dict, Tuple

__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def create(hub, ctx, name: str, ssh_key: str,) -> Tuple[bool, Dict[str, Any]]:
    """
    CLI Example:

    .. code-block:: bash
        idem exec vultr.sshkey.create
    """
    if os.path.exists(ssh_key):
        with open(ssh_key, "r") as fh_:
            ssh_key = fh_.read()
    return await hub.exec.vultr.util.query(
        ctx, "sshkey/create", method="POST", name=name, ssh_key=ssh_key
    )


async def destroy(hub, ctx, key_id: str) -> Tuple[bool, Dict[str, Any]]:
    """
    CLI Example:

    .. code-block:: bash
        idem exec vultr.sshkey.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "sshkey/destroy", method="POST", ssh_key=key_id
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """

    CLI Example:

    .. code-block:: bash
        idem exec vultr.sshkey.list
    """
    return await hub.exec.vultr.util.query(ctx, "sshkey/list")


async def update(
    hub, ctx, key_id: str, ssh_key: str = None, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """

    CLI Example:

    .. code-block:: bash
        idem exec vultr.sshkey.update
    """
    if ssh_key is not None:
        if os.path.exists(ssh_key):
            with open(ssh_key, "r") as fh_:
                ssh_key = fh_.read()
        kwargs["ssh_key"] = ssh_key
    return await hub.exec.vultr.util.query(
        ctx, "sshkey/update", method="POST", ssh_key=key_id, **kwargs
    )
