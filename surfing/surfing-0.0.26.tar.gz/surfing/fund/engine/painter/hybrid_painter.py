import pandas as pd
import numpy as np
import platform
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
CURRENT_PLATFORM = platform.system()
if CURRENT_PLATFORM == 'Darwin':
    mpl.rcParams['font.family'] = ['Heiti TC']
else:
    mpl.rcParams['font.family'] = ['STKaiti']

class HybridPainter(object):

    @staticmethod
    def plot_market_value(mv_df:pd.DataFrame, backtest_type:str, index_price:pd.DataFrame, saa_weight:dict, bk_stats:dict):
        index_df_raw = index_price.loc[mv_df.index[0]:mv_df.index[-1],]
        index_df = index_df_raw.copy().fillna(method='bfill')
        index_df = index_df / index_df.iloc[0]
        index_df['cash'] = 1
        w_l = []
        for idx, r in index_df_raw.iterrows():
            nan_asset = [k for k, v in r.to_dict().items() if np.isnan(v)]
            wgts = saa_weight.copy()
            for k in nan_asset:
                wgts[k] = 0
            s = sum([v  for k,v in wgts.items()])
            wgts = {k :v /s for k, v in wgts.items()}
            wgts['datetime'] = idx
            w_l.append(wgts)
        wgts_df = pd.DataFrame(w_l).set_index('datetime')
        mv_df['benchmark'] = (wgts_df * index_df).sum(axis = 1)
        mv_df = mv_df / mv_df.iloc[0]
        mv_df.plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title(f'{backtest_type} market value', fontsize=20)
        ar = round(bk_stats['annual_ret'],4)
        mdd = round(bk_stats['mdd'], 4)
        sharpe = round(bk_stats['sharpe'],4)
        pl.suptitle(f'annual_ret : {ar} mdd : {mdd} sharpe : {sharpe}',y=0.87,fontsize=17)
        plt.grid()

    @staticmethod
    def plot_asset_fund_mv_diff(asset_mv:pd.DataFrame, fund_mv:pd.DataFrame):
        asset_mv = asset_mv[['mv']]
        fund_mv = fund_mv[['mv']]
        asset_mv.columns = ['asset_mv']
        fund_mv.columns = ['fund_mv']
        check_diff = fund_mv.join(asset_mv)
        check_diff = check_diff / check_diff.iloc[0]
        check_diff['diff'] = 100 * (check_diff['fund_mv']  - check_diff['asset_mv']) / check_diff['asset_mv'] 
        check_diff[['fund_mv','asset_mv']].plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title('asset and fund market value ', fontsize=20)
        plt.grid()
        check_diff[['diff']].plot.line(figsize=(20,12),legend=False,fontsize = 17)
        l = pl.legend(loc='lower left',fontsize = 17)
        s = pl.title('asset and fund market value diff % ', fontsize=20)
        plt.grid()