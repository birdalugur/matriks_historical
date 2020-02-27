import pandas as pd


def merge_zeros(up_down: pd.DataFrame, limit='0.5s') -> pd.DataFrame:
    pivot = up_down.iloc[:, 1]
    duration_limit = pd.to_timedelta(limit)

    shift_sum = (pivot * pivot.shift())
    is_negative = shift_sum < 0
    pivot_waves = is_negative.cumsum()

    duration = up_down.date.diff()
    duration_bools = ~(duration <= duration_limit)
    duration_waves = duration_bools.cumsum()

    result = up_down.groupby([pivot_waves, duration_waves]).apply(find)

    return result.reset_index(drop=True)


def find(x):
    # If all non-pivot values are zero, return only the last row.
    if not (x.iloc[:, 2].any()):
        return x.tail(1)
    # Otherwise, remove the zero rows and return others
    else:
        return x.mask(x.iloc[:, 2].eq(0)).dropna()
