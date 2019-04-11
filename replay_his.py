
import sys
import datetime
import tushare as ts
import pandas as pd
pro = ts.pro_api('b31a70a518121c7880591cfa8121db52a604d4b2bc5a2b327d432c9d')
api = ts.pro_api('b31a70a518121c7880591cfa8121db52a604d4b2bc5a2b327d432c9d')


a = sys.argv[1]

end_date_pre = datetime.datetime.strptime(a, '%Y-%m-%d')
end_date = end_date_pre.strftime('%Y%m%d')

delta=datetime.timedelta(days=50)
start_date_pre=end_date_pre - delta
start_date = start_date_pre.strftime('%Y%m%d')

delta1 = datetime.timedelta(days=20)
fina_date_pre = end_date_pre + delta1
fina_date = fina_date_pre.strftime('%Y%m%d')

trade_date_pre1=pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)

trade_date_pre2=trade_date_pre1[trade_date_pre1.is_open == 1].sort_values(by = 'cal_date',axis = 0,ascending = False).reset_index()

trade_date5=trade_date_pre2['cal_date']

trade_date_pre11=pro.trade_cal(exchange='', start_date=end_date, end_date=fina_date)

trade_date_pre21=trade_date_pre11[trade_date_pre11.is_open == 1].sort_values(by = 'cal_date',axis = 0,ascending = False).reset_index()

trade_date6=trade_date_pre21['cal_date']
trade_date7 = trade_date6.sort_values().reset_index()
trade_date8 = trade_date7['cal_date']

df1=pro.daily_basic(ts_code='', trade_date=trade_date5[0], fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb')
for trade_date in trade_date5[1:20]:
    df = pro.daily_basic(ts_code='', trade_date=trade_date, fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb')
    df1=df1.append(df)

df2=df1.sort_values(by = ['ts_code','trade_date'] ,axis = 0,ascending = False).reset_index()

for i in range(len(df1)-1):
    if df2.loc[i,'ts_code']==df2.loc[i+1,'ts_code']:
        df2.loc[i,'pre_close'] = df2.loc[i+1,'close']
    else:
        df2.loc[i,'pre_close'] = 0

df2.loc[len(df1)-1,'pre_close'] = 0

df2['change']=(round(df2['close']/df2['pre_close'],2)-1)*100

df3=df2[(df2['change']>9.8) & (df2['change'] < 15)]

ban0 = df3[df3['trade_date'] == trade_date5[0]].groupby('ts_code')['close'].count().reset_index()
for i in range(16)[2:]:
    a = df3[df3['trade_date'] >= trade_date5[i-1]].groupby('ts_code')['close'].count().reset_index()
    b = a[a['close'] == i]
    ban0 = ban0.append(b)
ban0.sort_values(by ='close',axis = 0,ascending = False)

ban1_all=ban0[ban0['close'] == 1]

ban1_p=ban0[(ban0['close'] == 1) | (ban0['close'] == 2)]
ban1_p1 = ban1_p.groupby('ts_code').count().reset_index()
ban1 = ban1_p1[ban1_p1['close'] == 1]
ban1['ban_num']=1

for i in range(16)[2:]:
	a = ban0[(ban0['close'] == i) | (ban0['close'] == i+1)]
	b = a.groupby('ts_code').count().reset_index()
	c = b[b['close'] == 1]
	c['ban_num'] = i
	ban1=ban1.append(c)

stock_info = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

ban_info = pd.merge(ban1,stock_info,on='ts_code',how='left')

for i in range(len(ban_info)):
    if ban_info.loc[i,'list_date'] >= trade_date5[20]:
        ban_info.loc[i,'is_new'] = 'new'
    else:
        ban_info.loc[i,'is_new'] = 'old'

ban_info.sort_values('ban_num')

today_bar = pro.daily_basic(ts_code='', trade_date=end_date, fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb')

resu1 = pd.merge(ban_info, today_bar, on = 'ts_code', how='left')

con_path = '/Users/zy/Desktop/work/other/algo/data/result.csv'
con1 = pd.read_csv(con_path)
con = con1.loc[:,['ts_code','bz_item','name_x']]

resu2 = pd.merge(resu1, con, on='ts_code', how='left')

q = ban_info['ts_code']
b = ts.pro_bar(pro_api=api, ts_code=q[0], adj='qfq', start_date=trade_date5[1], end_date=trade_date8[10])
for k in q[1:]:
    a = ts.pro_bar(pro_api=api, ts_code=k, adj='qfq', start_date=trade_date5[1], end_date=trade_date8[10])
    b = b.append(a)

b['chg'] = round(b['pct_chg'],1)
profit = b.loc[:,['ts_code','chg']]

now = datetime.datetime.now()
hour = int(now.strftime('%H'))
now_date=now.strftime('%Y%m%d')
j=1
for k in range(1,8):
    if trade_date8[k] < now_date:
        j=k+1

hour = int(now.strftime('%H'))
if hour>=17 & j<8:
    j=j+1

resu3 = resu2

for i in range(1,j):
	a1 = profit.loc[trade_date8[i],:].reset_index().drop('trade_date', axis =1).rename(columns={'chg':i}, inplace = False)
	resu3 = pd.merge(resu3, a1, on='ts_code', how='left')

redu_path = '/Users/zy/Desktop/work/other/algo/replay_his/' + end_date + '_replay.xlsx'

resu3.to_excel(redu_path, index=None)