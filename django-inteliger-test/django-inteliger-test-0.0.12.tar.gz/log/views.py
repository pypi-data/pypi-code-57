from __future__ import annotations

from typing import Optional
import log.models


class LogMeta(type):
    _instance: Optional[Log] = None

    def __call__(self) -> Log:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Log(metaclass=LogMeta):
    def salvar(self, request=None, response=None):
        if request.META.get('REMOTE_ADDR') != '127.0.0.1':
            log.models.Log(
                status_code=response.status_code,
                reason_phrase=response.reason_phrase,
                metodo=request.method,
                ip=request.META.get('REMOTE_ADDR'),
                path=request.path,
                session_key=request.session.session_key
            ).save()
