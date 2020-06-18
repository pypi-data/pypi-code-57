import dataclasses
import copy
import datetime
import numpy as np
import copy

@dataclasses.dataclass
class AssetDict:
    # 战略配置参数
    hs300: float=0.0
    csi500: float=0.0
    gem: float=0.0
    sp500rmb: float=0.0
    national_debt: float=0.0
    gold: float=0.0
    credit_debt: float=0.0
    dax30rmb: float=0.0
    real_state: float=0.0
    oil: float=0.0
    n225rmb: float=0.0
    cash: float=0.0
    mmf: float=0.0

    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def copy(self):
        return copy.deepcopy(self)

    def isnan(self, v):
        return v is None or np.isnan(v)

@dataclasses.dataclass
class AssetWeight(AssetDict):

    def __post_init__(self):
        self.rebalance()

    def rebalance(self):
        _sum = 0.0
        for k, v in self.__dict__.items():
            assert round(v,8) >= 0, f'{k} has negative value'
            _sum += v
        assert _sum > 0, 'param sum value must be positive'
        # normalize, make sure change is correct
        for k, v in self.__dict__.items():
            self.__dict__[k] /= _sum
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v*100}%'
        s += '>'
        return s

@dataclasses.dataclass
class AssetPrice(AssetDict):

    def __post_init__(self):
        for k, v in self.__dict__.items():
            assert v is None or np.isnan(v) or round(v,8) >= 0, f'{k} has negative value: {v}'
        self.cash = 1 # cash price is always 1
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

@dataclasses.dataclass
class AssetTrade:

    index_id: str
    is_buy: bool
    mark_price: float
    submit_date: datetime.date
    amount: float=None
    volume: float=None
    trade_price: float=None
    commission: float=0.0
    trade_date: datetime.date=None

    def __post_init__(self):
        assert self.amount or self.volume, \
            f'both amount and volume are not valid (index){self.index_id} (vol){self.volume} (amt){self.amount}'

@dataclasses.dataclass
class AssetPosition(AssetDict):

    def __post_init__(self):
        for k, v in self.__dict__.items():
            assert round(v,8) >= 0, f'asset backtest {k} has negative value: {v}'
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def update(self, trd: AssetTrade):
        p = trd.trade_price if trd.trade_price else trd.mark_price
        v = trd.volume if trd.volume else trd.amount / p
        assert trd.is_buy or (self.__dict__[trd.index_id] - v > -1e-8), f'asset trade failed, (sell){v} (cur){self.__dict__[trd.index_id]} (trd){trd} (pos){self}'
        amt = trd.amount if trd.amount else v * p
        self.__dict__[trd.index_id] += v if trd.is_buy else -v
        self.cash += (-amt if trd.is_buy else amt) - trd.commission

@dataclasses.dataclass
class AssetValue(AssetDict):

    prices: AssetPrice=None
    positions: AssetPosition=None

    def __post_init__(self):
        for index_id, p in self.prices.__dict__.items():
            self.__dict__[index_id] = 0 if self.isnan(p) else p * self.positions.__dict__[index_id]
            # 不允许出现价格为空，但是仓位为正的情况
            assert not (self.isnan(p) and self.positions.__dict__[index_id] > 0), \
                f'price is nan but position is not zero... (index){index_id} (p){p} (pos){self.positions.__dict__[index_id]}'

    def sum(self):
        _sum = 0.0
        for k in AssetDict.__dataclass_fields__.keys():
            _sum += self.__dict__[k]
        return _sum

    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def get_weight(self):
        wgts = AssetWeight(cash=1)
        for index_id, p in self.prices.__dict__.items():
            wgts.__dict__[index_id] = self.__dict__[index_id]
        wgts.rebalance()
        return wgts
        

@dataclasses.dataclass
class FundTrade(AssetTrade):

    fund_id: str=None
    fund_unit_nav: float=None
    fund_unit_volume: float=None

@dataclasses.dataclass
class FundPosItem:

    fund_id: str            # 基金ID
    index_id: str           # 基金所属的大类资产
    volume: int             # 基金份额
    avg_cost: float=None    # 平均成本
    update_time: datetime.date=None # 更新时间

    def update(self, trade: FundTrade):
        assert self.fund_id == trade.fund_id, f'fund trade failed, self.fund_id != trade.fund_id: self.fund_id {self.fund_id}  trade.fund_id {trade.fund_id}'
        p = trade.trade_price if trade.trade_price else trade.mark_price
        v = trade.volume if trade.volume else trade.amount / p
        a = trade.amount if trade.amount else v * p
        assert trade.is_buy or (self.volume - v > -1e-8), f'fund trade failed, trade.volume {v} more than self.volume {self.volume}'
        vol_diff = v if trade.is_buy else -v
        amt_diff = a if trade.is_buy else -a
        volume = self.volume + vol_diff
        if trade.is_buy:
            amt = self.volume * self.avg_cost + amt_diff# 买入时平均成本摊销
            self.volume = volume
            self.avg_cost = amt / volume
        else:
            self.volume = volume
            if self.volume < 1e-8:# 清空仓位 平均成本为0
                self.avg_cost = 0
            else: #非清仓卖出 平均成本不变
                pass
        self.update_time = trade.trade_date
        assert self.volume >= -1e-8, f'fund backtest vol {self.volume} has negative value: '
        assert self.avg_cost >= -1e-8, f"fund avg cost can not be negative! (fund_id){self.fund_id} (update time){self.update_time}"
        return True
        
    def __repr__(self):
        return f'<{self.fund_id} (v){self.volume} (c){self.avg_cost}>'

@dataclasses.dataclass
class AssetTradeRateItem(AssetDict):
    def __post_init__(self):
        for k, v in self.__dict__.items():
            self.__dict__[k] = None if (v == 0 and k != 'mmf') else v

@dataclasses.dataclass
class AssetTradeParam:

    MinCountAmtDiff: float=0.001 # 少于总资产千分之一的资产Amount差异，不计在内
    MinActionAmtDiff: float=0.06 # 如果没有资产的偏离达到这个比例，那就不调仓
    EnableCommission: bool=True # 是否开启交易手续费计算
    PurchaseDiscount: float=0.15  # 大类资产的买入折扣
    RedeemDiscount: float=1.0    # 大类资产的卖出折扣
    AssetPurchaseRate: dict=None 
    AssetRedeemRate: dict=None

    def __post_init__(self):
        self.AssetPurchaseRate = self.AssetPurchaseRate or AssetTradeRateItem(csi500=0.011055, 
                                                                                gem=0.010488, 
                                                                                gold=0.001892, 
                                                                                hs300=0.011987, 
                                                                                national_debt=0.005438, 
                                                                                sp500rmb=0.008135,
                                                                                mmf=0).__dict__ #大类资产平均买入费率
        self.AssetRedeemRate = self.AssetRedeemRate or AssetTradeRateItem(csi500=0.002973, 
                                                                            gem=0.003407,
                                                                            gold=0.000755,
                                                                            hs300=0.004727,
                                                                            national_debt=0.000287,
                                                                            sp500rmb=0.003240,
                                                                            mmf=0).__dict__ #大类资产平均卖出费率
@dataclasses.dataclass
class FundTradeParam:

    MaxFundNumUnderAsset: float=3 # 同一个大类资产下基金最多数
    MinCountAmtDiff: float=0.0003 # 少于总资产万分之三的资产Amount差异，不做基金调仓处理
    MinActionAmtDiff: float=0.03 # 如果没有资产的基金市值偏离达到这个比例，那就不调仓
    EnableCommission: bool=True # 是否开启交易手续费计算
    PurchaseDiscount: float=0.15 # 基金的买入折扣
    RedeemDiscount: float=1.0    # 基金的卖出折扣

@dataclasses.dataclass
class TAAParam:

    HighThreshold: float=0.9    # 超过多少算作进入估值偏高的区域
    LowThreshold: float=0.1     # 低于多少算作进入估值偏低的区域
    HighMinus:    float=0.05    # 估值偏高时应该调低的占比
    LowPlus:      float=0.05    # 估值偏低是应该调高的占比
    HighStop:     float=0.5     # 进入估值偏高区后，什么时候算作退出
    LowStop:      float=0.5     # 进入估值偏低区后，什么时候算作退出
    TuneCash:     bool=False    # 默认taa调仓时，不调整cash
    ToMmf:        bool=True    # 默认taa加减仓不改变货基权重

@dataclasses.dataclass
class FundScoreParam:
    tag_type: int=1
    score_method: int=1
    is_full: int=1
    IndicatorTimespan: int=3    # 计算因子参数的时间要求

    def __repr__(self):
        return f'<fund_score_param tag_type={self.tag_type} score_method={self.score_method} is_full={self.is_full}'


@dataclasses.dataclass
class FAParam:

    MaxFundNumUnderAsset: float=3 # 同一个大类资产下基金最多数

@dataclasses.dataclass
class FundWeightItem:

    fund_id: str                # 基金ID
    index_id: str               # 基金所属的大类资产
    asset_wgt: float            # 资产的wgt
    fund_wgt_in_asset: float    # 基金在所属资产中的wgt
    fund_wgt: float=None        # 基金在整体组合中的wgt

    def __post_init__(self):
        self.fund_wgt = self.fund_wgt or self.asset_wgt * self.fund_wgt_in_asset

    def __repr__(self):
        return f'<{self.fund_id} (wgt){self.fund_wgt} (index){self.index_id} (iwgt){self.asset_wgt} (fwgt){self.fund_wgt_in_asset}>'

class FundWeight:

    def __init__(self):
        self.funds = {} # fund_id -> FundWeightItem

    def add(self, fund_wgt_item: FundWeightItem):
        self.funds[fund_wgt_item.fund_id] = fund_wgt_item
    
    def get_wgt(self, fund_id: str):
        fund_wgt_item = self.funds.get(fund_id)
        return fund_wgt_item.fund_wgt if fund_wgt_item else 0
    
    def get(self, fund_id: str):
        return self.funds.get(fund_id)

    def __repr__(self):
        s = f'<FW'
        for fund_id, wgt_item in self.funds.items():
            s += f' {wgt_item}'
        s += '>'
        return s

class FundPosition:

    def __init__(self, cash):
        self.funds = {} # fund_id -> FundPosItem
        self.index_fund_list = {} # index_id -> [fund_id]
        self.cash = cash

    def init_by_item_dict(self, cash, funds, index_fund_list):
        self.cash = cash
        self.funds = funds
        self.index_fund_list = index_fund_list
        return self

    def convert_to_item_dict(self):
        return {
            'cash': self.cash,
            'funds': {f: v.__dict__ for f, v in self.funds.items()},
            'index_fund_list': self.index_fund_list,
        }

    def calc_mv_n_w(self, 
                    fund_navs: dict, # fund_id -> nav(adjusted net value)
                    index_id=None): # filter: 只计算某个index_id
                
        mv = 0
        w_dic = {}
        for pos_item in self.funds.values():
            if index_id and pos_item.index_id != index_id:
                continue
            nav = fund_navs.get(pos_item.fund_id, np.nan)
            if np.isnan(nav):
                print('warning!!!! nav in nan')
            else:
                mv += nav * pos_item.volume
            w_dic[pos_item.fund_id] = nav * pos_item.volume
        mv = self.cash + mv
        w_dic = { f: w / mv for f, w in w_dic.items() }
        return mv, w_dic

    def calc_asset_position(self,
            fund_navs: dict,  # fund_id -> nav(adjusted net value)
            current_index_prices: AssetPrice,  # index_id -> nav(adjusted net value)
        ):
        mv_dic = {}
        for pos_item in self.funds.values():
            nav = fund_navs.get(pos_item.fund_id, np.nan)
            assert not np.isnan(nav), f'fund nav vol {pos_item.fund_id} has negative nav!'
            mv_dic[pos_item.index_id] = nav * pos_item.volume + mv_dic.get(pos_item.index_id, 0)
        vol_dic = {f: m / current_index_prices.__dict__.get(f) for f, m in mv_dic.items()}
        vol_dic['cash'] = self.cash
        return AssetPosition(**vol_dic)

    def get_volume(self, fund_id):
        item = self.funds.get(fund_id)
        if not item:
            return None
        return item.volume

    def get_funds(self, index_id):
        return self.index_fund_list.get(index_id, [])

    def add(self, fund_id, index_id, volume, avg_cost, update_time):
        pos_item = FundPosItem(fund_id=fund_id, index_id=index_id, volume=volume, avg_cost=avg_cost, update_time=update_time)
        self.funds[fund_id] = pos_item
        if index_id not in self.index_fund_list:
            self.index_fund_list[index_id] = []
        self.index_fund_list[index_id].append(fund_id)
        return pos_item

    def update(self, trade: FundTrade):
        assert isinstance(trade, FundTrade), 'only FundTrade is accepted here'
        pos_item = self.funds.get(trade.fund_id)
        if pos_item is None:
            assert trade.is_buy, "fund volume cannot be negative"
            pos_item = self.add(trade.fund_id, trade.index_id, 0, 0, trade.trade_date or trade.submit_date)
            
        if pos_item.update(trade):
            p = trade.trade_date if trade.trade_price else trade.mark_price
            amt = trade.amount if trade.amount else trade.volume * p
            cash_left = self.cash + (-amt if trade.is_buy else amt) - trade.commission 
            if cash_left <= -1e-8:
                print(f'cash negative alert: cancel order due to cash negative trade: {trade}, cash left if trade successed: {cash_left}')
                return False
            self.cash = cash_left
            return True
        else:
            return False

    def copy(self):
        n = FundPosition(cash=self.cash)
        n.funds = copy.deepcopy(self.funds)
        n.index_fund_list = copy.deepcopy(self.index_fund_list)
        return n

    def calc_weight(self, 
                fund_navs: dict, # fund_id -> nav(adjusted net value)
                index_id=None): # filter: 只计算某个index_id
        mv = 0
        for pos_item in self.funds.values():
            if index_id and pos_item.index_id != index_id:
                continue
            nav = fund_navs.get(pos_item.fund_id, np.nan)
            if np.isnan(nav):
                print('warning!!!! nav in nan')
            else:
                mv += nav * pos_item.volume
        return mv

    def __repr__(self):
        s = f'<FP cash={self.cash}'
        for fund_id, pos_item in self.funds.items():
            s += f' {pos_item}'
        s += '>'
        return s

class FundScoreHelper:
    ASSET_DICT = {
        '利率债' : 'national_debt',
        '美股大盘': 'sp500rmb',
        '德国大盘': 'dax30rmb',
        '信用债': 'credit_debt',
        '房地产': 'real_state',
        'A股大盘': 'hs300',
        '原油': 'oil',
        '黄金': 'gold',
        '创业板': 'gem',
        '日本大盘': 'n225rmb',
        'A股中盘': 'csi500',
    }
    TACTIC_ASSET_CONVERT = {
        '000300.XSHG': 'hs300',
        '000905.XSHG': 'csi500'
    }

    @staticmethod
    def keys():
        return FundScoreHelper.ASSET_DICT.keys()

    @staticmethod
    def get(index_id):
        for k, v in FundScoreHelper.ASSET_DICT.items():
            if v == index_id:
                return k
        return None
    
    @staticmethod
    def parse(tag_name):
        return FundScoreHelper.ASSET_DICT.get(tag_name)

class TaaTunerParam:
    index_id:            str
    IsTaaLowOnly:        bool=False
    IsTaaUpOnly:         bool=False
    param_list: list=[] # 调参范围列表
    POOL = {
        'gem'   : 'ps_pct',
        'hs300' : 'pe_pct',
        'csi500': 'pe_pct',
        'sp500rmb': 'pe_pct', 
    }
    PCT_PAIR = {
        'gem':'ps_ttm',
        'hs300':'pe_ttm',
        'csi500':'pe_ttm',
        'sp500rmb':'pe_ttm',
    }

@dataclasses.dataclass
class ScoreFilter:

    FilterIndexId:list = None
    CompanyHoldLimit:int = 95
    SizeBottom:int = 1e8
    SizeTop:int = 1e10
    
    def __post_init__(self):
        self.FilterIndexId = self.FilterIndexId or ['national_debt']

@dataclasses.dataclass
class ScorePenaltyParams:

    FilterYearIndex:list = None
    Penalty:float = -0.5 
    JudgeYearLength:float = 1.0

    def __post_init__(self):
        self.FilterYearIndex = self.FilterYearIndex or ['national_debt', 'csi500']

if __name__ == '__main__':
    a = AssetWeight(hs300=0.1, csi500=0.1, cash=0.8)
    print(a)