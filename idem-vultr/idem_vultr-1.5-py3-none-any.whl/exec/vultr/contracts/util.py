import asyncio
import enum
import httpx
import json
from typing import Any, Dict, List, Tuple


class HTTPResponseCode(enum.IntEnum):
    SUCCESS = 200
    INVALID_API_LOCATION = 400
    INVALID_API_KEY = 403
    INVALID_HTTP_METHOD = 405
    REQUEST_FAILED = 412
    INTERNAL_SERVER_ERROR = 500
    RATE_LIMIT_HIT = 503


def sig_get(
    hub,
    value: str or int,
    ret_dict: Tuple[bool, Dict[str, Dict[str, Any]]],
    keys: List[str],
) -> Dict[str, Any]:
    pass


def pre_get(hub, ctx):
    value = ctx.args[1]
    status, ret_dict = ctx.args[2]
    keys = ctx.args[3]

    assert isinstance(value, (int, str)), value
    assert isinstance(status, bool)
    assert isinstance(ret_dict, dict)
    # Make sure I'm working within a nested dict
    assert all(isinstance(v, dict) for v in ret_dict.values())
    assert isinstance(keys, list)


async def _nameid_to_id(hub, ctx, nameid: str or int, id_type: str) -> str or int:
    """
    :param nameid: A name or id from a vultr-api parameter
    :param id_type:
    :return: An ID usable by the vultr API
    """
    hub.log.debug(f"Turning nameid '{id_type}:{nameid}' into ID type")
    if id_type == "APPID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.app.list(ctx),
            ["APPID", "deploy_name", "name", "short_name"],
        ).get("APPID", nameid)
    elif id_type == "BACKUPID":
        return hub.exec.vultr.util.get(
            nameid, await hub.exec.vultr.os.list(ctx), ["BACKUPID", "description"]
        ).get("BACKUPID")
    elif id_type == "FIREWALLGROUPID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.firewall.group.list(ctx),
            ["FIREWALLGROUPID", "description"],
        ).get("FIREWALLGROUPID", nameid)
    elif id_type == "ISOID":
        iso_list = await hub.exec.vultr.iso.list(ctx, public=True)
        iso_list.update(await hub.exec.vultr.iso.list(ctx, public=False))
        return hub.exec.vultr.util.get(nameid, iso_list, ["ISOID", "filename"])["ISOID"]
    elif id_type == "METALPLANID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.plans.list(ctx, "baremetal"),
            ["METALPLANID", "name"],
        ).get("METALPLANID", nameid)
    elif id_type == "NETWORKID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.network.list(ctx),
            ["NETWORKID", "description", "v4_subnet"],
        ).get("NETWORKID", nameid)
    elif id_type == "OBJSTORECLUSTERID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.object_storage.cluster.list(ctx),
            ["OBJSTORECLUSTERID", "name"],
        ).get("OBJSTORECLUSTERID", nameid)
    elif id_type == "OSID":
        return hub.exec.vultr.util.get(
            nameid, await hub.exec.vultr.os.list(ctx), ["OSID", "name"]
        ).get("OSID", nameid)
    elif id_type == "RECORDID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.dns.record.list(ctx),
            ["RECORDID", "name", "data"],
        ).get("RECORDID", nameid)
    elif id_type == "SCRIPTID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.script.list(ctx),
            ["SCRIPTID", "script", "name"],
        ).get("SCRIPTID", nameid)
    elif id_type == "SNAPSHOTID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.snapshot.list(ctx),
            ["SNAPSHOTID", "description"],
        ).get("SNAPSHOTID", nameid)
    elif id_type == "SSHKEYID":
        return hub.exec.vultr.util.get(
            nameid,
            await hub.exec.vultr.ssh_key.list(ctx),
            ["SSHKEYID", "ssh_key", "name"],
        ).get("SSHKEYID")
    elif id_type == "VPSPLANID":
        return hub.exec.vultr.util.get(
            nameid, await hub.exec.vultr.plans.list(ctx), ["VPSPLANID", "name"]
        ).get("VPSPLANID", nameid)


def sig_query(
    hub, ctx, path: str, method: str, **kwargs
) -> Tuple[bool, Dict[str, Any]]:
    pass


def pre_query(hub, ctx):
    """
    Verify that the ctx has all the information it needs from the profile
    """
    func_ctx = ctx.kwargs.get("ctx", ctx.args[1])
    if not func_ctx["acct"]:
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("api_key"):
        raise ConnectionError("Incomplete profile information: missing api_key")


async def call_query(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    func_ctx = ctx.args[1]
    method = ctx.kwargs.pop("method", "GET").upper()
    kwargs = {}
    if "DCID" in func_ctx["acct"]:
        kwargs["DCID"] = func_ctx["acct"]["DCID"]
    if "SSHKEYID" in func_ctx["acct"]:
        kwargs["SSHKEYID"] = func_ctx["acct"]["SSHKEYID"]

    for key, value in ctx.kwargs.items():
        if key.startswith("raw_"):
            kwargs[key[4:]] = value
            continue

        if isinstance(value, bool):
            value = "yes" if value else "no"
        trimmed_key = key.replace("_", "").upper()
        if trimmed_key == "CLUSTER":
            trimmed_key = "OBJESTORECLUSTERID"
        else:
            if not trimmed_key.endswith("ID"):
                trimmed_key += "ID"
        if trimmed_key in ("GROUPID", "RULEID", "SUBID"):
            key = trimmed_key
        result = await _nameid_to_id(hub, func_ctx, value, trimmed_key)
        if result is None:
            kwargs[key] = value
        else:
            kwargs[trimmed_key] = result

    if kwargs:
        hub.log.debug(f"Making Vultr API call with params: {kwargs}")

    return await ctx.func(*ctx.args, method=method, **kwargs)


async def post_query(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    # This is the result of hub.exec.vultr.util.query
    ret: httpx.Response = ctx.ret

    # idem is is too efficient, don't hit up the API so fast
    if hub.OPT.idem.vultr_rate_limit > 0:
        await asyncio.sleep(1 / hub.OPT.idem.vultr_rate_limit)

    if ret.status_code != 200:
        hub.log.error(
            f"Vultr API request failed: {HTTPResponseCode(ret.status_code).name}({ret.status_code})"
        )
        return False, {"VULTR_API_REQUEST_STATUS": ret.text}

    try:
        ret_dict = json.loads(ret.text)
        if isinstance(ret_dict, list):
            ret_dict = {
                key: value for key, value in zip(range(len(ret_dict)), ret_dict)
            }
        return True, {key: ret_dict[key] for key in sorted(ret_dict)}
    except json.JSONDecodeError:
        return True, {}
