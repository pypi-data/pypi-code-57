import aiofiles
import logging
import os
import yaml

log = logging.getLogger(__name__)


async def load_config(hub):
    """
    Return the grains set in the grains file
    """
    # TODO this comes from salt.salt.grains.extra.py, how do we want to locate static grains configs in hub.OPT?
    if "conf_file" not in hub.OPT:
        return

    if os.path.isdir(hub.OPT.conf_file):
        gfn = os.path.join(hub.OPT.conf_file, "grains")
    else:
        gfn = os.path.join(os.path.dirname(hub.OPT.conf_file), "grains")

    if os.path.isfile(gfn):
        log.debug("Loading static grains from %s", gfn)
        async with aiofiles.open(gfn, "rb") as fp_:
            try:
                # TODO? Load the yaml file with hub.rend
                hub.grains.GRAINS.update(yaml.safe_load(fp_))
            except Exception:  # pylint: disable=broad-except
                log.warning("Bad syntax in grains file! Skipping.")
