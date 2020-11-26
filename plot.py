import calculations as calc
import plotly.graph_objects as go


def histogram():
    pass


def candlestick(data, offset):
    ohcl = data.resample(offset).apply(calc.ohlc)
    _time = ohcl.index
    _open, _high, _low, _close = [], [], [], []
    for item in ohcl.values:
        _open.append(item['open'])
        _high.append(item['high'])
        _low.append(item['low'])
        _close.append(item['close'])

    fig = go.Figure(
        data=go.Candlestick(x=_time, open=_open, high=_high, low=_low, close=_close)
    )

    fig.show()
