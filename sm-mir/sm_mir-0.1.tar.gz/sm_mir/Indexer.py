
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Problem import Problem


class Indexer(Problem):
    """ Indexer Class
    
        Provides Weight of Evidence Index a variable
        
    """
    
    def __init__(self, pType):
        
        Problem.__init__(self, pType)
        
        self.indexData = []
        
        
    def calculateWOE(self, colNum):
        
        df = pd.DataFrame(self.data).iloc[:,[self.outcome, colNum]]
        
        # non target as 1 - target
        
        nonTarget = 1-df[df.columns[0]] 
        df['nonTarget'] = nonTarget
        
        # group by 
        df2a = df.groupby([df.columns[1]]).sum()
        
        df2a['totTarget']=df.iloc[:,0].sum()
        df2a['totNonTarget']=df.iloc[:,2].sum()

        df2a['pctTarget'] = df2a[df2a.columns[0]]/df2a[df2a.columns[2]]
        df2a['pctNonTarget'] = df2a[df2a.columns[1]]/df2a[df2a.columns[3]]
        df2a['Index'] = df2a['pctTarget']/df2a['pctNonTarget']
        df2a['WoE'] = np.log(df2a.Index)
        df2a['IV'] = (df2a.pctTarget - df2a.pctNonTarget)*df2a.WoE 
        
        self.IndexData = df2a
        
        # also plot WoE
        
        plt.barh(df2a.index, df2a.WoE)        
        
        plt.ylabel(df2a.index.name)
        plt.xlabel('Weight Of Evidence')
        plt.title('Variable Indexing')
        
        plt.show()
        
        return self.IndexData