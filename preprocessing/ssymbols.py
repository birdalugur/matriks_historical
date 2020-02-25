#!/usr/bin/env python
# coding: utf-8


# Select specific symbols from the data using the lists in bist_symbols.csv


import pandas as pd

bistList_path: str = '../bist_symbols.csv'

data_path: str = '/home/ugur/bist_data/mid_price.csv'

dt: dict = {'symbol': 'str', 'bid_price': 'float64', 'mid_price': 'float64'}
parse_dates: list = ['date']

bist_list: pd.DataFrame = pd.read_csv(bistList_path)

data: pd.DataFrame = pd.read_csv(data_path, dtype=dt, parse_dates=parse_dates)

bist30_list: pd.Series = bist_list.bist30

bist30_data: pd.DataFrame = data[data.symbol.isin(bist30_list)]

bist30_data.sort_values(['symbol', 'date'], inplace=True)

bist30_data.to_csv('bist30data.csv', index=False)
