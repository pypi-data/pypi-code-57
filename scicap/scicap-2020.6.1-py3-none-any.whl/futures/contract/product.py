import time
import numpy as np
import pandas as pd
from . import config

product_rule_df = pd.DataFrame(data=config.product_rule_data_list,
                               columns=config.product_rule_column_list)
today = time.strftime('%Y-%m-%d')
product_rule_df['END_DATE'] = product_rule_df['END_DATE'].str.replace('CURRENT', today)


def get_product_info(date: str):
    return product_rule_df[(product_rule_df['BEGIN_DATE'] <= date) & (date <= product_rule_df['END_DATE'])]
