# Import python libs
import asyncio


async def modify(hub, name, chunk):
    """
    Check the state containing the target func and call the aggregate
    function if present
    """
    state = chunk["state"]
    func = hub.idem.rules.init.get_func(name, chunk, "mod_aggregate")
    if func:
        chunk = func(name, chunk)
        if asyncio.iscoroutine(chunk):
            chunk = await chunk
    return chunk
