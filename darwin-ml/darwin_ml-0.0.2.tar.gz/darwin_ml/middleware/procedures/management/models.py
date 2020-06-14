from typing import List

from addict import Dict as ADDICT
from jamboree.middleware.procedures import (ModelProcedureAbstract,
                                            ProcedureManagement)
from loguru import logger

from darwin_ml.middleware.procedures.models import (CremeProcedure,
                                                    SklearnProcedure)


class ModelProcedureManagement(ProcedureManagement):
    def __init__(self):
        super().__init__()
        self.required_attributes = ["model_type", "online"]
        
        # Don't forget to look at the 

    @property
    def allowed(self) -> List[str]:
        return ["sklearn", "creme"]

    
    def access(self, key):
        self.check_allowed(key)
        spec = {
            "sklearn": SklearnProcedure(),
            "creme": CremeProcedure(),
        }.get(key)
        return spec


if __name__ == "__main__":
    modelmgt = ModelProcedureManagement()
    print(modelmgt.access("sklearn"))
