import pandas as pd
from numpy import nan


def ohlc(time_series) -> dict:
    """
    Get the open, high, low and close values in the data array.

    Args:
        time_series : (list or pandas series)
    """
    _open, _high, _low, _close = nan, nan, nan, nan

    if isinstance(time_series, pd.Series):
        _time = time_series.index
        _open = time_series.iloc[0]
        _high = time_series.max()
        _low = time_series.min()
        _close = time_series.iloc[-1]

    elif isinstance(time_series, pd.DataFrame):
        raise ValueError("Use pandas series or python list.")
        # _time = time_series.iloc[:, 0]

    elif isinstance(time_series, list):
        _open = time_series[0]
        _high = max(time_series)
        _low = min(time_series)
        _close = time_series[-1]

    return {'open': _open, 'high': _high, 'low': _low, 'close': _close}
