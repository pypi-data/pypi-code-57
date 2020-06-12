from see137.parameters import Parameter
from jamboree.utils.core import consistent_hash

class StopLossParameter(Parameter):
    def __init__(self, complex_id:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comp_id = complex_id
        self.stop_loss_params = []
        # self.
    
    def extract_params(self, **kwargs):
        if len(self.stop_loss_params) == 0: return
        if len(kwargs) == 0: return
        for k, v in kwargs.items():
            if k in self.stop_loss_params:
                self.__dict__[k] = v
    
    
    def verify(self):
        pass

        