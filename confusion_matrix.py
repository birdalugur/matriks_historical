# kullanılacak kütüphaneler import ediliyor
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

akbnk = data['AKBNK']
garan = data['GARAN']

# Up - Down
from up_down import get_change, find_updown

change = get_change(akbnk, garan)

up_down = find_updown(change.index, change.iloc[:, 0], change.iloc[:, 1])

up_down = up_down.loc[np.trim_zeros(up_down.AKBNK).index]

up_down = up_down.fillna(0)

# Confusion Matrix
from sklearn.metrics import confusion_matrix

c_matrix = confusion_matrix(up_down.iloc[:, 1], up_down.iloc[:, 2], labels=[1, 0, -1]).T

c_matrix = np.delete(c_matrix, 1, 1)

# Plot
from cm_plot import plot_confusion_matrix

np.set_printoptions(precision=2)

class_names = ['up', 'const', 'down']

x = plot_confusion_matrix(c_matrix, classes=class_names, title='Confusion matrix, without normalization')
y = plot_confusion_matrix(c_matrix, classes=class_names, normalize=True, title='Normalized confusion matrix')

# Info
y_true = up_down.iloc[:, 1]
y_pred = up_down.iloc[:, 2]

import scipy.stats as stats
from sklearn.metrics import matthews_corrcoef, mutual_info_score
from sklearn.metrics import adjusted_rand_score, r2_score, accuracy_score

# cnf_matrix[[True,False,True],:]
# cnf_matrix2d = np.delete(cnf_matrix,[1,3,4,5,7]).reshape(2,2)
# cnf_matrix2d

# oddsratio, pvalue = stats.fisher_exact(c_matrix)
# print('Fischer exact test p-val: ',p_value)
res = stats.chi2_contingency(c_matrix)
print('Chi-square test p-val: ', res[1])
mcc = matthews_corrcoef(y_true, y_pred)
print("Mathews correlation coef. =", mcc)
acc = accuracy_score(y_true, y_pred)
print('Accuracy score: ', acc)
mi = mutual_info_score(y_true, y_pred)
print('Mutual information score: ', mi)
ari = adjusted_rand_score(y_true, y_pred)
print('Adjusted random score: ', ari)

# oddsratio, pvalue = stats.fisher_exact(y_true, y_pred)
