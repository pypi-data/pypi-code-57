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
        idem exec vultr.dns.sec.info
    """
    return await hub.exec.vultr.util.query(ctx, "dns/dnssec_info", domain=domain)


async def enable(hub, ctx, domain: str, enable: bool) -> Tuple[bool, Dict[str, Any]]:
    """
    Create a domain name in DNS.

    CLI Example:

    .. code-block:: bash
        idem exec vultr.dns.sec.enable
    """
    return await hub.exec.vultr.util.query(
        ctx,
        "dns/dnssec_enable",
        method="POST",
        domain=domain,
        enable="yes" if enable else "no",
    )
