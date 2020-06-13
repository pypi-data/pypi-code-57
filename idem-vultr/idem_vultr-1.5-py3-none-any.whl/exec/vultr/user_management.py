from typing import Any, Dict, Tuple, List

__virtualname__ = "user"
__func_alias__ = {
    "list_": "list",
}


async def create(
    hub,
    ctx,
    name: str,
    password: str,
    email: str,
    acls: List[str],
    api_enabled: bool = True,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new user.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.user.create
    """
    kwargs = {}
    return await hub.exec.vultr.util.query(
        ctx,
        "user/create",
        method="POST",
        email=email,
        name=name,
        password=password,
        api_enabled="yes" if api_enabled else "no",
        acls=acls,
    )


async def delete(hub, ctx, user_id: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Delete a user.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.net.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "user/delete", method="POST", USERID=user_id
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieve a list of any users associated with this account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.net.list
    """
    return await hub.exec.vultr.util.query(ctx, "user/list")


async def update(
    hub,
    ctx,
    name: str,
    password: str,
    email: str,
    acls: List[str],
    user_id: str,
    **kwargs,
) -> Tuple[bool, Dict[str, Any]]:
    """
    List all domains associated with the current account.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.net.list
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "user/update",
        method="POST",
        name=name,
        password=password,
        email=email,
        acls=acls,
        USERID=user_id,
        **kwargs,
    )
