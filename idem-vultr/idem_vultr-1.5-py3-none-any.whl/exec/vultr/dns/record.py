from typing import Any, Dict, Tuple

__func_alias__ = {
    "list_": "list",
}


async def create(
    hub, ctx, name: str, domain: str, type_: str, data: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.record.create
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "dns/create_record",
        method="POST",
        domain=domain,
        name=name,
        data=data,
        **kwargs,
    )


async def delete(hub, ctx, domain: str, recordid: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Delete an individual DNS record.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.record.delete
    """
    return await hub.exec.vultr.util.query(
        ctx, "dns/delete_record", method="POST", domain=domain, recordid=recordid
    )


async def list_(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    List all the records associated with a particular domain.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.record.list
    """
    return await hub.exec.vultr.util.query(ctx, "dns/records")


async def update(
    hub, ctx, domain: str, record: int, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    """
    Update a DNS record.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.record.list
    """
    return await hub.exec.vultr.util.query(
        ctx, "dns/update_record", method="POST", domain=domain, record=record, **kwargs,
    )
