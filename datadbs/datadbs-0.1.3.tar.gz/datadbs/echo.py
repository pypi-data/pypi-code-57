from .general import GeneralData

class Echo(GeneralData):
    def __init__(self,*args,**kwargs):
        super(Echo,self).__init__(*args,**kwargs)

    def manage_data(self, data):
        print(data)
        return str(data)
