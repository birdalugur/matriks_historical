# kullanılacak kütüphaneler import ediliyor
import itertools
import pandas as pd
import numpy as np

# data'ya ait yol
data_path: str = 'data/bist30data.csv'

# csv'den okunacak verilerin tiplerini belirttik
dt: dict = {'symbol': 'str', 'bid_price': 'float64', 'mid_price': 'float64'}
parse_dates: list = ['date']

# veri okunuyor
data: pd.DataFrame = pd.read_csv(data_path, dtype=dt, parse_dates=parse_dates, index_col='date')

# TEST DATA
# all_data = data.resample('D')

data = data.reset_index().pivot_table(index='date', columns='symbol', values='mid_price')

from up_down import get_change, find_updown
from sklearn.metrics import confusion_matrix
from plot import plot_confusion_matrix, plt
import scipy.stats as stats
from sklearn.metrics import matthews_corrcoef, mutual_info_score
from sklearn.metrics import adjusted_rand_score, accuracy_score


def get_confusion_matrix(pivot, other):
    # Confusion Matrix
    c_matrix = confusion_matrix(pivot, other, labels=[1, 0, -1]).T

    c_matrix = np.delete(c_matrix, 1, 1)

    return c_matrix


all_pairs = [list(pair) for pair in itertools.permutations(data.columns, 2)]

np.set_printoptions(precision=2)

class_names = ['up', 'const', 'down']

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

for pair in all_pairs:
    print('>>>>>>>>')
    print(pair)
    # first_symbol = data[pair[0]]
    # second_symbol = data[pair[1]]
    pair_df = data[pair]

    change = pair_df.resample('D').apply(get_change)
    change = change.droplevel(0)

    # Up - Down
    up_down = change.resample('D').apply(find_updown)
    up_down = up_down.reset_index(drop=True)
    pivot = up_down.iloc[:, 1]
    other = up_down.iloc[:, 2]
    # pivot, other = find_updown(change)

    matrix = get_confusion_matrix(pivot, other)

    matrix2d = np.delete(matrix, 1, 0).reshape(2, 2)

    # stats
    mcc = matthews_corrcoef(other, pivot)
    acc_score = accuracy_score(other, pivot)
    mi = mutual_info_score(other, pivot)
    ari = adjusted_rand_score(other, pivot)
    oddsratio, p_value = stats.fisher_exact(matrix2d)

    try:
        chi2, p, dof, ex = stats.chi2_contingency(matrix)
    except ValueError:
        error_list.append(pair)
        print(pair, ': için chi2 hesaplanamadı ve değerler nan geçildi !')
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
    plot_confusion_matrix(matrix, classes=class_names, title='Normalized confusion matrix',
                          x_label=pair[0], y_label=pair[1], normalize=True)
    file_name = 'graphs_normalized/' + pair[0] + '_' + pair[1] + '.png'
    plt.savefig(file_name)
    plt.close()

    plt.figure()
    plot_confusion_matrix(matrix, classes=class_names, title='Confusion matrix, without normalized',
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
