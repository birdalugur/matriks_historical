# import used libraries >>>>>>>
import itertools
import pandas as pd
import numpy as np
from up_down import *
from plot import plot_confusion_matrix, plt
import scipy.stats as stats
from sklearn.metrics import matthews_corrcoef, mutual_info_score
from sklearn.metrics import adjusted_rand_score, accuracy_score
# <<<<<<<<<<<<<<<<<<<<<<


# read data from csv >>>>>>>>>>>>>>>>>>>>
dropbox_link = 'https://www.dropbox.com/sh/fdnc4b1x8e9fge7/AAA2UVr5l0k19qapPVfn3COOa?dl=0'
data_path: str = 'data/bist30data.csv'
dt: dict = {'symbol': 'str', 'bid_price': 'float64', 'mid_price': 'float64'}
parse_dates: list = ['date']
data: pd.DataFrame = pd.read_csv(data_path, dtype=dt, parse_dates=parse_dates, index_col='date')
# <<<<<<<<<<<<<<<<<<<<<<

# create pivot table from data and get the permutation of symbols >>>>>>>
data = data.reset_index().pivot_table(index='date', columns='symbol', values='mid_price')
all_pairs = [list(pair) for pair in itertools.permutations(data.columns, 2)]
# <<<<<<<<<<<<<<<<<<<<<

# metrics results is store on lists >>>>>>>>
all_mcc = []
all_acs = []
all_mi = []
all_ari = []
all_oddsratio = []
all_pval = []
all_chi2 = []
all_p = []
all_dof = []
all_ex = []
error_list = list()
# <<<<<<<<<<<<<<<<<<<<<<<<<
count = 1

# get a each pair and do the following operations >>>>>>>>>> for >>>>>>
for pair in all_pairs:
    print(pair, ' : ', count)
    log.append(pair)
    count=count+1
    # select pairs >>>>>>>>
    pivot = data[pair[0]].dropna()
    other = data[pair[1]].dropna()
    # <<<<<<<<<<<<<<<<<<<<

    # calculate change for each day >>>>>>>>>>>>>>>>>
    pivot = pivot.resample('D').apply(lambda x: np.trim_zeros(x.diff().dropna())).droplevel(0)
    other = other.resample('D').apply(lambda x: np.trim_zeros(x.diff().dropna())).droplevel(0)

    change_df = pd.concat([pivot, other], axis=1)

    pivot_start_time: pd.Timestamp = pivot.index.min()
    end_time: pd.Timestamp = change_df.last_valid_index()
    change_df = change_df.between_time(start_time=pivot_start_time.time(), end_time=end_time.time())
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # up-down >>>>>>>>>>>>
    up_down = change_df.groupby(change_df.index.date).apply(find_updown)
    # <<<<<

    y_pred = up_down.iloc[:, 1]
    y_true = up_down.iloc[:, 2]

    matrix = get_confusion_matrix(y_pred, y_true)

    matrix2d = np.delete(matrix, 1, 0).reshape(2, 2)

    # stats
    mcc = matthews_corrcoef(y_true, y_pred)
    acc_score = accuracy_score(y_true, y_pred)
    mi = mutual_info_score(y_true, y_pred)
    ari = adjusted_rand_score(y_true, y_pred)
    oddsratio, p_value = stats.fisher_exact(matrix2d)

    try:
        chi2, p, dof, ex = stats.chi2_contingency(matrix)
    except ValueError:
        error_list.append(pair)
        log.append((pair, ': için chi2 hesaplanamadı ve değerler nan geçildi !'))
        chi2, p, dof, ex = np.nan, np.nan, np.nan, np.nan

    # add stats to list
    all_mcc.append(mcc)
    all_acs.append(acc_score)
    all_mi.append(mi)
    all_ari.append(ari)
    all_oddsratio.append(oddsratio)
    all_pval.append(p_value)
    all_chi2.append(chi2)
    all_p.append(p)
    all_dof.append(dof)
    all_ex.append(ex)

    plt.figure()
    plot_confusion_matrix(matrix, title='Normalized confusion matrix',
                          x_label=pair[0], y_label=pair[1], normalize=True)
    file_name = 'graphs_normalized/' + pair[0] + '_' + pair[1] + '.png'
    plt.savefig(file_name)
    plt.close()

    plt.figure()
    plot_confusion_matrix(matrix, title='Confusion matrix, without normalized',
                          x_label=pair[0], y_label=pair[1], normalize=False)
    file_name = 'graphs/' + pair[0] + '_' + pair[1] + '.png'
    plt.savefig(file_name)
    plt.close()

all_stats = pd.DataFrame([
    all_mcc,
    all_acs,
    all_mi,
    all_ari,
    all_oddsratio,
    all_pval,
    all_chi2,
    all_p,
    all_dof], index=['matthews_corrcoef', 'accuracy_score', 'mutual_info_score',
                     'adjusted_rand_score', 'oddsratio', 'p_value', 'chi2', 'p', 'dof'])

all_stats.columns = list(itertools.permutations(data.columns, 2))

all_stats.to_csv('statistics.csv')
