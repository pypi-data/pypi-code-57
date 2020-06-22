from typing import (
    Any,
    Mapping,
    Union,
)

import datadog

from ai.backend.common.plugin.monitor import AbstractStatReporterPlugin, StatMetricTypes


class DatadogStatsMonitor(AbstractStatReporterPlugin):

    async def init(self) -> None:
        datadog.initialize(api_key=self.plugin_config['datadog_api_key'],
                           app_key=self.plugin_config['datadog_app_key'])
        self.statsd = datadog.statsd
        self.statsd.__enter__()

    async def cleanup(self) -> None:
        self.statsd.__exit__(None, None, None)

    async def update_plugin_config(self, new_plugin_config: Mapping[str, Any]) -> None:
        self.plugin_config = self.new_plugin_config
        await self.cleanup()
        await self.init()

    async def report_metric(
        self,
        metric_type: StatMetricTypes,
        metric_name: str,
        value: Union[float, int] = None,
    ):
        if metric_type == StatMetricTypes.INCREMENT:
            self.statsd.increment(metric_name)
        elif metric_type == StatMetricTypes.GAUGE:
            self.statsd.gauge(metric_name, value)
        else:
            raise ValueError(f'Not supported report type: {metric_type}')
