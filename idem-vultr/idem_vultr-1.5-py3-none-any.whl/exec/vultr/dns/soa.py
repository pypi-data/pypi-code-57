from typing import Any, Dict, Tuple

__virtualname__ = "sec"
__func_alias__ = {
    "info": "get",
}


async def info(hub, ctx, domain: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.sec.get
    """
    return await hub.exec.vultr.util.query(ctx, "dns/soa_info", domain=domain)


async def update(
    hub, ctx, domain: str, nsprimary: str = None, email: str = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.sec.enable
    """
    kwargs = {}
    if nsprimary is not None:
        kwargs["nsprimary"] = nsprimary
    if email is not None:
        kwargs["email"] = email
    return await hub.exec.vultr.util.query(
        ctx, "dns/dnssec_enable", method="POST", domain=domain, **kwargs
    )
