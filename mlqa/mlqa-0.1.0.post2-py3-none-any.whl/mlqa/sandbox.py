import checkers as ch
from identifiers import DiffChecker


dc = DiffChecker(logger='mylog.log')
import numpy as np
import pandas as pd
np.random.seed(123)
df = pd.DataFrame({'col1':np.random.normal(0, 0.1, 100), 'col2':np.random.normal(0, 1.0, 100)})
ch.qa_outliers(df, std=0.5, logger=dc.logger)

df1 = pd.DataFrame({'col1':[1, 2]*10, 'col2':[0, 4]*10})
df2 = pd.DataFrame({'col1':[1, 9]*10, 'col2':[0, -4]*10})
ch.qa_df_set([df1, df2], logger=dc.logger)

df1 = pd.DataFrame({'Gender': ['Male', 'Male', 'Female', 'Female'],'Weight': [200, 250, 100, 125]})
ch.qa_category_distribution_on_value(df1, 'Gender', {'Male':.5, 'Female':.5}, 'Weight', logger=dc.logger)


