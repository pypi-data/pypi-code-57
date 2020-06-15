_status_waiting = 'waiting'
_status_scheduled = 'scheduled'
_status_running = 'running'
_status_succeded = 'succeded'
_status_failed = 'failed'


class TaskStatus(object):
    def __init__(self, status: str = _status_waiting):
        assert status in [_status_waiting, _status_scheduled, _status_running,
                          _status_succeded, _status_failed]
        self.status = status
        return

    def is_scheduled(self) -> bool:
        return self.status == _status_scheduled

    def advance(self):
        if self.status == _status_waiting:
            self.status = _status_scheduled
        elif self.status == _status_scheduled:
            self.status == _status_running
        elif self.status == _status_running:
            self.status == _status_succeded
        else:
            raise RuntimeError(f"Can not advance status 'f{self.status}'")
        return
