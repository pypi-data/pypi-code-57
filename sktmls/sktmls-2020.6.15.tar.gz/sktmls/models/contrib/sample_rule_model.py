from typing import Any, Dict, List

from sktmls.models.mls_model import MLSModelError, MLSRuleModel


class SampleRuleModel(MLSRuleModel):
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        age = x[0]
        app_use_traffic_youtube = x[1]
        svc_scrb_period = x[2]

        if len(self.features) != len(x):
            raise MLSModelError("The length of input is different from features on model.json")

        if svc_scrb_period < 100 or age < 19 or age > 60 or app_use_traffic_youtube < 10:
            return {"items": []}
        else:
            return {
                "items": [{"id": "NA00006538", "name": "T플랜 스페셜", "props": {"percent_rk": "0.5755"}, "type": "fee"}]
            }
