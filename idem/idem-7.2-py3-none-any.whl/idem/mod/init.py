# Import python libs
import asyncio


async def modify(hub, name, chunk):
    """
    Take the given run name and low chunk, and allow state pluggins to modify
    the low chunk
    """
    for mod in hub.idem.mod:
        if mod.__name__ == "init":
            continue
        if hasattr(mod, "modify"):
            chunk = mod.modify(name, chunk)
            if asyncio.iscoroutine(chunk):
                chunk = await chunk
    return chunk
