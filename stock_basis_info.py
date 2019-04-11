import tushare as ts
import pandas as pd
import time
import os

a = '/Users/zy/Desktop/work/other/algo/data'

pro = ts.pro_api('b31a70a518121c7880591cfa8121db52a604d4b2bc5a2b327d432c9d')
api = ts.pro_api('b31a70a518121c7880591cfa8121db52a604d4b2bc5a2b327d432c9d')

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

all_code=data['ts_code']

df1= pro.fina_mainbz(ts_code = all_code[0], start_date='20170101', type='P')

# 下面是把主营业务以及对应收入放在文件中

filename = '/Users/zy/Desktop/work/other/algo/data/biz.csv'
os.remove(filename)
i=0
for code in all_code:
    i=i+1
    if i%60 == 0:
        time.sleep(65)
    else:
        df0=pro.fina_mainbz(ts_code=code, start_date='20170101', type='P')
        df = df0[df0['end_date'] == df0['end_date'].max()]
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=None)
        else:
            df.to_csv(filename)

main_bus = pd.read_csv(filename)

a1 = main_bus.groupby(['ts_code','bz_item']).sum().reset_index()
a2 = a1.sort_values(['ts_code','bz_profit'], ascending=False)
a3=a2.groupby('ts_code')['bz_item'].apply(list).reset_index()

# 下面是把感念股放入csv文件中
concept = pro.concept(src='ts')
all_concept=concept['code']
filename2 = '/Users/zy/Desktop/work/other/algo/data/concept.csv'
os.remove(filename2)
i=0
for con in all_concept:
    i=i+1
    if i%60 == 0:
        time.sleep(65)
    else:
        df=pro.concept_detail(id=con, fields='id,ts_code,name')
        if os.path.exists(filename2):
            df.to_csv(filename2, mode='a', header=None)
        else:
            df.to_csv(filename2)

#把每个概念股拿出来
##1.按照每个概念的序号排序
##2.按照每只股票，把概念汇总

stock_con = pd.read_csv(filename2)
a_con =pro.concept(src='ts')
b1 = pd.merge(a_con,stock_con,left_on='code',right_on='id',how='left')
b2 = b1.groupby('ts_code')['name_x'].apply(list).reset_index()
d1 = pd.merge(a3,b2,on='ts_code')

result = pd.merge(data,d1,on='ts_code')

filename5 = '/Users/zy/Desktop/work/other/algo/data/result.csv'
os.remove(filename5)
result.to_csv(filename5)