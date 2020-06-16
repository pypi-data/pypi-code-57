import pandas as pd
import numpy as np
import hashlib
import hmac
import time, datetime
import base64
from urllib.parse import quote_plus
import pycurl
from io import StringIO
from io import BytesIO
import certifi
import json

class WhaleWisdomConfig:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

def get_13f_holdings(filer_id: int, config: WhaleWisdomConfig, start_date: datetime.date=None, end_date: datetime.date=None,
    include_filer_name:bool=True, prefix:str=None
) -> pd.DataFrame:
    if not isinstance(filer_id, int) or filer_id < 0:
        raise ValueError("invalid filer id")
    
    if config == None:
        raise ValueError("invalid config")

    args = {
        "command": "holdings",
        "filer_ids": [filer_id],
        "all_quarters": 1,
        "columns": [x for x in range(0, 21, 1) if x not in [0, 2, 16, 17, 19]]
    }

    secret_key = config.private_key
    shared_key = config.public_key
    json_args = json.dumps(args)
    formatted_args = quote_plus(json_args)
    timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    digest = hashlib.sha1
    raw_args=json_args+'\n'+timenow
    hmac_hash = hmac.new(secret_key.encode(),raw_args.encode(),digest).digest()
    sig = base64.b64encode(hmac_hash).rstrip()
    url_base = 'https://whalewisdom.com/shell/command.json?'
    url_args = 'args=' + formatted_args
    url_end = '&api_shared_key=' + shared_key + '&api_sig=' + sig.decode() + '&timestamp=' + timenow
    api_url = url_base + url_args + url_end
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.URL, api_url)
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    body = buffer.getvalue()
    result = json.loads(body)
    result = result["results"][0]
    result = result["records"]
    df = pd.DataFrame.from_dict(data = result[0]["holdings"])
    df = df.iloc[0:0]
    dates = pd.Series(data=result[0]["quarter"])
    dates = df.iloc[0:0]
    for outer in result:
        date = datetime.datetime.strptime(outer["quarter"], "%Y-%m-%d").date()
        for _ in range(len(outer["holdings"])):
            dates = dates.append(pd.Series(date), ignore_index=True)
            pass
        df = df.append(outer["holdings"], ignore_index=True)
    dates = dates[0]
    df["Quarter"] = dates
    df["position_change_type"].fillna("hold", inplace=True)

    # combo fields here

    if isinstance(include_filer_name, bool):
        if not include_filer_name:
            df.drop(columns=["filer_name"], inplace=True)
    else:
        raise ValueError("include_filer_name must be a bool.")

    if prefix == None:
       pass 
    elif isinstance(prefix, str):
        temp_cols = ["stock_name", "stock_ticker", "Quarter", "security_type", "sector"]
        temp = df[temp_cols]
        df = df[[x for x in df.columns if x not in temp_cols]]
        df = df.add_prefix(prefix+"_")
        df = pd.concat([temp, df], axis=1)
    else: 
        raise ValueError("Prefix must be a string or none")

    if start_date != None and isinstance(start_date, datetime.date):
        df = df[df["Quarter"] >= start_date]
    
    if end_date != None and isinstance(end_date, datetime.date):
        df = df[df["Quarter"] <= end_date]

    return df


def get_13f_holdings_long_format(filer_ids: list, config:WhaleWisdomConfig, start_date=None, end_date=None) -> pd.DataFrame:
    if not (isinstance(filer_ids, list)):
        raise ValueError('invalid id list')
    df = pd.DataFrame()
    merge_on = ["Quarter", "security_type", "stock_ticker"]

    for i, id in enumerate(filer_ids):
        temp = get_13f_holdings(id[0], config, start_date=start_date, end_date=end_date, include_filer_name=False, prefix=id[1])
        # print(temp)
        if i == 0:
            df = temp

            # temporary
            df.drop(columns="stock_name",inplace=True)
            df.drop(columns="sector",inplace=True)
        else:
            # this is just for now, now sure how to get these to merge correctly
            temp.drop(columns="stock_name", inplace=True)
            temp.drop(columns="sector", inplace=True)

            #
            df = df.merge(temp, how="outer", on=merge_on, sort="Quarter")
            df.drop_duplicates(inplace=True)            
    return df
    
# if __name__ == "__main__":
#     config = WhaleWisdomConfig("PUB KEY", "PRIV KEY")
#     # df = get_13f_holdings(1725, config, include_filer_name=False, prefix="lonepine")
#     # cuatue 677, tiger global 2911
#     l = [(1725, "lonepine"), (3068, "viking"), (677, "coatue"), (2911, "tiger_global")]
#     df = get_13f_holdings_long_format(l, config, None, None)
#     df.to_excel('df.xlsx', index=0)
#     print(df)
