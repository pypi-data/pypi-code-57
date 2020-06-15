import pandas as pd
import traceback
from ...wrapper.mysql import (RawDatabaseConnector, BasicDatabaseConnector, DerivedDatabaseConnector, 
    ViewDatabaseConnector)
from ...view.view_models import FundDailyCollection
from ...view.raw_models import RqFundIndicator
from ...view.basic_models import FundNav, FundInfo, FundRatingLatest, FundSize
from ...view.derived_models import FundAlpha, FundScore, FundIndicator
from ....constant import ExchangeStatus

class FundDailyCollectionProcessor(object):
    def get_fund_df(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    FundInfo.fund_id,
                    FundInfo.order_book_id,
                    FundInfo.wind_class_1,
                    FundInfo.start_date,
                    FundInfo.manager_id,
                    FundInfo.company_id,
                    FundInfo.benchmark,
                    FundInfo.desc_name,
                    FundInfo.track_index,
                )
                funds = pd.read_sql(query.statement, query.session.bind)
                return funds.set_index('fund_id')
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_nav_df(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(FundNav).order_by(FundNav.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                query = mn_session.query(
                    FundNav.fund_id,
                    FundNav.unit_net_value,
                    FundNav.acc_net_value,
                    FundNav.adjusted_net_value,
                    FundNav.datetime,
                    FundNav.redeem_status,
                    FundNav.subscribe_status,
                ).filter(FundNav.datetime==latest_time)

                nav = pd.read_sql(query.statement, query.session.bind)
                return nav.set_index('fund_id'), latest_time
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    # TODO: use data in basic
    def get_indicator_df(self):
        with RawDatabaseConnector().managed_session() as quant_session:
            try:
                latest_time = quant_session.query(RqFundIndicator).order_by(RqFundIndicator.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                query = quant_session.query(
                    RqFundIndicator.order_book_id,
                    RqFundIndicator.annualized_returns,
                    RqFundIndicator.annualized_risk,
                    RqFundIndicator.average_size,
                    RqFundIndicator.information_ratio,
                    RqFundIndicator.last_month_return,
                    RqFundIndicator.last_six_month_return,
                    RqFundIndicator.last_three_month_return,
                    RqFundIndicator.last_twelve_month_return,
                    RqFundIndicator.last_week_return,
                    RqFundIndicator.year_to_date_return,
                    RqFundIndicator.to_date_return,
                    RqFundIndicator.sharp_ratio,
                    RqFundIndicator.max_drop_down,
                ).filter(RqFundIndicator.datetime==latest_time)
                indicator = pd.read_sql(query.statement, query.session.bind)
                return indicator

            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_institution_rating_df(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(FundRatingLatest).order_by(FundRatingLatest.update_time.desc()).limit(1).one_or_none()
                latest_time = latest_time.update_time
                print(latest_time)
                query = mn_session.query(
                    FundRatingLatest.fund_id,
                    FundRatingLatest.zs,
                    FundRatingLatest.sh3,
                    FundRatingLatest.sh5,
                    FundRatingLatest.jajx,
                ).filter(FundRatingLatest.update_time==latest_time)
                rating = pd.read_sql(query.statement, query.session.bind)
                return rating

            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_size_df(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    FundSize.fund_id,
                    FundSize.latest_size
                )
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.drop_duplicates(subset=['fund_id'], keep='last')
                df = df.set_index('fund_id')
                return df
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_alpha_df(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(FundAlpha).order_by(FundAlpha.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    FundAlpha.fund_id,
                    FundAlpha.track_err,
                    FundAlpha.this_y_alpha,
                    FundAlpha.cumulative_alpha,
                    FundAlpha.w1_alpha,
                    FundAlpha.m1_alpha,
                    FundAlpha.m3_alpha,
                    FundAlpha.m6_alpha,
                    FundAlpha.y1_alpha,
                    FundAlpha.y3_alpha,
                    FundAlpha.y5_alpha,
                    FundAlpha.y10_alpha,
                ).filter(FundAlpha.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.drop_duplicates(subset=['fund_id'], keep='last')
                return df

            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_score_df(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(FundScore.datetime).order_by(FundScore.datetime.desc()).limit(1).one_or_none()[0]
                print(latest_time)
                query = mn_session.query(
                    FundScore.fund_id,
                    FundScore.tag_name,
                    FundScore.score,
                ).filter(FundScore.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.drop_duplicates(subset=['fund_id'], keep='last')
                return df

            except Exception as e:
                print('Failed get_score_df <err_msg> {}'.format(e))

    def get_tag_fund_indicator_df(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(FundIndicator).order_by(FundIndicator.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    FundIndicator.fund_id,
                    FundIndicator.alpha,
                    FundIndicator.beta,
                    FundIndicator.track_err,
                    FundIndicator.fee_rate,
                    FundIndicator.info_ratio,
                    FundIndicator.treynor,
                    FundIndicator.mdd,
                    FundIndicator.down_risk,
                    FundIndicator.ret_over_period,
                    FundIndicator.annual_avg_daily_ret,
                    FundIndicator.annual_vol,
                    FundIndicator.annual_ret,
                    FundIndicator.m_square,
                    FundIndicator.time_ret,
                    FundIndicator.var,
                    FundIndicator.r_square,
                    FundIndicator.sharpe,
                ).filter(FundIndicator.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns={'track_err': 'tag_track_err'})
                df = df.drop_duplicates(subset=['fund_id'], keep='last')
                return df

            except Exception as e:
                print('Failed get_fund_indicator_df <err_msg> {}'.format(e))

    def append_data(self, table_name, data_append_directly_data_df):
        if not data_append_directly_data_df.empty:
            with ViewDatabaseConnector().managed_session() as mn_session:
                try:
                    mn_session.execute(f'TRUNCATE TABLE {table_name}')
                    mn_session.commit()
                except Exception as e:
                    print(f'Failed to truncate table {table_name} <err_msg> {e}')
            data_append_directly_data_df.to_sql(table_name, ViewDatabaseConnector().get_engine(), index = False, if_exists = 'append')
            print('新数据已插入')
        else:
            print('没有需要插入的新数据')

    def get_exchange_status(self, x):
        if x['redeem_status'] == ExchangeStatus.LIMITED:
            x['redeem_status'] = ExchangeStatus.OPEN
        if x['subscribe_status'] == ExchangeStatus.LIMITED:
            x['subscribe_status'] = ExchangeStatus.OPEN
        if x['redeem_status'] == ExchangeStatus.CLOSE and x['subscribe_status'] == ExchangeStatus.CLOSE:
            return '暂停交易'
        if x['redeem_status'] == ExchangeStatus.SUSPENDED:
            return '暂停赎回'
        if x['subscribe_status'] == ExchangeStatus.SUSPENDED:
            return '暂停申购'
        if x['redeem_status'] == ExchangeStatus.OPEN and x['subscribe_status'] == ExchangeStatus.OPEN:
            return '正常开放'
        return '暂无状态'

    def get_found_to_now(self, x):
        if pd.isna(x):
            return None
        return round((pd.datetime.now().date() - x).days / 365, 2)

    def modify_fund_manager(self, x):
        try:
            return x.split('\r\n')[-1].split('(')[0]
        except:
            return x

    def compute_daily_collection(self):
        try:
            funds = self.get_fund_df()
            funds = funds.reset_index()
            funds = funds.drop_duplicates(subset=['fund_id'], keep='last')
            funds = funds.set_index('fund_id')
            print('info', funds)
            print('-' * 100)

            nav, latest_time = self.get_nav_df()
            print(latest_time)
            nav = nav.reset_index()
            nav = nav.drop_duplicates(subset=['fund_id'], keep='last')
            nav = nav.set_index('fund_id')
            print('nav', nav)
            print('-' * 100)

            alpha = self.get_alpha_df()
            alpha = alpha.set_index('fund_id')
            print(alpha)
            print('-' * 100)
            size = self.get_size_df()
            print(size)
            print('-' * 100)
            score = self.get_score_df().set_index('fund_id')
            print(score)
            print('-' * 100)
            tag_indicator = self.get_tag_fund_indicator_df().set_index('fund_id')
            print(tag_indicator)
            print('-' * 100)

            print('处理机构评级')
            rating = self.get_institution_rating_df()
            rating = rating.drop_duplicates(subset=['fund_id'], keep='last')
            rating = rating.set_index('fund_id')
            print(rating)
            print('-' * 100)

            print('处理净值')
            df = pd.concat([funds, nav, alpha, size, rating, score, tag_indicator], axis=1, sort=False)
            df.index.name = 'fund_id'
            print('_'*100)
            print(df)

            print('处理行情')
            indicator = self.get_indicator_df()
            indicator = indicator.dropna(subset=['order_book_id'])
            indicator['fund_id'] = indicator['order_book_id'] + '!0'
            indicator = indicator.drop_duplicates(subset=['order_book_id'], keep='last')
            indicator = indicator.drop(['order_book_id'], axis=1)
            indicator = indicator.set_index('fund_id')
            print(indicator)
            print('-' * 100)

            df = pd.concat([df, indicator.reindex(index=df.index)], axis=1, sort=False)
            df.index.name = 'fund_id'
            df = df.reset_index()
            df = df.dropna(subset=['fund_id'])
            df['exchange_status'] = df.apply(self.get_exchange_status, axis=1)
            df['found_to_now'] = df['start_date'].apply(self.get_found_to_now)
            df['manager_id'] = df['manager_id'].apply(self.modify_fund_manager)
            df = df.rename(columns={
                'wind_class_1': 'wind_class_I',
                'start_date': 'found_date',
                'manager_id': 'fund_manager',
                'company_id': 'company_name',
                'desc_name': 'symbol',
            })
            df = df.drop(['redeem_status', 'subscribe_status'], axis=1)
            df = df.sort_values(['fund_id'])
            df = df.drop_duplicates(subset=['order_book_id'], keep='first')
            df = df.dropna(subset=['order_book_id'])

            # df.to_csv('./hhh.csv')
            self.append_data(FundDailyCollection.__tablename__, df)

            print(df)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def process(self):
        failed_tasks = []
        if not self.compute_daily_collection():
            failed_tasks.append('compute_daily_collection')
        return failed_tasks


if __name__ == '__main__':
    FundDailyCollectionProcessor().compute_daily_collection()


