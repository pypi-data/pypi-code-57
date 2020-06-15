from typing import Any, Dict, List

import numpy as np

from sktmls.models.mls_model import MLSLightGBMModel


class SampleModel(MLSLightGBMModel):
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        if not self.model:
            return {"items": []}

        y = self.model.predict(np.array([x])).flatten().tolist()[0]

        if y < 0.2:
            return {"items": []}

        return {
            "items": [
                {
                    "id": "BNF0000001",
                    "name": "T건강습관",
                    "props": {"context_id": "context_discount_benefit", "score": y},
                    "type": "bnf_healthhabit",
                }
            ]
        }
