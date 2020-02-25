#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np

file_path: str = '../data/bist30data.csv'

export_folder: str = '../data/5min/'

dt = {'symbol': 'str', 'bid_price': 'float64', 'mid_price': 'float64'}
parse_dates = ['date']

data = pd.read_csv(file_path, dtype=dt, parse_dates=parse_dates)

data.set_index('date', inplace=True)


def to_pivot(x):
    return x.drop('symbol', axis=1).reset_index().pivot_table(index='date', columns='symbol', values='mid_price',
                                                              dropna=False).ffill()


days = []

for g, day in data.resample('D'):
    days.append(day.groupby('symbol').resample('5Min', label='right', closed='right').last())

days = [day for day in days if day.size != 0]

pivots = [to_pivot(day) for day in days]

start = []
end = []
for pivot in pivots:
    start.append(pivot.index.min())
    end.append(pivot.index.max())
time_info = pd.DataFrame({'start_time': start, 'end_time': end})
time_info.to_csv(export_folder + 'time_info.csv')

for pivot in pivots:
    name = str(pivot.index.date[0]) + '.csv'
    pivot.to_csv(export_folder + name)

# --------------------------------------------------------------------------------------------------------
# **resample fonksiyonu** kullanılarak 5'er dakikalık olacak şekilde veri yeniden şekillendirildi. Her **5dk'lık** dilim içerisindeki **son data** alındı. Bu, ilk parametre **5Min** ayarlanarak ve **last()** fonksiyonu kullanılarak yapıldı. 
# >resample fonksiyonunda kullanılabilecek diğer parametreler
# <br>
# 
# ```	
#     **Alias** 	**Description**
# 	B 		      business day frequency
# 	C 		      custom business day frequency (experimental)
# 	D 		      calendar day frequency
# 	W 		      weekly frequency
# 	M 		      month end frequency
# 	BM 		      business month end frequency
# 	CBM 	      custom business month end frequency
# 	MS 		      month start frequency
# 	BMS 	      business month start frequency
# 	CBMS 	      custom business month start frequency
# 	Q 		      quarter end frequency
# 	BQ 		      business quarter endfrequency
# 	QS 		      quarter start frequency
# 	BQS 	      business quarter start frequency
# 	A 		      year end frequency
# 	BA 		      business year end frequency
# 	AS 		      year start frequency
# 	BAS 	      business year start frequency
# 	BH 		      business hour frequency
# 	H 		      hourly frequency
# 	T, min 	      minutely frequency
# 	S 		      secondly frequency
# 	L, ms 	      milliseonds
# 	U, us 	      microseconds
# 	N 		      nanoseconds
# ```
# Son veriyi değil de ortalama almak istersek **.last()** yerine **.mean()** fonksiyonu kullanılacak.
# <br>
# Benzer şekilde kullanılabilecek fonksiyonlar **max,min,std,sum,median,...**
# 
# --------------------------------------------------------------------------------------------------------------
