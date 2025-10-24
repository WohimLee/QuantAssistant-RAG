
import os
import numpy as np
import pandas as pd
import tushare as ts

from datetime import datetime






pro = ts.pro_api(token="fce8f09d9763b2cc31301464e0dbf8b9706286ffa29a62b5f8d9ed5c")

#查询当前所有正常上市交易的股票列表

'''
ts_code     TS股票代码
name        名称
market      市场类别 （主板/创业板/科创板/CDR/北交所）
list_status 上市状态    L上市 D退市 P暂停上市，默认是L
exchange    交易所      SSE上交所 SZSE深交所 BSE北交所
is_hs       是否沪深港通标的，N否 H沪股通 S深股通
'''

def load_api_vocab(file):

    with open(file, "r") as f:
        data = f.read().strip().split("\n")
    
    vocab = {}
    for line in data:
        items = line.split("\t")
        en, cn = items[0], items[-1]

        vocab.setdefault(en, cn)
    return vocab



def get_all_stocks(exchange="", list_status="L", fields=None, path=None, vocab=None):
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d_%H_%M")
    file_name = os.path.join(path, f"stock_list_{formatted}.csv")

    data_df = pro.stock_basic(exchange='', list_status='L', fields=fields)

    data_df.columns = [vocab.get(col, col) for col in data_df.columns]

    data_df.to_csv(file_name)


if __name__ == "__main__":

    path = "app/data/tushare_data"
    fields = "ts_code,symbol,name,area,industry,fullname,market,exchange,list_date,act_name,act_ent_type"
    vocab_file = "app/config/tushare_vocab.txt"

    vocab = load_api_vocab(vocab_file)

    get_all_stocks(fields=fields, path=path, vocab=vocab)


    pass


