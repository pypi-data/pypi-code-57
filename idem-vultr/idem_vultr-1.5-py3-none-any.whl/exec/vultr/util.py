import httpx
from typing import Any, Dict, List, Tuple


def get(
    hub,
    value: str,
    ret_dict: Tuple[bool, Dict[str, Dict[str, Any]]],
    keys: List[str] = None,
) -> Dict[str, Any]:
    """
    Find a value within the return of a query
    """
    for v in ret_dict[1].values():
        for k in keys or v.keys():
            if v.get(k) == value:
                return v
    return {}


async def query(hub, ctx, path: str, method: str, **kwargs) -> httpx.Response:
    """
    Perform a query directly against the Vultr REST API
    """
    url = f"{ctx['acct']['api_url']}/{path}"

    headers = {
        "API-Key": ctx["acct"]["api_key"],
        "Accept": "application/json,text/plain",
    }
    if method == "GET":
        return await hub.exec.vultr.HTTPX.get(
            url, headers=headers, timeout=hub.OPT.idem.vultr_timeout, params=kwargs
        )
    elif method == "POST":
        return await hub.exec.vultr.HTTPX.post(
            url, headers=headers, timeout=hub.OPT.idem.vultr_timeout, data=kwargs
        )
    else:
        raise ValueError(f"Unknown url method '{method}'")
