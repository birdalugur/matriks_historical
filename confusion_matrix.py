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
all_data = data.resample('D')

data = list(all_data)[6][1]

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


def get_stats(y_true, y_pred):
    mcc = matthews_corrcoef(y_true, y_pred)
    # print("Mathews correlation coef. =", mcc)
    acc = accuracy_score(y_true, y_pred)
    # print('Accuracy score: ', acc)
    mi = mutual_info_score(y_true, y_pred)
    # print('Mutual information score: ', mi)
    ari = adjusted_rand_score(y_true, y_pred)
    # print('Adjusted random score: ', ari)
    return mcc, acc, mi, ari


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

for pair in all_pairs:
    print(pair)
    first_symbol = data[pair[0]]
    second_symbol = data[pair[1]]

    change = get_change(first_symbol, second_symbol)

    # Up - Down
    pivot, other = find_updown(change)

    matrix = get_confusion_matrix(pivot, other)

    matrix2d = np.delete(matrix, 1, 0).reshape(2, 2)

    # stats
    mcc = matthews_corrcoef(other, pivot)
    acc_score = accuracy_score(other, pivot)
    mi = mutual_info_score(other, pivot)
    ari = adjusted_rand_score(other, pivot)
    oddsratio, p_value = stats.fisher_exact(matrix2d)
    chi2, p, dof, ex = stats.chi2_contingency(matrix2d)

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
    plot_confusion_matrix(matrix, classes=class_names, title='Confusion matrix, normalization',
                          x_label=pair[0], y_label=pair[1], normalize=True)
    file_name = 'graphs_normalized/' + pair[0] + '_' + pair[1] + '.png'
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
    all_dof,
    all_ex,
], index=['matthews_corrcoef', 'accuracy_score', 'mutual_info_score',
          'adjusted_rand_score', 'oddsratio', 'p_value', 'chi2', 'p', 'dof', 'ex'], columns=all_pairs)


all_stats.to_csv('statistics.csv')