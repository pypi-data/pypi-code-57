
import dbconnector
import pandas as pd 
import json
def showdata(start,end):
    conn=dbconnector.connect()
    query="""select * from DTT_daily_tops where shdate1 between '{}' and '{}' ;""".format(start,end)
    cursor=conn.cursor()
    SQL_Query = pd.read_sql_query(query, conn)
    sql_data = pd.DataFrame(SQL_Query,columns=['msgid','channel','cluster_id','views','txtContent','date','shdate1']) 
    final=sql_data.sort_values(by=['shdate1','views'],axis=0).groupby('shdate1').tail(20)
    jsonformat=final.to_json(orient='records',force_ascii=False)
    return jsonformat

def main(start,end):
    start=start
    end=end
    showdata(start,end)
