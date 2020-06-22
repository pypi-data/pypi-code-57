from typing import (
    Any,
    Mapping,
    Union,
)

import sentry_sdk

from ai.backend.common.plugin.monitor import AbstractErrorReporterPlugin
from . import __version__


class SentryErrorMonitor(AbstractErrorReporterPlugin):

    async def init(self) -> None:
        sentry_sdk.init(
            self.plugin_config['dsn'],
            release=__version__,
        )

    async def cleanup(self) -> None:
        pass

    async def capture_exception(
        self,
        exc_instance: Exception = None,
        context: Mapping[str, Any] = None,
    ) -> None:
        sentry_sdk.capture_exception(exc_instance)

    async def capture_message(self, msg: str) -> None:
        sentry_sdk.capture_message(msg)

    async def update_plugin_config(self, new_plugin_config: Mapping[str, Any]) -> None:
        self.plugin_config = self.new_plugin_config
        await self.cleanup()
        await self.init()
