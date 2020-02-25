#!/usr/bin/env python
# coding: utf-8


# Her bir sembol için, işlemin her gün kaçta başladığını ve işlemin her gün kaçta sonlandığını hesaplar.
# input : @path ('bist_data/bist30data.csv')
# output : start_end_time.csv


path = 'bist_data/bist30data.csv'

import pandas as pd

data = pd.read_csv(path, parse_dates=['date'])

data.set_index('date', inplace=True)

start_time = data.groupby('symbol').resample('D').symbol.apply(lambda x: x.index.min())

end_time = data.groupby('symbol').resample('D').symbol.apply(lambda x: x.index.max())

df = pd.concat([start_time, end_time], axis=1)

df.dropna(inplace=True)

df = df.droplevel(1).drop('date', axis=1)

df.columns = ['start_time', 'end_time']

df.to_csv('start_end_time.csv')
