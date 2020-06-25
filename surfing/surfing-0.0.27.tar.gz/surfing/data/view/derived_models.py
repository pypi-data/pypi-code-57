from sqlalchemy import CHAR, Column, Integer, Index, BOOLEAN, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, DATETIME


class Base():
    _update_time = Column('_update_time', DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # 更新时间


# make this column at the end of every derived table
Base._update_time._creation_order = 9999
Base = declarative_base(cls=Base)


class IndexVolatility(Base):
    '''指数波动率'''

    __tablename__ = 'index_volatility'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期
    w1_vol = Column(DOUBLE(asdecimal=False)) # 近一周波动率
    m1_vol = Column(DOUBLE(asdecimal=False)) # 近一月波动率
    m3_vol = Column(DOUBLE(asdecimal=False)) # 近三月波动率
    m6_vol = Column(DOUBLE(asdecimal=False)) # 近半年波动率
    y1_vol = Column(DOUBLE(asdecimal=False)) # 近一年波动率
    y3_vol = Column(DOUBLE(asdecimal=False)) # 近三年波动率
    y5_vol = Column(DOUBLE(asdecimal=False)) # 近五年波动率
    y10_vol = Column(DOUBLE(asdecimal=False)) # 近十年波动率
    this_y_vol = Column(DOUBLE(asdecimal=False)) # 今年以来波动率
    cumulative_vol = Column(DOUBLE(asdecimal=False)) # 成立至今波动率

    __table_args__ = (
        Index('idx_index_volatility_datetime', 'datetime'),
    )


class IndexReturn(Base):
    '''指数收益率'''

    __tablename__ = 'index_return'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期
    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近三月收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    y3_ret = Column(DOUBLE(asdecimal=False)) # 近三年收益率
    y5_ret = Column(DOUBLE(asdecimal=False)) # 近五年收益率
    y10_ret = Column(DOUBLE(asdecimal=False)) # 近十年收益率
    this_y_ret = Column(DOUBLE(asdecimal=False)) # 今年以来收益率
    cumulative_ret = Column(DOUBLE(asdecimal=False)) # 成立至今收益率

    __table_args__ = (
        Index('idx_index_return_datetime', 'datetime'),
    )


class FundAlpha(Base):
    '''基金超额收益'''

    __tablename__ = 'fund_alpha'

    track_err = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    this_y_alpha = Column(DOUBLE(asdecimal=False)) # 今年以来超额收益
    cumulative_alpha = Column(DOUBLE(asdecimal=False)) # 成立以来超额收益
    w1_alpha = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_alpha = Column(DOUBLE(asdecimal=False)) # 近一月超额收益
    m3_alpha = Column(DOUBLE(asdecimal=False)) # 近三月超额收益
    m6_alpha = Column(DOUBLE(asdecimal=False)) # 近半年超额收益
    y1_alpha = Column(DOUBLE(asdecimal=False)) # 近一年超额收益
    y3_alpha = Column(DOUBLE(asdecimal=False)) # 近三年超额收益
    y5_alpha = Column(DOUBLE(asdecimal=False)) # 近五年超额收益
    y10_alpha = Column(DOUBLE(asdecimal=False)) # 近十年超额收益
    fund_id = Column(CHAR(16), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期

    __table_args__ = (
        Index('idx_fund_alpha_datetime', 'datetime'),
    )


class IndexValuation(Base):
    '''指数估值'''

    __tablename__ = 'index_valuation'

    index_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(DATE, primary_key=True) # 日期
    pb_mrq = Column(DOUBLE(asdecimal=False)) # 市净率-MRQ
    pe_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率-MMT
    peg_ttm = Column(DOUBLE(asdecimal=False)) # PEG-MMT
    roe_ttm = Column(DOUBLE(asdecimal=False)) # 净资产收益率-MMT
    dy_ttm = Column(DOUBLE(asdecimal=False)) # 股息率-MMT
    pe_pct = Column(DOUBLE(asdecimal=False)) # PE百分位
    pb_pct = Column(DOUBLE(asdecimal=False)) # PB百分位
    val_score = Column(DOUBLE(asdecimal=False)) # 估值评分

    __table_args__ = (
        Index('idx_index_valuation_datetime', 'datetime'),
    )


class IndexValuationDevelop(Base):
    '''指数估值'''

    __tablename__ = 'index_valuation_develop'
    index_id = Column(CHAR(20), primary_key=True) #指数ID
    datetime = Column(DATE, primary_key=True) # 日期

    pb_mrq = Column(DOUBLE(asdecimal=False)) # 市净率-MRQ
    pe_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率-MMT
    roe = Column(DOUBLE(asdecimal=False)) # 净资产收益率
    ps_ttm = Column(DOUBLE(asdecimal=False)) # 市销率—MMT
    dy = Column(DOUBLE(asdecimal=False)) # 股息率
    pcf_ttm = Column(DOUBLE(asdecimal=False)) # 市现率-MMT
    peg_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率相对盈利增长比率-MMT
    pe_pct = Column(DOUBLE(asdecimal=False)) # PE百分位
    pb_pct = Column(DOUBLE(asdecimal=False)) # PB百分位
    ps_pct = Column(DOUBLE(asdecimal=False)) # PS百分位
    val_score = Column(DOUBLE(asdecimal=False)) # 估值评分
    eps_ttm = Column(DOUBLE(asdecimal=False)) # 每股收益—MMT
    roe_pct = Column(DOUBLE(asdecimal=False)) # ROE百分位

    __table_args__ = (
        Index('idx_index_valuation_develop_datetime', 'datetime'),
    )


class FundIndicator(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID
    datetime = Column(DATE, primary_key=True) # 日期
    beta = Column(DOUBLE(asdecimal=False)) # 风险指数
    alpha = Column(DOUBLE(asdecimal=False)) # 投资回报
    track_err = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    timespan = Column(DOUBLE(asdecimal=False)) # 历史数据跨度(年)
    fee_rate = Column(DOUBLE(asdecimal=False)) # 费率
    info_ratio = Column(DOUBLE(asdecimal=False)) # 信息比率
    treynor = Column(DOUBLE(asdecimal=False)) # 特雷诺比率
    mdd = Column(DOUBLE(asdecimal=False)) #净值最大回撤
    down_risk = Column(DOUBLE(asdecimal=False)) #下行风险
    ret_over_period = Column(DOUBLE(asdecimal=False)) #区间收益率
    annual_avg_daily_ret = Column(DOUBLE(asdecimal=False)) #年化日均收益
    annual_vol = Column(DOUBLE(asdecimal=False)) #年化波动率
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    m_square = Column(DOUBLE(asdecimal=False)) #M平方测度 风险调整收益指标
    time_ret = Column(DOUBLE(asdecimal=False)) #择时收益
    var = Column(DOUBLE(asdecimal=False)) #资产在险值
    r_square = Column(DOUBLE(asdecimal=False)) #决定系数R方
    sharpe = Column(DOUBLE(asdecimal=False)) #夏普率
    year_length = Column(DOUBLE(asdecimal=False)) #成立年限

    __table_args__ = (
        Index('idx_fund_indicator_datetime', 'datetime'),
    )


class FundScore(Base):
    '''基金评分'''

    __tablename__ = 'fund_score'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(10)) # 基金ID
    datetime = Column(DATE) # 日期
    score = Column(DOUBLE(asdecimal=False)) # 评分
    tag_name = Column(CHAR(64)) # 基金类别
    tag_type = Column(Integer) # 1 '大类资产评分'
    tag_method = Column(CHAR(40)) # 打标签版本号
    is_full = Column(BOOLEAN) # 1 true
    score_method = Column(Integer)
    desc_name = Column(CHAR(64))

    __table_args__ = (
        Index('idx_fund_score_datetime', 'datetime'),
    )


class AssetAllocationInfo(Base):
    '''十档大类资产组合'''

    __tablename__ = 'asset_allocation_info'
    allocation_id = Column(Integer, primary_key=True) # 组合id
    version = Column(Integer, primary_key=True) # 版本号

    hs300 =  Column(DOUBLE(asdecimal=False)) # 沪深300权重
    csi500 =  Column(DOUBLE(asdecimal=False)) # 中证500权重
    gem =  Column(DOUBLE(asdecimal=False)) # 创业板权重
    sp500rmb =  Column(DOUBLE(asdecimal=False)) # 标普500人民币权重
    national_debt = Column(DOUBLE(asdecimal=False)) # 国债权重
    gold =  Column(DOUBLE(asdecimal=False)) # 黄金权重
    credit_debt =  Column(DOUBLE(asdecimal=False)) # 信用债权重
    dax30rmb = Column(DOUBLE(asdecimal=False)) # 德国dax30权重
    real_state = Column(DOUBLE(asdecimal=False)) # 房地产权重 拼错了
    oil = Column(DOUBLE(asdecimal=False)) # 原油权重
    n225rmb = Column(DOUBLE(asdecimal=False)) # 日经225权重
    cash = Column(DOUBLE(asdecimal=False)) # 现金权重
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤
    annual_ret = Column(DOUBLE(asdecimal=False)) # 年化收益
    sharpe = Column(DOUBLE(asdecimal=False)) # 夏普率
    recent_y5_ret = Column(DOUBLE(asdecimal=False)) # 最近五年收益
    annual_vol = Column(DOUBLE(asdecimal=False)) # 年化波动率
    mdd_d1 = Column(DATE) # 最大回撤开始时间
    mdd_d2 = Column(DATE) # 最大回撤结束时间
    start_date = Column(DATE) # 回测开始时间
    end_date = Column(DATE) # 回测结束时间

class StyleAnalysisFactorReturn(Base):
    '''风格分析因子收益'''

    __tablename__ = 'style_analysis_factor_return'

    universe_index = Column(CHAR(20), primary_key=True)  # universe, 全市场股票时值为all
    datetime = Column(DATE, primary_key=True)  # 日期
    latest_size = Column(DOUBLE(asdecimal=False))  # 规模
    bp = Column(DOUBLE(asdecimal=False))  # 价值
    short_term_momentum = Column(DOUBLE(asdecimal=False))  # 短期动量
    long_term_momentum = Column(DOUBLE(asdecimal=False))  # 长期动量
    high_low = Column(DOUBLE(asdecimal=False))  # 波动率
    const = Column(DOUBLE(asdecimal=False))  # 常数项

class AllocationDistribution(Base):
    '''有效前沿下各mdd最优策略'''

    __tablename__ = 'allocation_distribution'

    ef_id = Column(CHAR(8), primary_key=True)  # 有效前沿id
    version = Column(Integer, primary_key=True) # 版本号
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    csi500 = Column(DOUBLE(asdecimal=False)) # 中证500权重
    gem = Column(DOUBLE(asdecimal=False)) #创业板权重
    gold = Column(DOUBLE(asdecimal=False)) #黄金权重
    hs300 = Column(DOUBLE(asdecimal=False)) #沪深300权重
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤
    mdd_up_limit = Column(DOUBLE(asdecimal=False)) #最大回测档位上限
    mmf = Column(DOUBLE(asdecimal=False)) # 货币基金权重
    national_debt = Column(DOUBLE(asdecimal=False)) #国债权重
    sp500rmb = Column(DOUBLE(asdecimal=False)) #标普500权重
    cash = Column(DOUBLE(asdecimal=False)) #现金权重