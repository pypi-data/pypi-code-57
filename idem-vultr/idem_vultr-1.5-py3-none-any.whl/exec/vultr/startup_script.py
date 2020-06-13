import os
from typing import Any, Dict, Tuple

__virtualname__ = "script"
__func_alias__ = {
    "destroy": "delete",
    "list_": "list",
}


async def create(
    hub, ctx, name: str, content: str, pxe: bool = False,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a new user.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.startupscript.create
    """
    if os.path.exists(content):
        with open(content, "r") as fh_:
            content = fh_.read()
    return await hub.exec.vultr.util.query(
        ctx,
        "startupscript/create",
        method="POST",
        name=name,
        raw_script=content,
        type="pxe" if pxe else "boot",
    )


async def destroy(hub, ctx, script: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Remove a startup script.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.startupscript.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "startupscript/destroy", method="POST", script=script
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all startup scripts on the current account. 

    CLI Example:

    .. code-block:: bash
        idem exec vultr.startupscript.list
    """
    return await hub.exec.vultr.util.query(ctx, "startupscript/list")


async def update(
    hub, ctx, name: str, script: int, contents: str,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Update an existing startup script.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.startupscript.update
    """
    return await hub.exec.vultr.util.query(
        ctx, "startupscript/update", name=name, script=script, contents=contents
    )
