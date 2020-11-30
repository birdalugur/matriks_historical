import pandas as pd


data = pd.read_csv('data/bist30data.csv')

data = data[(data.date < '2020-01-20') & (data.date > '2020-01-15')]

data = data[data.symbol.isin(['AKBNK', 'ARCLK', 'ASELS', 'BIMAS', 'DOHOL'])]

data = data.pivot(index='date', columns='symbol', values='mid_price')


def calc_matrix(pair: pd.DataFrame):
    """
    Args:
        pair: DatetimeIndex'e sahip 2 sütunlu veri çerçevesi.
    """
    pass
