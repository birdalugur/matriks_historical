import pandas as pd
import numpy as np


def tick_pivot(pivot: pd.Series) -> pd.Series:
    """Mark the pivot's movements.
    """
    x = np.sign(pivot)
    y = x.fillna(0)

    q = ~(x.shift() * x).eq(1)
    z = (((y < 0) | (y > 0)) & q).cumsum()
    return z


def get_change(pivot, other):
    # NaN'ları kaldır ve change'i hesapla
    change_1 = pivot.dropna().diff().dropna()
    change_2 = other.dropna().diff().dropna()
    change_df = pd.concat([change_1, change_2], axis=1)
    change_df = change_df[(change_df.index >= change_1.index.min())]
    # # baştaki ve sondaki nan'ları kaldır
    # change_df = change_df[change_df.first_valid_index():change_df.last_valid_index()]
    return change_df


def _find_updown(ts: pd.DatetimeIndex, pivot: pd.Series, non_pivot: pd.Series):
    # pivot'un değişim noktaları işaretleniyor
    waves_pivot: pd.Series = tick_pivot(pivot)

    signs_non_pivot: pd.Series = np.sign(non_pivot)

    d1 = pd.concat([waves_pivot, pivot, non_pivot, signs_non_pivot], axis=1)
    d1.columns = ['waves', 'pivot', 'other', 'sign_other']

    group = d1.groupby('waves')
    group_names = list(group.groups.keys())

    other_signs = []
    pivot_signs = []
    pivot_time = []

    for name in group_names:
        df = group.get_group(name)
        sign_pivot = np.sign(df['pivot'].sum())
        if len(df) == 1:
            try:
                res = group.get_group(name + 1)['sign_other'].head(1).values[0]
            except:
                print(name + 1, ' is not found!')
        else:
            sign_o = df['sign_other'].mask(df['sign_other'].eq(0)).dropna()
            if len(sign_o) == 0:
                res = 0
            else:
                res = sign_o.values[0]

        other_signs.append(res)
        pivot_signs.append(sign_pivot)
        pivot_time.append(df.index[0])

    result = pd.concat([pd.Series(pivot_time), pd.Series(pivot_signs), pd.Series(other_signs)], axis=1)
    result.columns = ['date', pivot.name, non_pivot.name]
    return result


def find_updown(change: pd.DataFrame):
    up_down = _find_updown(change.index, change.iloc[:, 0], change.iloc[:, 1])
    up_down = up_down.loc[np.trim_zeros(up_down.iloc[:, 1]).index]
    up_down = up_down.fillna(0)
    return up_down.iloc[:, 1], up_down.iloc[:, 2]