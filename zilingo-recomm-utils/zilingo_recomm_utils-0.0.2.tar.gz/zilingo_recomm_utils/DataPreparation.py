
class DataPreparation():
    
    def __init__(self):
        pass
    
    def test_pd(self, file_path):
        import pandas as pd
        print(pd.__version__) 
        df = pd.read_csv(file_path)
        print((df).head(2))
        return df.shape