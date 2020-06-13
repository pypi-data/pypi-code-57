__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx):
    r"""
    Retrieve information about the current account.

    CLI Example:

    .. code-block:: bash

        idem exec vultr.account.get
    """
    return await hub.exec.vultr.util.query(ctx, "account/info")
