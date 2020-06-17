import numpy as np
import pandas as pd
from . import utils
from . import product


def get_instrument_info(date: str, instrument_id_list: list):
    instrument_df = pd.DataFrame(data=instrument_id_list, columns=['INSTRUMENT_ID'])
    instrument_df['INSTRUMENT_ID'] = instrument_df['INSTRUMENT_ID'].str.upper()
    instrument_df['PRODUCT_ID'] = instrument_df['INSTRUMENT_ID'].apply(utils.get_letter_part)

    product_df = product.get_product_info(date)
    rtn_df = pd.merge(instrument_df, product_df, how='left', on='PRODUCT_ID')
    
    assert not rtn_df.empty

    rtn_df['VALID'] = rtn_df.apply(func=__apply_func_is_valid_instrument, axis=1, date=date)
    rtn_df['LAST_TRADING_DAY'] = rtn_df.apply(func=__apply_func_parse_last_trading_day, axis=1, date=date)
    rtn_df.loc[~rtn_df['VALID'], 1:] = np.nan
    rtn_df.drop(columns=['VALID'], inplace=True)
    return rtn_df


def __apply_func_is_valid_instrument(x, date):
    begin_contract = x['BEGIN_CONTRACT']
    begin_date = x['BEGIN_DATE']
    end_contract = x['END_CONTRACT']
    end_date = x['END_DATE']
    instrument = x['INSTRUMENT_ID']
    if end_contract == 'CURRENT':
        equal_latter_instrument = utils.get_equal_latter_instrument(date_1=begin_date,
                                                                    date_2=date,
                                                                    instrument_id_1=begin_contract,
                                                                    instrument_id_2=instrument)
        return instrument == equal_latter_instrument
    else:
        equal_latter_instrument = utils.get_equal_latter_instrument(date_1=begin_date,
                                                                    date_2=date,
                                                                    instrument_id_1=begin_contract,
                                                                    instrument_id_2=instrument)
        equal_earlier_instrument = utils.get_equal_earlier_instrument(date_1=end_date,
                                                                      date_2=date,
                                                                      instrument_id_1=end_contract,
                                                                      instrument_id_2=instrument)
        return (instrument == equal_latter_instrument) and (instrument == equal_earlier_instrument)


def __apply_func_parse_last_trading_day(x, date):
    return utils.parse_last_trading_day(date, x['INSTRUMENT_ID'], x['LAST_TRADING_DAY_RULE'])
