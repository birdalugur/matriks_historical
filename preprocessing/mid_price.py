#!/usr/bin/env python
# coding: utf-8


import pandas as pd

import_path = '../matriksdata_1.csv'
export_path = '../data/mid_price.csv'

dt = {'symbol': 'str', 'bid_price': 'float', 'ask_price': 'float'}
parse_dates = ['date']
cols = ['symbol', 'bid_price', 'ask_price', 'date']

data = pd.read_csv(import_path, dtype=dt,
                   parse_dates=parse_dates, usecols=cols)

# mid_price hesaplanıyor
data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

data.drop(['bid_price', 'ask_price'], inplace=True, axis=1)

data.to_csv(export_path, index=False)
