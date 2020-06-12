class ExchangeFields:
    

    def __init__(self, name, broker_fee=0.005, slippage=0.005):
        self.name:str=name
        self.broker_fee:float=broker_fee
        self.slippage:float=slippage
        self.verify()
    
    def verify(self):
        if not isinstance(self.name, str):
            raise TypeError("Exchange name needs to be a string")
        

        splintered = "".join(self.name.split(" "))
        if not bool(splintered):
            raise ValueError("Name cannot be empty")
        


class CurrencyFields:
    def __init__(self, base:str="USD", initial:float=100000.0):
        self.base = base
        self.initial = initial
        self.verify()
    
    def verify(self):
        if self.initial <= 0:
            raise ValueError("Starting amount cannot be zero or negative")
        if not isinstance(self.base, str):
            raise TypeError("Base currency needs to be a string")