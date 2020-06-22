from typing import Iterator, NamedTuple, List, Dict


class Telemetry(NamedTuple):
    timestamp: str
    value: str
    node: str
    metric: str
    subsystem: str = None


class NodeInfo(NamedTuple):
    """
    Represents the data held in the telemd info keys. The data is documented in https://github.com/edgerun/go-telemd

    * arch      the processor architecture (arm32, amd64, ...)
    * cpus      number of processors
    * ram       maximal available RAM in kilobytes
    * boot      UNIX timestamp of when the node was last booted
    * disk      The disk devices available for monitoring
    * net       The network devices available for monitoring
    * hostname  The real hostname
    """
    node: str
    data: Dict[str, str]


class TelemetrySubscriber:

    def __init__(self, rds, pattern=None) -> None:
        super().__init__()
        self.rds = rds
        self.pattern = pattern or 'telem/*'
        self.pubsub = None

    def run(self) -> Iterator[Telemetry]:
        self.pubsub = self.rds.pubsub()

        try:
            self.pubsub.psubscribe(self.pattern)

            for item in self.pubsub.listen():
                data = item['data']
                if type(data) == int:
                    continue
                channel = item['channel']
                timestamp, value = data.split(' ')
                parts = channel.split('/', maxsplit=3)
                # 'telem', node_id, metric [, subsystem]

                yield Telemetry(timestamp, value, *parts[1:])
        finally:
            self.pubsub.close()

    def close(self):
        if self.pubsub:
            self.pubsub.punsubscribe()
