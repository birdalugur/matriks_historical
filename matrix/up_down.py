import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

log = []


def get_waves(sign_pivot: pd.Series) -> pd.Series:
    """Mark the pivot's movements.
    """
    y = sign_pivot.fillna(0)
    q = ~(sign_pivot.shift() * sign_pivot).eq(1)
    z = (((y < 0) | (y > 0)) & q).cumsum()
    return z


def _find_updown(ts: pd.DatetimeIndex, pivot: pd.Series, non_pivot: pd.Series):
    # pivot'un değişim noktaları işaretleniyor
    sign_pivot = np.sign(pivot)
    waves_pivot: pd.Series = get_waves(sign_pivot)

    signs_non_pivot: pd.Series = np.sign(non_pivot)

    d1 = pd.concat([waves_pivot, sign_pivot, signs_non_pivot], axis=1)
    d1.columns = ['waves', 'sign_pivot', 'sign_other']

    group = d1.groupby('waves')
    group_names = list(group.groups.keys())

    other_signs = []
    pivot_signs = []
    pivot_time = []

    for name in group_names:
        # @sign_pivot : sign of pivot in current wave
        # @res : sign of pivot in current wave
        df = group.get_group(name)
        sign_pivot2 = np.sign(df['sign_pivot'].sum())
        if len(df) == 1:
            try:
                res = group.get_group(name + 1)['sign_other'].head(1).values[0]
            except:
                log.append((name + 1, ' is not found!'))
                res = np.nan
        else:
            sign_o = df['sign_other'].mask(df['sign_other'].eq(0)).dropna()
            if len(sign_o) == 0:
                res = 0
            else:
                res = sign_o.values[0]

        other_signs.append(res)
        pivot_signs.append(sign_pivot2)
        pivot_time.append(df.index[0])

    log.append('\n')
    log.append('--------')
    result = pd.concat([pd.Series(pivot_time), pd.Series(pivot_signs), pd.Series(other_signs)], axis=1)
    result.columns = ['date', pivot.name, non_pivot.name]
    return result


def get_confusion_matrix(pivot, other):
    # Confusion Matrix
    c_matrix = confusion_matrix(pivot, other, labels=[1, 0, -1]).T

    c_matrix = np.delete(c_matrix, 1, 1)

    return c_matrix


def find_updown(change: pd.DataFrame):
    up_down = _find_updown(change.index, change.iloc[:, 0], change.iloc[:, 1])
    up_down = up_down.loc[np.trim_zeros(up_down.iloc[:, 1]).index]
    up_down = up_down.fillna(0)
    return up_down
    # return up_down.iloc[:, 1], up_down.iloc[:, 2]
