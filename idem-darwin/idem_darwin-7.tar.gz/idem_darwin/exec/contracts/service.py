from typing import Any, Dict


async def call_sig_read_plist_file(hub, ctx) -> Dict[str, Any]:
    # TODO call the function and wrap the return in an imap
    # Are async contracts working now?  That's the main reason i haven't been using contracts
    return await hub.pop.data.imap(ctx.func())
