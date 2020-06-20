import time

import dateutil
import pandas as pd
import pymysql
from sqlalchemy import create_engine

from fundquant.data_get.xq_data import XqApi


class LxrMerge2Jsl:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:@localhost:3306/quant')

    def merge(self, index_code):
        etf_list_df = pd.read_sql_query('select etf_code, etf_name, index_id, index_name from jsl_etf_list {}'.format(
            '' if index_code is None else " where index_id = '{}' ".format(index_code)),
            self.engine)

        index_df = pd.read_sql_query('select index_code, dt, pe, pb from index_data where pe > 0 {}'.format(
            '' if index_code is None else "and index_code = '{}' ".format(index_code)),
                                     self.engine)
        index_df['index_id'] = index_df['index_code']

        df = etf_list_df.merge(index_df, on='index_id', how='inner')

        print(len(df))

        for index, item in df.iterrows():
            etf_code = item['etf_code']
            dt = item['dt']
            etf_name = item['etf_name']
            index_code = item['index_code']
            index_name = item['index_name']
            pe = item['pe']
            pb = item['pb']

            self.upsert_jsl_etf_data(etf_code, dt, etf_name, index_code, index_name, pe, pb)

    def upsert_jsl_etf_data(self, etf_code, dt, etf_name, index_code, index_name, pe, pb):
        conn = pymysql.connect(user='root', password='', database='quant', charset='utf8')
        try:
            cursor = conn.cursor()

            sql = "insert into jsl_etf_data(`etf_code`, `dt`, `etf_name`, `index_code`, `index_name`, `pe`, `pb`) " \
                  "values('{}', '{}', '{}', '{}', '{}', {}, {}) " \
                .format(etf_code, dt, etf_name, index_code, index_name, pe, pb)

            cursor.execute(sql)
        except Exception as e:
            print(e)
            cursor = conn.cursor()
            sql = "update jsl_etf_data set etf_name='{}', index_code='{}', index_name='{}', pe={}, pb={} " \
                  " where etf_code='{}' and dt='{}' " \
                .format(etf_name, index_code, index_name, pe, pb, etf_code, dt)
            cursor.execute(sql)
        finally:
            conn.commit()

    def upsert_close_price_jsl_etf_data(self):
        etf_list_df = pd.read_sql_query('select etf_code, etf_name, index_id, index_name from jsl_etf_list',
                                        self.engine)
        for index, item in etf_list_df.iterrows():
            etf_code = item['etf_code']
            if etf_code[0] == '1':
                symbol = 'SZ' + etf_code
            else:
                symbol = 'SH' + etf_code

            df = XqApi().get_his_k_data(symbol, dateutil.today_plus(-7200), dateutil.today_plus(0))
            for idx, item1 in df.iterrows():
                close_price = item1['close']
                dt = item1['date']

                conn = pymysql.connect(user='root', password='', database='quant', charset='utf8')
                try:
                    cursor = conn.cursor()
                    sql = "update jsl_etf_data set close_price={} " \
                          " where etf_code='{}' and dt='{}' " \
                        .format(close_price, etf_code, dt)
                    cursor.execute(sql)
                except Exception as e:
                    print(e)
                finally:
                    conn.commit()
            time.sleep(10)


if __name__ == '__main__':
    merge = LxrMerge2Jsl()
    merge.merge('930652')
