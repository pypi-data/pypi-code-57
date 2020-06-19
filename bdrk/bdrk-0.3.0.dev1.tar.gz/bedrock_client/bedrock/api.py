import os
from logging import Logger
from typing import TYPE_CHECKING, Any, List, Tuple

import requests

if TYPE_CHECKING:
    from pybdrk.bdrk.v1.api_client import ApiClient
    from pybdrk.bdrk.v1.configuration import Configuration
    from pybdrk.bdrk.v1.api.internal_api import InternalApi
    from pybdrk.bdrk.v1.models.run_metric_schema import RunMetricSchema
    from pybdrk.bdrk.v1.exceptions import ApiException
else:
    from bdrk.v1 import ApiClient, Configuration, InternalApi
    from bdrk.v1.models import RunMetricSchema
    from bdrk.v1.exceptions import ApiException


class BedrockApi:
    def __init__(self, logger: Logger):
        self.logger = logger

        self.has_api_settings = False
        if "BEDROCK_API_TOKEN" not in os.environ:
            return

        configuration = Configuration()
        configuration.host = os.environ.get("BEDROCK_API_DOMAIN", "https://api.bdrk.ai")
        # This is Bedrock Internal API token which will be auto-set in bedrock workload container
        configuration.api_key["X-Bedrock-Api-Token"] = os.environ["BEDROCK_API_TOKEN"]

        api_client = ApiClient(configuration)
        self.internal_api = InternalApi(api_client)
        self.has_api_settings = True

    def log_metric(self, key: str, value: Any):
        if not self.has_api_settings:
            self.logger.error("BEDROCK API TOKEN not found")
            return

        post_data = RunMetricSchema(key=key, value=value)
        try:
            response = self.internal_api.update_run_metrics(run_metric_schema=post_data)
            self.logger.info(f"Response: {response}")
        except ApiException as exc:
            self.logger.error(f"API Error: {exc}")

    @staticmethod
    def _compute_tn_fp_fn_tp(actual: List[int], prediction: List[int]) -> Tuple:
        """Compute TN, FP, FN, TP.

        :param List[int] actual: Actual values
        :param List[int] prediction: Predicted values
        :return Tuple: TN, FP, FN, TP
        """
        tp = sum([p == 1 and a == 1 for p, a in zip(prediction, actual)])
        tn = sum([p == 0 and a == 0 for p, a in zip(prediction, actual)])
        fp = sum([p == 1 and a == 0 for p, a in zip(prediction, actual)])
        fn = len(actual) - tp - tn - fp
        return tn, fp, fn, tp

    def log_chart_data(self, actual: List[int], probability: List[float]):
        """Log prediction data for creating run metrics charts.

        :param List[int] actual: Actual values; must be 0 or 1.
        :param List[float] probability: Predicted probabilities produced by model;
                                        must be between 0 and 1.
        """

        if not all(map(lambda v: v in [0, 1], actual)):
            self.logger.error(f"log_chart_data: actual values must be 0 or 1: {actual}")
            return

        if not all(map(lambda v: 0.0 <= v <= 1.0, probability)):
            self.logger.error(
                f"log_chart_data: probability values must be between 0 and 1: {probability}"
            )
            return

        if not len(actual) == len(probability):
            self.logger.error(
                f"log_chart_data: mismatch in length of actual ({len(actual)}) "
                f"vs probability ({len(probability)}) values"
            )
            return

        chart_data = []
        thresholds = (x * 0.05 for x in range(0, 20))  # 0 to 1 in 0.05 increments
        for threshold in thresholds:
            prediction = [int(p > threshold) for p in probability]

            tn, fp, fn, tp = BedrockApi._compute_tn_fp_fn_tp(actual, prediction)

            chart_data.append({"threshold": threshold, "tn": tn, "fp": fp, "fn": fn, "tp": tp})

        self.log_metric("binary_classifier_chart", chart_data)

    def _log_explainability_data(self, indv_data: bytes, global_data: bytes):
        try:
            data = self.internal_api.get_individual_explainability_data_upload_url()
            self.logger.debug(f"UploadURLData: {data}")
            resp = requests.put(data.url, data=indv_data, headers=data.headers)
            resp.raise_for_status()

            data = self.internal_api.get_global_explainability_data_upload_url()
            self.logger.debug(f"UploadURLData: {data}")
            resp = requests.put(data.url, data=global_data, headers=data.headers)
            resp.raise_for_status()
        except ApiException as exc:
            self.logger.error(f"API Error: {exc}")
        except requests.exceptions.HTTPError as exc:
            self.logger.error(f"Upload request error: {exc}")

    def _log_fairness_data(self, fairness_data: bytes):
        try:
            data = self.internal_api.get_fairness_metrics_upload_url()
            self.logger.debug(f"UploadURLData: {data}")
            resp = requests.put(data.url, data=fairness_data, headers=data.headers)
            resp.raise_for_status()
        except ApiException as exc:
            self.logger.error(f"API Error: {exc}")
        except requests.exceptions.HTTPError as exc:
            self.logger.error(f"Upload request error: {exc}")

    def _log_sample_data(self, sample_data: bytes):
        try:
            data = self.internal_api.get_explainability_sample_data_upload_url()
            self.logger.debug(f"UploadURLData: {data}")
            resp = requests.put(data.url, data=sample_data, headers=data.headers)
            resp.raise_for_status()
        except ApiException as exc:
            self.logger.error(f"API Error: {exc}")
        except requests.exceptions.HTTPError as exc:
            self.logger.error(f"Upload request error: {exc}")
