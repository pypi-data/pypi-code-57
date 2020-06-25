import gzip
import json
import logging
from typing import Any, Callable, Dict, List, Optional

import numpy as np
import pandas as pd

from bedrock_client.bedrock.api import BedrockApi

from . import ModelTypes
from . import explainability as exp
from . import fairness as fair


class ModelAnalyzer:
    def __init__(
        self,
        model,
        model_name: str,
        model_type: Optional[ModelTypes] = None,
        description: str = "",
    ):
        self.model = model
        self.model_type = model_type
        self.model_name = model_name
        self.desc = description
        self.predict: Optional[Callable] = None
        self.train_feat: Optional[pd.Dataframe] = None
        self.test_feat: Optional[pd.Dataframe] = None
        self.test_inf: Optional[pd.Dataframe] = None
        self.fconfig: Optional[Dict] = None
        self.test_lbs: Optional[pd.Dataframe] = None
        self.test_pred_lbs: Optional[pd.DataFrame] = None
        self.shap_values = None
        self.shap_base_values = None
        self.fairness_metrics = None
        self.api = BedrockApi(logging.getLogger(__name__))

    def predict_func(self, f: Callable[..., Any]):
        """Predict function to use with model
        """
        self.predict = f
        return self

    def train_features(self, df):
        """Used for calculating training feature distribution"""
        self.train_feat = df
        return self

    def test_features(self, df):
        """Test set data
        Used for calculating explanability and fairness metrics
        """
        self.test_feat = df
        return self

    def test_inference(self, df):
        """Inference done on test set data
        Used for calculating fairness metrics
        """
        self.test_inf = df
        return self

    def test_predicted_labels(self, df):
        """Inference done on test set data
        Used for calculating fairness metrics
        """
        self.test_pred_lbs = df
        return self

    def fairness_config(self, config):
        """Fairness configuration
        Should be a dictionary of the form

        {
            "FEATURE_NAME": {
                "unprivileged_attribute_values": ["privileged value"],
                "privileged_attribute_values": ["unprivileged value"]
            }
        }
        """
        self.fconfig = config
        return self

    def test_labels(self, labels):
        """Groundtruth labels of test set data
        Used for calculating fairness metrics
        """
        self.test_lbs = labels
        return self

    def analyze(self):
        # TODO: use metrics collector to collect distribution
        exp_results = exp.get_explainability(
            self.test_feat,
            model=self.model,
            model_type=self.model_type,
            predict_func=self.predict,
            bkgrd_data=self.train_feat,
        )
        self._log_sample_data(self.test_feat, self.test_inf, self.test_lbs)
        shap_values, base_values = exp_results["indv_data"]
        self.shap_values = shap_values
        self.base_values = base_values
        self._log_xai_data(shap_values, exp_results["global_data"], self.test_feat)
        if self.fconfig:
            if self.test_lbs is None:
                raise ValueError("Calculating fairness metrics requires labels data on test set")
            if self.test_inf is None:
                raise ValueError(
                    "Calculating fairness metrics requires inference produced from test set"
                )
            fairness_metrics = {}
            for attr, attr_vals in self.fconfig.items():
                fairness_metrics[attr] = fair.get_fairness(
                    self.test_feat,
                    self.test_pred_lbs,
                    self.test_lbs,
                    attr,
                    attr_vals["privileged_attribute_values"],
                    attr_vals["unprivileged_attribute_values"],
                )
            self.fairness_metrics = fairness_metrics
            self._log_fai_data(fairness_metrics)
        return shap_values, base_values, exp_results["global_data"], fairness_metrics

    def _log_xai_data(
        self,
        indv_xai_data: List[np.array],
        global_xai_data: List[np.array],
        train_feat: pd.DataFrame,
    ):
        if self.api.has_api_settings:
            indv_data = {}
            for i, output_cls in enumerate(indv_xai_data):
                indv_data[f"class {i}"] = pd.DataFrame(
                    data=output_cls, columns=train_feat.columns
                ).to_dict()
            indv_json = json.dumps(indv_data).encode("utf-8")
            indv_compressed_json = gzip.compress(indv_json)

            global_json = json.dumps(global_xai_data).encode("utf-8")
            global_compressed_json = gzip.compress(global_json)
            self.api._log_explainability_data(indv_compressed_json, global_compressed_json)

    def _log_fai_data(self, fai_data: Dict[str, pd.DataFrame]):
        if self.api.has_api_settings:
            output = {}
            for att_name, fairness_metrics in fai_data.items():
                fmeasures, confusion_matrix = fairness_metrics
                output[att_name] = fmeasures.to_dict()
                output[att_name]["confusion_matrix"] = confusion_matrix
            output_json = json.dumps(output).encode("utf-8")
            compressed_json = gzip.compress(output_json)
            self.api._log_fairness_data(compressed_json)

    def _log_sample_data(
        self,
        sample_data: pd.DataFrame,
        inf_data: Optional[np.array],
        sample_data_label: Optional[np.array],
    ):
        if self.api.has_api_settings:
            output = {}
            # sample Dataframe is converted to string first to
            # preserve NaN and Inf, which are not compliant JSON values
            features = sample_data.copy()
            output["features"] = features.applymap(str).to_dict()
            if sample_data_label is not None:
                output["ground_truth"] = sample_data_label.tolist()
            if inf_data is not None:
                output["inference_result"] = inf_data.tolist()
            output_json = json.dumps(output).encode("utf-8")
            compressed_json = gzip.compress(output_json)
            self.api._log_sample_data(compressed_json)
