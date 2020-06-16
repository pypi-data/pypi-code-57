
from .host import Host

import asyncio


def run_host():
	host = Host()
	loop = asyncio.get_event_loop()
	loop.create_task(host.run())
	loop.run_forever()
	loop.close()


if __name__ == "__main__":
	run_host()
