from sqlalchemy import CHAR, Column, Integer, Index, BOOLEAN, text, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT, DATETIME


class Base():
    _update_time = Column('_update_time', DATETIME, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # 更新时间


# make this column at the end of every derived table
Base._update_time._creation_order = 9999
Base = declarative_base(cls=Base)


class IndexInfo(Base):
    '''指数信息表'''

    __tablename__ = 'index_info'
    index_id = Column(CHAR(20), primary_key=True)

    order_book_id = Column(CHAR(20)) # 米筐ID
    # web_id= Column(CHAR(20)) # 数据所在网页ID
    industry_tag = Column(CHAR(64)) # 行业标签
    tag_method = Column(CHAR(64)) # 估值评分采用方法
    desc_name = Column(CHAR(64)) # 名称
    em_id = Column(CHAR(20)) # ChoiceID
    em_plate_id = Column(CHAR(20)) # Choice板块ID


class StockInfo(Base):
    '''股票信息表'''

    __tablename__ = 'stock_info'
    stock_id = Column(CHAR(20), primary_key=True) # 股票ID
    rq_id = Column(CHAR(20)) # 米筐ID


class FundSize(Base):
    '''基金最新规模'''

    __tablename__ = 'fund_size'

    fund_id = Column(CHAR(10), primary_key=True) # 基金id
    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模


class FundInfo(Base):
    '''基金信息表'''

    __tablename__ = 'fund_info'
    fund_id = Column(CHAR(10), primary_key=True) # 基金ID

    wind_id = Column(CHAR(20)) # Wind基金ID
    transition = Column(Integer) # 基金变更次数
    order_book_id = Column(CHAR(10)) # RiceQuant基金ID
    desc_name = Column(CHAR(64)) # 基金名称
    start_date = Column(DATE) # 成立日期
    end_date = Column(DATE) # 关闭日期
    wind_class_1 = Column(CHAR(64)) # Wind基金类型
    wind_class_2 = Column(CHAR(64)) # Wind基金二级类型
    manager_id = Column(TEXT) # 基金经理
    company_id = Column(CHAR(64)) # 基金公司
    benchmark = Column(CHAR(255)) # 业绩基准
    full_name = Column(CHAR(255)) # 基金全名
    currency = Column(CHAR(20)) # 币种
    base_fund_id = Column(CHAR(20)) # 分级基金基础基金代号
    is_structured = Column(TINYINT(1)) # 是否为分级基金
    is_open = Column(TINYINT(1)) # 是否为日常开放申赎的基金 1是 0否， 排除掉封闭基金和定期开放基金
    is_regular_open_ended = Column(TINYINT(1)) # 是否为定期开放式基金 1是 0否
    is_closed_ended= Column(TINYINT(1)) # 是否为封闭基金 1是 0 否
    structure_type = Column(TINYINT(1))  # 是否为分级子基金  0/nan非   1母   2分级A  3 分级B 4 其他
    is_etf = Column(TINYINT(1)) # 是否是etf  0 非  1 etf
    asset_type = Column(CHAR(32)) # 资产类别
    tt_purchase_fee = Column(DOUBLE(asdecimal=False)) # 天天基金优惠申购费
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    track_index = Column(CHAR(20)) # 跟踪指数
    benchmark_1 = Column(CHAR(255)) # 业绩基准标的指数简称第一名
    benchmark_2 = Column(CHAR(255)) # 业绩基准标的指数简称第二名
    index_id = Column(CHAR(20)) # 基于第一业绩标准所标注的指数ID
    is_c =  Column("is_c", BOOLEAN, nullable=False)  #是否是etf  0 非  1 c  
    is_a = Column("is_a", BOOLEAN, nullable=False)  #是否是etf  0 非  1 a   
    ac_filter = Column("ac_filter", BOOLEAN, nullable=False) #是否ac均有要排除的a 0 排除  1 保留  
    is_selected_mmf = Column(TINYINT(1)) # 是否基金规模最大的前50只货币基金(10年前有两只存在)  0 非  1 是
    national_debt_extension = Column(TINYINT(1)) # 纯债tag  0 非  1 是

class TradingDayList(Base):
    '''交易日列表'''

    __tablename__ = 'trading_day_list'
    datetime = Column(DATE, primary_key=True)


class FundNav(Base):
    '''基金净值表'''

    __tablename__ = 'fund_nav'
    fund_id = Column(CHAR(20), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期

    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累积单位净值 基金公司公告发布的原始数据 单位净值 + 单位累积分红
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值 考虑分红再投资后调整的单位净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    redeem_status = Column(Integer) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    subscribe_status = Column(Integer) # 订阅状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    fund_size = Column(DOUBLE(asdecimal=False)) # 基金规模

    __table_args__ = (
        Index('idx_fund_nav_datetime', 'datetime'),
    )


class IndexPrice(Base):
    '''指数价格表'''

    __tablename__ = 'index_price'
    index_id = Column(CHAR(20), primary_key=True) # 指数id
    datetime = Column(DATE, primary_key=True) # 日期

    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 成交额
    ret = Column(DOUBLE(asdecimal=False)) # 日收益

    __table_args__ = (
        Index('idx_index_price_datetime', 'datetime'),
    )


class StockPrice(Base):
    '''股票价格表'''

    __tablename__ = 'stock_price'
    stock_id = Column(CHAR(20), primary_key=True) # 指数id
    datetime = Column(DATE, primary_key=True) # 日期

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    num_trades = Column(DOUBLE(asdecimal=False)) # 交易笔数
    adj_close = Column(DOUBLE(asdecimal=False)) # 后复权价格
    post_adj_factor = Column(DOUBLE(asdecimal=False)) # 后复权因子

    __table_args__ = (
        Index('idx_stock_price_datetime', 'datetime'),
    )


class FundRet(Base):
    '''基金历史收益'''

    __tablename__ = 'fund_ret'

    fund_id = Column(CHAR(10), primary_key=True) # 原始基金ID
    datetime = Column(DATE, primary_key=True) # 日期

    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近一季度收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    to_date_ret = Column(DOUBLE(asdecimal=False)) # 成立至今收益率
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤（成立以来）
    annual_ret = Column(DOUBLE(asdecimal=False)) # 年化收益（成立以来）
    avg_size = Column(DOUBLE(asdecimal=False)) # 平均规模（成立以来）
    sharpe_ratio = Column(DOUBLE(asdecimal=False)) # 夏普率（成立以来）


class FundRatingLatest(Base):
    '''基金最新评级'''

    __tablename__ = 'fund_rating_latest'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    zs = Column(DOUBLE(asdecimal=False))  # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False))  # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False))  # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False))  # 济安金信评级
    update_time = Column(DATE)  # 更新日期

    __table_args__ = (
        Index('idx_fund_rating_latest_datetime', 'update_time'),
    )


class StyleAnalysisStockFactor(Base):
    '''风格分析股票因子'''

    __tablename__ = 'style_analysis_stock_factor'

    stock_id = Column(CHAR(10), primary_key=True)  # EM股票ID
    datetime = Column(DATE, primary_key=True)  # 日期
    rate_of_return = Column(DOUBLE(asdecimal=False), nullable=False)  # 收益率
    latest_size = Column(DOUBLE(asdecimal=False))  # 规模
    bp = Column(DOUBLE(asdecimal=False))  # 价值
    short_term_momentum = Column(DOUBLE(asdecimal=False))  # 短期动量
    long_term_momentum = Column(DOUBLE(asdecimal=False))  # 长期动量
    high_low = Column(DOUBLE(asdecimal=False))  # 波动率

    __table_args__ = (
        Index('idx_style_analysis_stock_factor_datetime', 'datetime'),
    )

class Fund_size_and_hold_rate(Base):
    '''基金规模和持有人比例'''

    __tablename__ = 'fund_size_and_hold_rate'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    datetime = Column(DATE, primary_key=True)  # 日期
    size = Column(DOUBLE(asdecimal=False)) # 最新规模
    personal_holds = Column(DOUBLE(asdecimal=False)) # 个人持有比例 单位百分比 
    institution_holds = Column(DOUBLE(asdecimal=False)) # 机构持有比例 单位百分比 

    