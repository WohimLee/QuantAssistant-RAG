
import numpy as np
import pandas as pd
import tushare as ts




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
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,market,exchange,list_date')


pass


