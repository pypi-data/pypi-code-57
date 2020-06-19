from typing import Iterable, List, MutableMapping, Optional

from prometheus_client import Metric

from .collector.feature import FeatureDistribution
from .collector.inference import InferenceDistribution
from .context import PredictionContext
from .frequency import FrequencyMetric


class LiveMetricRegistry:
    """An immutable collection of live metrics that can be incremented as new observations arrive.
    """

    def __init__(self, metrics: Iterable[Metric]):
        """Constructs live metrics based on the given baseline metrics.

        Live metrics are implemented using Prometheus ValueClass and may be incremented as new
        observations arrive. This is different from static metrics from collectors which don't
        change over time.

        Users may export the live metrics current values using the collect method.

        :param metrics: The collection of baseline metrics
        :type metrics: Iterable[Metric]
        """
        self._feature_metrics: MutableMapping[int, FrequencyMetric] = {}
        self._inference_metric: Optional[FrequencyMetric] = None
        for m in metrics:
            if FeatureDistribution.is_supported(m):
                index = FeatureDistribution.extract_index(m)
                frequency = FeatureDistribution.SUPPORTED[m.type].load_frequency(m)
                self._feature_metrics[index] = frequency
            elif InferenceDistribution.is_supported(m):
                self._inference_metric = InferenceDistribution.SUPPORTED[m.type].load_frequency(m)

    def collect(self) -> List[Metric]:
        """Converts live metrics to a static metrics using their current values in the registry.

        :return: The list of converted static metrics
        :rtype: List[Metric]
        """
        metrics = self._inference_metric.metric.collect() if self._inference_metric else []
        for _, v in self._feature_metrics.items():
            metrics += v.metric.collect()
        return metrics

    def observe(self, prediction: PredictionContext):
        """Updates live metrics in the registry with a new observation.

        :param prediction: The new observation
        :type prediction: PredictionContext
        """
        if self._inference_metric:
            self._inference_metric.observe(prediction.output)
        for i, v in enumerate(prediction.features):
            if i in self._feature_metrics:
                self._feature_metrics[i].observe(v)
