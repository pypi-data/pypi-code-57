
from sqlalchemy import CHAR, Column, Integer, TEXT, BOOLEAN, text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT, DATETIME


class Base():
    _update_time = Column('_update_time', DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # 更新时间


# make this column at the end of every derived table
Base._update_time._creation_order = 9999
Base = declarative_base(cls=Base)


class WindFundInfo(Base):
    '''万徳基金信息表'''

    __tablename__ = 'wind_fund_info'

    wind_id = Column(CHAR(20), primary_key=True) # 基金代码
    desc_name = Column(CHAR(64)) # 基金名称
    full_name = Column(CHAR(255)) #基金全称
    start_date = Column(DATE) # 成立日期
    end_date = Column(DATE) # 结束日期
    benchmark = Column(CHAR(255)) # 业绩比较基准
    wind_class_1 = Column(CHAR(64)) # wind投资分类一级
    wind_class_2 = Column(CHAR(64)) # wind投资分类二级
    currency = Column(CHAR(20)) # 交易币种
    base_fund_id = Column(CHAR(20)) # 分级基金母基金代码
    is_structured = Column(TINYINT(1)) # 是否分级基金
    is_open = Column(TINYINT(1)) # 是否定期开放基金
    manager_id = Column(CHAR(255)) # 基金经理(历任)
    company_id = Column(CHAR(64)) # 基金公司


class RqStockPrice(Base):
    '''米筐股票不复权数据表'''

    __tablename__ = 'rq_stock_price'

    order_book_id = Column(CHAR(20), primary_key=True) # 股票ID
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 成交额
    volume = Column(DOUBLE(asdecimal=False)) # 成交量  不复权和后复权的交易量不同
    num_trades = Column(DOUBLE(asdecimal=False)) # 成交笔数

    __table_args__ = (
        Index('idx_rq_stock_price_datetime', 'datetime'),
    )


class RqStockPostPrice(Base):
    '''米筐股票后复权数据表'''

    __tablename__ = 'rq_stock_post_price'

    order_book_id = Column(CHAR(20), primary_key=True) # 股票ID
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 成交额
    volume = Column(DOUBLE(asdecimal=False)) # 成交量  不复权和后复权的交易量不同
    num_trades = Column(DOUBLE(asdecimal=False)) # 成交笔数

    __table_args__ = (
        Index('idx_rq_stock_post_price_datetime', 'datetime'),
    )


class RqFundNav(Base):
    '''米筐基金净值表'''

    __tablename__ = 'rq_fund_nav'

    order_book_id = Column(CHAR(10), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期

    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累计单位净值
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    subscribe_status = Column(CHAR(10)) # 申购状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    redeem_status = Column(CHAR(10)) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close

    __table_args__ = (
        Index('idx_rq_fund_nav_datetime', 'datetime'),
    )


class RqStockValuation(Base):
    '''
    股票每日估值
    LF, Last File 时效性最好
    LYR, Last Year Ratio 上市公司年报有审计要求，数据可靠性最高
    TTM, Trailing Twelve Months 时效性较好，滚动4个报告期计算，可避免某一期财报数据的偶然性
    '''

    __tablename__ = 'rq_stock_valuation'

    stock_id = Column(CHAR(20), primary_key=True) # 股票id
    datetime = Column(DATE, primary_key=True) # 日期

    pe_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市盈率lyr
    pe_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率ttm
    ep_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 盈市率lyr
    ep_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 盈市率ttm
    pcf_ratio_total_lyr = Column(DOUBLE(asdecimal=False)) # 市现率_总现金流lyr
    pcf_ratio_total_ttm = Column(DOUBLE(asdecimal=False)) # 市现率_总现金流ttm
    pcf_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市现率_经营lyr
    pcf_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市现率_经营ttm
    cfp_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 现金收益率lyr
    cfp_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 现金收益率ttm
    pb_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市净率lyr
    pb_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市净率ttm
    pb_ratio_lf = Column(DOUBLE(asdecimal=False)) # 市净率lf
    book_to_market_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 账面市值比lyr
    book_to_market_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 账面市值比ttm
    book_to_market_ratio_lf = Column(DOUBLE(asdecimal=False)) # 账面市值比lf
    dividend_yield_ttm = Column(DOUBLE(asdecimal=False)) # 股息率ttm
    peg_ratio_lyr = Column(DOUBLE(asdecimal=False)) # PEG值lyr
    peg_ratio_ttm = Column(DOUBLE(asdecimal=False)) # PEG值ttm
    ps_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市销率lyr
    ps_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市销率ttm
    sp_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 销售收益率lyr
    sp_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 销售收益率ttm
    market_cap = Column(DOUBLE(asdecimal=False)) # 总市值1
    market_cap_2 = Column(DOUBLE(asdecimal=False)) # 流通股总市值
    market_cap_3 = Column(DOUBLE(asdecimal=False)) # 总市值3
    a_share_market_val = Column(DOUBLE(asdecimal=False)) # A股市值
    a_share_market_val_in_circulation = Column(DOUBLE(asdecimal=False)) # 流通A股市值
    ev_lyr = Column(DOUBLE(asdecimal=False)) # 企业价值lyr
    ev_ttm = Column(DOUBLE(asdecimal=False)) # 企业价值ttm
    ev_lf = Column(DOUBLE(asdecimal=False)) # 企业价值lf
    ev_no_cash_lyr = Column(DOUBLE(asdecimal=False)) # 企业价值(不含货币资金)lyr
    ev_no_cash_ttm = Column(DOUBLE(asdecimal=False)) # 企业价值(不含货币资金)ttm
    ev_no_cash_lf = Column(DOUBLE(asdecimal=False)) # 企业价值(不含货币资金)lf
    ev_to_ebitda_lyr = Column(DOUBLE(asdecimal=False)) # 企业倍数lyr
    ev_to_ebitda_ttm = Column(DOUBLE(asdecimal=False)) # 企业倍数ttm
    ev_no_cash_to_ebit_lyr = Column(DOUBLE(asdecimal=False)) # 企业倍数(不含货币资金)lyr
    ev_no_cash_to_ebit_ttm = Column(DOUBLE(asdecimal=False)) # 企业倍数(不含货币资金)ttm

    __table_args__ = (
        Index('idx_rq_stock_valuation_datetime', 'datetime'),
    )


class RqFundIndicator(Base):
    '''米筐基金指标'''

    __tablename__ = 'rq_fund_indicator'

    order_book_id = Column(CHAR(10), primary_key=True) # 原始基金ID
    datetime = Column(DATE, primary_key=True) # 日期

    last_week_return = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    last_month_return = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    last_three_month_return = Column(DOUBLE(asdecimal=False)) # 近一季度收益率
    last_six_month_return = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    last_twelve_month_return = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    year_to_date_return = Column(DOUBLE(asdecimal=False)) # 今年以来收益率
    to_date_return = Column(DOUBLE(asdecimal=False)) # 成立至今收益率
    average_size = Column(DOUBLE(asdecimal=False)) # 平均规模
    annualized_returns = Column(DOUBLE(asdecimal=False)) # 成立以来年化收益率
    annualized_risk = Column(DOUBLE(asdecimal=False)) # 成立以来年化风险
    sharp_ratio = Column(DOUBLE(asdecimal=False)) # 成立以来夏普比率
    max_drop_down = Column(DOUBLE(asdecimal=False)) # 成立以来最大回撤
    information_ratio = Column(DOUBLE(asdecimal=False)) # 成立以来信息比率

    __table_args__ = (
        Index('idx_rq_fund_indicator_datetime', 'datetime'),
    )


class RqIndexPrice(Base):
    '''米筐指数数据'''

    __tablename__ = 'rq_index_price'

    order_book_id = Column(CHAR(20), primary_key=True) # 米筐代码
    datetime = Column(DATE, primary_key=True) # 日期

    high = Column(DOUBLE(asdecimal=False)) # 最高价
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量

    __table_args__ = (
        Index('idx_rq_index_price_datetime', 'datetime'),
    )


class RqIndexComponent(Base):
    '''米筐指数成分'''

    __tablename__ = 'rq_index_component'

    index_id = Column(CHAR(20), primary_key=True) # 米筐代码
    datetime = Column(DATE, primary_key=True) # 日期
    stock_list = Column(TEXT) # 股票列表


class EmIndexPrice(Base):
    '''Choice指数数据'''

    __tablename__ = 'em_index_price'
    em_id = Column(CHAR(20), primary_key=True) # Choice代码
    datetime = Column(DATE, primary_key=True) # 日期
    close = Column(DOUBLE(asdecimal=False)) # 收盘价


class FundFee(Base):
    '''基金费率'''

    __tablename__ = 'fund_fee'
    id = Column(Integer, primary_key=True)

    desc_name = Column(CHAR(32)) # 基金名称
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    fund_id = Column(CHAR(20)) # 基金id


class CxindexIndexPrice(Base):
    '''中证指数数据'''

    __tablename__ = 'cxindex_index_price'

    index_id = Column(CHAR(20), primary_key=True) # 指数名称
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    ret = Column(DOUBLE(asdecimal=False)) # 收益率

    __table_args__ = (
        Index('idx_cxindex_index_price_datetime', 'datetime'),
    )

class YahooIndexPrice(Base):
    '''雅虎指数数据'''

    __tablename__ = 'yahoo_index_price'

    index_id = Column(CHAR(20), primary_key=True) # 指数名称
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    ret = Column(DOUBLE(asdecimal=False)) # 收益率

    __table_args__ = (
        Index('idx_yahoo_index_price_datetime', 'datetime'),
    )

class CmIndexPrice(Base):
    '''汇率数据'''

    __tablename__ = 'cm_index_price'
    datetime = Column(DATE, primary_key=True) # 日期

    usd_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 美元人民币汇率中间价
    eur_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 欧元人民币汇率中间价
    jpy_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 日元人民币汇率中间价
    usd_cfets = Column(DOUBLE(asdecimal=False)) # 美元人民币市询价
    eur_cfets = Column(DOUBLE(asdecimal=False)) # 欧元人民币市询价
    jpy_cfets = Column(DOUBLE(asdecimal=False)) # 日元人民币市询价


class FundRating(Base):
    '''基金评级'''

    __tablename__ = 'fund_rating'

    order_book_id = Column(CHAR(10), primary_key=True) # 米筐基金id
    datetime = Column(DATE, primary_key=True) # 日期

    zs = Column(DOUBLE(asdecimal=False)) # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False)) # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False)) # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False)) # 济安金信评级


class RqIndexWeight(Base):
    '''指数成分权重'''

    __tablename__ = 'rq_index_weight'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期

    weight_list = Column(TEXT) # 权重列表 json 格式str 两者顺位对应
    stock_list = Column(TEXT) # 股票列表 json 格式str 两者顺位对应

    __table_args__ = (
        Index('idx_rq_index_weight_datetime', 'datetime'),
    )


class RqStockFinFac(Base):
    '''米筐股票财务因子'''

    __tablename__ = 'rq_stock_fin_fac'

    stock_id = Column(CHAR(20), primary_key=True) # 股票
    datetime = Column(DATE, primary_key=True) # 日期

    return_on_equity_ttm = Column(DOUBLE(asdecimal=False))  # 净资产收益率ttm
    market_cap_3 = Column(DOUBLE(asdecimal=False))  # 总市值
    net_profit_parent_company_ttm_0 = Column(DOUBLE(asdecimal=False))  # 归母公司净利润TTM
    net_profit_ttm_0 = Column(DOUBLE(asdecimal=False))  # 最近一期净利润TTM
    net_profit_ttm_1 = Column(DOUBLE(asdecimal=False))  # 最近一期上一期的净利润TTM
    basic_earnings_per_share_lyr_0 = Column(DOUBLE(asdecimal=False))  # 最近一期年报基本每股收益LYR
    basic_earnings_per_share_lyr_1 = Column(DOUBLE(asdecimal=False))  # 最近一期上一期年报基本每股收益LYR
    basic_earnings_per_share_lyr_2 = Column(DOUBLE(asdecimal=False))  # 最近一期上上期年报基本每股收益LYR
    equity_parent_company_mrq_0 = Column(DOUBLE(asdecimal=False))  # 最近一期单季度归母公司所有者权益合计


class RqFundSize(Base):
    '''米筐基金最新规模'''

    __tablename__ = 'rq_fund_size'

    order_book_id = Column(CHAR(10), primary_key=True) # 米筐基金id
    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模


class StockInfo(Base):
    '''股票信息表'''

    __tablename__ = 'rq_stock_info'

    stock_id = Column(CHAR(20), primary_key=True) # 股票ID
    rq_id = Column(CHAR(20)) # 米筐ID


class TradingDayList(Base):
    '''交易日列表'''

    __tablename__ = 'rq_trading_day_list'
    datetime = Column(DATE, primary_key=True)


class IndexValPct(Base):
    '''指数估值'''

    __tablename__ = 'index_valpct'

    index_id = Column(CHAR(20), primary_key=True) # 指数
    datetime = Column(DATE, primary_key=True) # 日期

    pe_ttm  = Column(DOUBLE(asdecimal=False)) # pe
    pe_pct = Column(DOUBLE(asdecimal=False)) # pe 百分位
    pb =  Column(DOUBLE(asdecimal=False)) # pb
    pb_pct =  Column(DOUBLE(asdecimal=False)) # pb pct


class EmFundNav(Base):
    '''Choice基金净值表'''

    __tablename__ = 'em_fund_nav'
    CODES = Column(CHAR(10), primary_key=True) # 合约代码
    DATES = Column(DATE, primary_key=True) # 日期

    ORIGINALUNIT = Column(DOUBLE(asdecimal=False)) # 单位净值
    ORIGINALNAVACCUM = Column(DOUBLE(asdecimal=False)) # 累计单位净值
    ADJUSTEDNAV = Column(DOUBLE(asdecimal=False)) # 复权净值
    UNITYIELD10K = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    YIELDOF7DAYS = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）

    __table_args__ = (
        Index('idx_em_fund_nav_datetime', 'DATES'),
    )


class EmFundScale(Base):
    '''
    Choice基金状态表
    包含基金规模，基金申赎状态
    '''

    __tablename__ = 'em_fund_scale'
    CODES = Column(CHAR(10), primary_key=True) # 合约代码
    DATES = Column(DATE, primary_key=True) # 日期

    FUNDSCALE = Column(DOUBLE(asdecimal=False)) # 基金规模


class EMIndexPct(Base):
    '''Choice指数估值数据'''

    __tablename__ = 'em_index_pct'
    index_id = Column(CHAR(20), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期
    pe_ttm = Column(DOUBLE(asdecimal=False)) # pe
    pe_pct = Column(DOUBLE(asdecimal=False)) # pe 百分位


class EmStockPrice(Base):
    '''Choice股票不复权数据表'''

    __tablename__ = 'em_stock_price'

    CODES = Column('stock_id', CHAR(10), primary_key=True) # EM股票ID
    DATES = Column('datetime', DATE, primary_key=True) # 日期
    OPEN = Column('open', DOUBLE(asdecimal=False), nullable=False) # 开盘价
    CLOSE = Column('close', DOUBLE(asdecimal=False), nullable=False) # 收盘价
    HIGH = Column('high', DOUBLE(asdecimal=False), nullable=False) # 最高价
    LOW = Column('low', DOUBLE(asdecimal=False), nullable=False) # 最低价
    PRECLOSE = Column('pre_close', DOUBLE(asdecimal=False), nullable=False) # 前收盘价
    AVERAGE = Column('average', DOUBLE(asdecimal=False), server_default=text("0")) # 均价
    AMOUNT = Column('amount', DOUBLE(asdecimal=False), server_default=text('0')) # 成交额
    VOLUME = Column('volume', DOUBLE(asdecimal=False), server_default=text('0')) # 成交量  不复权和后复权的交易量不同
    TURN = Column('turn', DOUBLE(asdecimal=False), server_default=text('0')) # 换手率
    TRADESTATUS = Column('trade_status', CHAR(20), nullable=False) # 交易状态
    TNUM = Column('t_num', DOUBLE(asdecimal=False), server_default=text('0')) # 成交笔数
    BUYVOL = Column('buy_vol', DOUBLE(asdecimal=False), server_default=text('0')) # 内盘成交量
    SELLVOL = Column('sell_vol', DOUBLE(asdecimal=False), server_default=text('0')) # 外盘成交量

    __table_args__ = (
        Index('idx_em_stock_price_datetime', 'datetime'),
    )

class EmStockPostPrice(Base):
    '''Choice股票后复权数据表'''

    __tablename__ = 'em_stock_post_price'

    CODES = Column('stock_id', CHAR(10), primary_key=True) # EM股票ID
    DATES = Column('datetime', DATE, primary_key=True) # 日期
    OPEN = Column('open', DOUBLE(asdecimal=False), nullable=False) # 开盘价
    CLOSE = Column('close', DOUBLE(asdecimal=False), nullable=False) # 收盘价
    HIGH = Column('high', DOUBLE(asdecimal=False), nullable=False) # 最高价
    LOW = Column('low', DOUBLE(asdecimal=False), nullable=False) # 最低价
    PRECLOSE = Column('pre_close', DOUBLE(asdecimal=False), nullable=False) # 前收盘价
    AVERAGE = Column('average', DOUBLE(asdecimal=False), server_default=text("0")) # 均价
    AMOUNT = Column('amount', DOUBLE(asdecimal=False), server_default=text('0')) # 成交额
    VOLUME = Column('volume', DOUBLE(asdecimal=False), server_default=text('0')) # 成交量
    TRADESTATUS = Column('trade_status', CHAR(20), nullable=False) # 交易状态
    TAFACTOR = Column('tafactor', DOUBLE(asdecimal=False), server_default=text("0")) # 复权因子（后）

    __table_args__ = (
        Index('idx_em_stock_post_price_datetime', 'datetime'),
    )

class EmStockDailyInfo(Base):
    '''Choice股票每日更新'''

    __tablename__ = 'em_stock_daily_info'

    CODES = Column("stock_id", CHAR(10), primary_key=True) # EM股票ID
    DATES = Column('datetime', DATE, primary_key=True) # 日期
    TOTALSHARE = Column("total_share", DOUBLE(asdecimal=False), nullable=False) # 总股本
    HOLDFROZENAMTACCUMRATIO = Column('hold_frozen_amt_accum_ratio', DOUBLE(asdecimal=False))  # 控股股东累计质押数量占持股比例
    ASSETMRQ = Column('asset_mrq', DOUBLE(asdecimal=False))  # 资产总计(MRQ)
    EQUITYMRQ = Column('equity_mrq', DOUBLE(asdecimal=False))  # 归属母公司股东的权益(MRQ)(净资产)
    PETTMDEDUCTED = Column('pe_ttm_deducted', DOUBLE(asdecimal=False))  # 市盈率TTM(扣除非经常性损益)
    PBLYRN = Column('pb_lyr_n', DOUBLE(asdecimal=False))  # 市净率(PB，LYR)(按公告日)
    PSTTM = Column('ps_ttm', DOUBLE(asdecimal=False))  # 市销率(PS，TTM)
    AHOLDER = Column('a_holder', TEXT)  # 实际控制人
    ESTPEG = Column('est_peg', DOUBLE(asdecimal=False)) # 预测PEG(最近一年)

    __table_args__ = (
        Index('idx_em_stock_daily_info_datetime', 'datetime'),
    )

class EmStockInfo(Base):
    '''Choice股票信息表'''

    __tablename__ = 'em_stock_info'

    CODES = Column("stock_id", CHAR(10), primary_key=True) # EM股票ID
    NAME = Column("name", TEXT, nullable=False) # 股票简称
    ENGNAME = Column("eng_name", TEXT) # 证券英文简称
    COMPNAME = Column("comp_name", TEXT, nullable=False) # 公司中文名称
    COMPNAMEENG = Column("comp_name_eng", TEXT) # 公司英文名称
    LISTDATE = Column("list_date", DATE, nullable=False) # 首发上市日期
    FINPURCHORNOT = Column("fin_purch_ornot", BOOLEAN, nullable=False) # 是否属于融资标的
    FINSELLORNOT = Column("fin_sell_ornot", BOOLEAN, nullable=False) # 是否属于融券标的
    STOHSTOCKCONNECTEDORNOT = Column("stoh_stock_connected_ornot", BOOLEAN, nullable=False) # 是否属于沪股通标的
    SHENGUTONGTARGET = Column("shengutong_target", BOOLEAN, nullable=False) # 是否属于深股通标的
    BLEMINDCODE = Column("bl_em_ind_code", CHAR(40), nullable=False) # 所属东财行业指数代码
    BLSWSINDCODE = Column("bl_sws_ind_code", CHAR(40), nullable=False) # 所属申万行业指数代码
    SW2014CODE = Column("sw_2014_code", CHAR(40), nullable=False) # 所属申万行业代码
    EMINDCODE2016 = Column("em_ind_code_2016", CHAR(40), nullable=False) # 所属东财行业(2016)代码
    CITICCODE2020 = Column("citic_code_2020", CHAR(40), nullable=False) # 所属中信行业代码(2020)
    BLCSRCINDCODE = Column("bl_csrc_ind_code", CHAR(32), nullable=False) # 所属证监会行业指数代码
    CSRCCODENEW = Column("csrc_code_new", CHAR(16), nullable=False) # 所属证监会行业(新)代码
    CSINDCODE2016 = Column("cs_ind_code_2016", CHAR(32), nullable=False) # 所属中证行业(2016)代码
    GICSCODE = Column("gics_code", CHAR(32), nullable=False) # 所属GICS行业代码


class EmStockFinFac(Base):
    '''Choice股票财务因子 '''

    __tablename__ = 'em_stock_fin_fac'

    CODES = Column("stock_id", CHAR(10), primary_key=True) # EM股票id
    DATES = Column("datetime", DATE, primary_key=True) # 日期
    EBIT = Column("ebit", DOUBLE(asdecimal=False)) # 息税前利润EBIT(反推法)
    EBITDA = Column("ebitda", DOUBLE(asdecimal=False)) # 息税折旧摊销前利润EBITDA(反推法)
    EXTRAORDINARY = Column("extra_ordinary", DOUBLE(asdecimal=False)) # 非经常性损益
    LOWERDIANDNI = Column("lower_diandni", DOUBLE(asdecimal=False)) # 扣非前后净利润孰低
    GROSSMARGIN = Column("gross_margin", DOUBLE(asdecimal=False)) # 毛利
    OPERATEINCOME = Column("operate_income", DOUBLE(asdecimal=False)) # 经营活动净收益
    INVESTINCOME = Column("invest_income", DOUBLE(asdecimal=False)) # 价值变动净收益
    EBITDRIVE = Column("ebit_drive", DOUBLE(asdecimal=False)) # 息税前利润EBIT(正推法)
    TOTALCAPITAL = Column("total_capital", DOUBLE(asdecimal=False)) # 全部投入资本
    WORKINGCAPITAL = Column("working_capital", DOUBLE(asdecimal=False)) # 营运资本
    NETWORKINGCAPITAL = Column("networking_capital", DOUBLE(asdecimal=False)) # 净营运资本
    TANGIBLEASSET = Column("tangible_asset", DOUBLE(asdecimal=False)) # 有形资产
    RETAINED = Column("retained", DOUBLE(asdecimal=False)) # 留存收益
    INTERESTLIBILITY = Column("interest_liability", DOUBLE(asdecimal=False)) # 带息负债
    NETLIBILITY = Column("net_liability", DOUBLE(asdecimal=False)) # 净债务
    EXINTERESTCL = Column("ex_interest_cl", DOUBLE(asdecimal=False)) # 无息流动负债
    EXINTERESTNCL = Column("ex_interest_ncl", DOUBLE(asdecimal=False)) # 无息非流动负债
    FCFF = Column("fcff", DOUBLE(asdecimal=False)) # 企业自由现金流量FCFF
    FCFE = Column("fcfe", DOUBLE(asdecimal=False)) # 股权自由现金流量FCFE
    DA = Column("da", DOUBLE(asdecimal=False)) # 当期计提折旧与摊销
    FCFFDRIVE = Column("fcff_drive", DOUBLE(asdecimal=False)) # 企业自由现金流量FCFF(正推法)
    DEDUCTEDINCOME_BA = Column("deducted_income_ba", DOUBLE(asdecimal=False)) # 归属于上市公司股东的扣除非经常性损益后的净利润(调整前)
    DEDUCTEDINCOME_AA = Column("deducted_income_aa", DOUBLE(asdecimal=False)) # 归属于上市公司股东的扣除非经常性损益后的净利润(调整后)
    GRTTMR = Column("gr_ttmr", DOUBLE(asdecimal=False)) # 营业总收入TTM(报告期)
    GCTTMR = Column("gc_ttmr", DOUBLE(asdecimal=False)) # 营业总成本TTM(报告期)
    ORTTMR = Column("or_ttmr", DOUBLE(asdecimal=False)) # 营业收入TTM(报告期)
    OCTTMR = Column("oc_ttmr", DOUBLE(asdecimal=False)) # 营业成本非金融类TTM(报告期)
    EXPENSETTMR = Column("expense_ttmr", DOUBLE(asdecimal=False)) # 营业支出金融类TTM(报告期)
    GROSSMARGINTTMR = Column("gross_margin_ttmr", DOUBLE(asdecimal=False)) # 毛利TTM(报告期)
    OPERATEEXPENSETTMR = Column("operate_expense_ttmr", DOUBLE(asdecimal=False)) # 销售费用TTM(报告期)
    ADMINEXPENSETTMR = Column("admin_expense_ttmr", DOUBLE(asdecimal=False)) # 管理费用TTM(报告期)
    FINAEXPENSETTMR = Column("fina_expense_ttmr", DOUBLE(asdecimal=False)) # 财务费用TTM(报告期)
    IMPAIRMENTTTMR = Column("impairment_ttmr", DOUBLE(asdecimal=False)) # 资产减值损失TTM(报告期)
    OPERATEINCOMETTMR = Column("operate_income_ttmr", DOUBLE(asdecimal=False)) # 经营活动净收益TTM(报告期)
    INVESTINCOMETTMR = Column("invest_income_ttmr", DOUBLE(asdecimal=False)) # 价值变动净收益TTM(报告期)
    OPTTMR = Column("op_ttmr", DOUBLE(asdecimal=False)) # 营业利润TTM(报告期)
    NONOPERATEPROFITTTMR = Column("non_operate_profi_ttmr", DOUBLE(asdecimal=False)) # 营业外收支净额TTM(报告期)
    EBITTTMR = Column("ebit_ttmr", DOUBLE(asdecimal=False)) # 息税前利润TTM(报告期)
    EBTTTMR = Column("ebt_ttmr", DOUBLE(asdecimal=False)) # 利润总额TTM(报告期)
    TAXTTMR = Column("tax_ttmr", DOUBLE(asdecimal=False)) # 所得税TTM(报告期)
    PNITTMR = Column("pni_ttmr", DOUBLE(asdecimal=False)) # 归属母公司股东的净利润TTM(报告期)
    KCFJCXSYJLRTTMR = Column("kcfjcxsyjlr_ttmr", DOUBLE(asdecimal=False)) # 扣除非经常性损益净利润TTM(报告期)
    NPTTMRP = Column("np_ttmrp", DOUBLE(asdecimal=False)) # 净利润TTM(报告期)
    FVVPALRP = Column("fvvpal_rp", DOUBLE(asdecimal=False)) # 公允价值变动损益TTM(报告期)
    IRTTMRP = Column("irtt_mrp", DOUBLE(asdecimal=False)) # 投资收益TTM(报告期)
    IITTMFJVAJVRP = Column("iittmfjvajv_rp", DOUBLE(asdecimal=False)) # 对联营企业和合营企业的投资收益TTM(报告期)
    BTAATTMRP = Column("btaa_ttmrp", DOUBLE(asdecimal=False)) # 营业税金及附加TTM(报告期)
    SALESCASHINTTMR = Column("sales_cashin_ttmr", DOUBLE(asdecimal=False)) # 销售商品提供劳务收到的现金TTM(报告期)
    CFOTTMR = Column("cfo_ttmr", DOUBLE(asdecimal=False)) # 经营活动现金净流量TTM(报告期)
    CFITTMR = Column("cfi_ttmr", DOUBLE(asdecimal=False)) # 投资活动现金净流量TTM(报告期)
    CFFTTMR = Column("cff_ttmr", DOUBLE(asdecimal=False)) # 筹资活动现金净流量TTM(报告期)
    CFTTMR = Column("cf_ttmr", DOUBLE(asdecimal=False)) # 现金净流量TTM(报告期)
    CAPEXR = Column("cap_exr", DOUBLE(asdecimal=False)) # 资本支出TTM(报告期)
    PERFORMANCEEXPRESSPARENTNI = Column('performance_express_parent_ni', DOUBLE(asdecimal=False)) # 业绩快报.归属母公司股东的净利润
    MBSALESCONS = Column('mb_sales_cons', TEXT) # 主营收入构成(按行业)
    MBSALESCONS_P = Column('mb_sales_cons_p', TEXT) # 主营收入构成(按产品)
    GPMARGIN = Column('gp_margin', DOUBLE(asdecimal=False)) # 销售毛利率
    NPMARGIN = Column('np_margin', DOUBLE(asdecimal=False)) # 销售净利率(营业收入/净利润)
    EXPENSETOOR = Column('expense_toor', DOUBLE(asdecimal=False)) # 销售期间费用率
    INVTURNRATIO = Column('inv_turn_ratio', DOUBLE(asdecimal=False)) # 存货周转率
    ARTURNRATIO = Column('ar_turn_ratio', DOUBLE(asdecimal=False)) # 应收账款周转率(含应收票据)
    ROEAVG = Column('roe_avg', DOUBLE(asdecimal=False)) # 净资产收益率ROE(平均)
    ROEWA = Column('roe_wa', DOUBLE(asdecimal=False)) # 净资产收益率ROE(加权)
    EPSBASIC = Column('eps_basic', DOUBLE(asdecimal=False)) # 每股收益EPS(基本)
    EPSDILUTED = Column('eps_diluted', DOUBLE(asdecimal=False)) # 每股收益EPS(稀释)
    BPS = Column('bps', DOUBLE(asdecimal=False)) # 每股净资产
    BALANCESTATEMENT_25 = Column('balance_statement_25', DOUBLE(asdecimal=False)) # 流动资产合计
    BALANCESTATEMENT_46 = Column('balance_statement_46', DOUBLE(asdecimal=False)) # 非流动资产合计
    BALANCESTATEMENT_93 = Column('balance_statement_93', DOUBLE(asdecimal=False)) # 流动负债合计
    BALANCESTATEMENT_103 = Column('balance_statement_103', DOUBLE(asdecimal=False)) # 非流动负债合计
    BALANCESTATEMENT_141 = Column('balance_statement_141', DOUBLE(asdecimal=False)) # 股东权益合计
    BALANCESTATEMENT_140 = Column('balance_statement_140', DOUBLE(asdecimal=False)) # 归属于母公司股东权益合计
    BALANCESTATEMENT_195 = Column('balance_statement_195', DOUBLE(asdecimal=False)) # 其他权益工具
    INCOMESTATEMENT_9 = Column('income_statement_9', DOUBLE(asdecimal=False)) # 营业收入
    INCOMESTATEMENT_48 = Column('income_statement_48', DOUBLE(asdecimal=False)) # 营业利润
    INCOMESTATEMENT_60 = Column('income_statement_60', DOUBLE(asdecimal=False)) # 净利润
    INCOMESTATEMENT_61 = Column('income_statement_61', DOUBLE(asdecimal=False)) # 归属于母公司股东的净利润
    INCOMESTATEMENT_85 = Column('income_statement_85', DOUBLE(asdecimal=False)) # 其他业务收入
    INCOMESTATEMENT_127 = Column('income_statement_127', DOUBLE(asdecimal=False)) # 利息费用
    INCOMESTATEMENT_14 = Column('income_statement_14', DOUBLE(asdecimal=False)) # 财务费用
    CASHFLOWSTATEMENT_39 = Column('cashflow_statement_39', DOUBLE(asdecimal=False)) # 经营活动产生的现金流量净额
    CASHFLOWSTATEMENT_59 = Column('cashflow_statement_59', DOUBLE(asdecimal=False)) # 投资活动产生的现金流量净额
    CASHFLOWSTATEMENT_77 = Column('cashflow_statement_77', DOUBLE(asdecimal=False)) # 筹资活动产生的现金流量净额
    CASHFLOWSTATEMENT_82 = Column('cashflow_statement_82', DOUBLE(asdecimal=False)) # 现金及现金等价物净增加额
    CASHFLOWSTATEMENT_86 = Column('cashflow_statement_86', DOUBLE(asdecimal=False)) # 资产减值准备

    __table_args__ = (
        Index('idx_em_stock_fin_fac_datetime', 'datetime'),
    )

class EmStockRefinancing(Base):
    '''Choice股票再融资信息表'''

    __tablename__ = 'em_stock_refinancing'

    id = Column(Integer, primary_key=True)

    SECURITYCODE = Column('stock_id', CHAR(10), nullable=False) # EM股票id
    APPROVENOTICEDATE = Column('approve_notice_date', DATE, nullable=False) # 最新公告日
    PLANNOTICEDDATE = Column('plan_noticed_date', DATE, nullable=False) # 首次公告日
    NEWPROGRESS = Column('new_progress', TEXT) # 方案进度
    SUMFINA_T = Column('sum_fina_t', DOUBLE(asdecimal=False)) # 预计募资_上限(亿元)
    ATTACHNAME = Column('attach_name', TEXT) # 原始公告链接
    ADDPURPOSE = Column('add_purpose', TEXT, nullable=False) # 增发目的

class EmIndexVal(Base):
    '''Choice指数估值数据'''

    __tablename__ = 'em_index_val'

    CODES = Column("em_id", CHAR(16), primary_key=True) # EM股票id
    DATES = Column("datetime", DATE, primary_key=True) # 日期
    PETTM = Column("pe_ttm", DOUBLE(asdecimal=False)) # 市盈率PE(TTM)
    PBMRQ = Column("pb_mrq", DOUBLE(asdecimal=False)) # 市净率PB(MRQ)
    DIVIDENDYIELD = Column("dividend_yield", DOUBLE(asdecimal=False)) # 股息率
    PSTTM = Column("ps_ttm", DOUBLE(asdecimal=False)) # 市销率PS(TTM)
    PCFTTM = Column("pcf_ttm", DOUBLE(asdecimal=False)) # 市现率PCF(TTM)
    ROE = Column("roe", DOUBLE(asdecimal=False)) # 净资产收益率
    EPSTTM = Column("eps_ttm", DOUBLE(asdecimal=False)) # 每股收益TTM

class EmTradeDates(Base):
    '''Choice交易日数据'''

    __tablename__ = 'em_tradedates'
    TRADEDATES = Column(DATE, primary_key=True)

class EmIndexComponent(Base):
    '''Choice指数成分'''

    __tablename__ = 'em_index_component'

    index_id = Column(CHAR(20), primary_key=True)
    datetime = Column(DATE, primary_key=True) # 日期
    em_id = Column(CHAR(20), nullable=False)  # Choice ID
    em_plate_id = Column(CHAR(20), nullable=False)  # Choice板块ID
    stock_list = Column(TEXT, nullable=False)  # 股票列表

class EmFundHoldingRate(Base):
    '''Choice基金持有人比例'''
    __tablename__ = 'em_fund_holding_rate'

    CODES =Column(CHAR(10), primary_key=True) # 合约代码
    DATES = Column(DATE, primary_key=True) # 日期
    HOLDPERSONALHOLDINGPCT = Column(DOUBLE(asdecimal=False)) # 个人持有比例 单位百分比
    HOLDINSTIHOLDINGPCT = Column(DOUBLE(asdecimal=False)) # 机构持有比例 单位百分比

