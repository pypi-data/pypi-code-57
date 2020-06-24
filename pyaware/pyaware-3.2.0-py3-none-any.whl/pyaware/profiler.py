import asyncio
import yappi
import datetime
import threading
import pyaware.config
import logging

profile_lock = threading.Lock()

profile_path = pyaware.config.aware_path / "profiling"
try:
    profile_path.mkdir()
except FileExistsError:
    pass


def start():
    yappi.start()


def profile_dump():
    with profile_lock:
        yappi.stop()
        stats = yappi.get_func_stats()
        pstats = yappi.convert2pstats(stats)
        dump = pstats.dump_stats(
            profile_path / f"profiler_{datetime.datetime.utcnow().isoformat().replace('-', '_').replace(':', '_')}.pstat")
        yappi.clear_stats()
        logging.info(f"Dumped profile data")
        yappi.start()


async def profile_loop(interval):
    while True:
        await asyncio.sleep(interval)
        try:
            await asyncio.get_event_loop().run_in_executor(None, profile_dump)
        except BaseException as e:
            logging.exception(e)
