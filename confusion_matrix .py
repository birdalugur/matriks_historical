#!/usr/bin/env python
# coding: utf-8


# kullanılacak kütüphaneler import ediliyor
from sklearn.metrics import adjusted_rand_score, r2_score, accuracy_score
from sklearn.metrics import matthews_corrcoef, mutual_info_score
import scipy.stats as stats
import itertools
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import plotly.graph_objects as go


data_path: str = 'bist30data.csv'  # data'ya ait yol

# csv'den okunacak verilerin tiplerini belirttik
dt: dict = {'symbol': 'str', 'bid_price': 'float64', 'mid_price': 'float64'}
parse_dates: list = ['date']


# veri okunuyor
data: pd.DataFrame = pd.read_csv(
    data_path, dtype=dt, parse_dates=parse_dates, index_col='date')


# TEST DATA
all_data = data.resample('D')

data = list(all_data)[6][1]

data = data.reset_index().pivot_table(
    index='date', columns='symbol', values='mid_price')


# ### Fonksiyonlar


def last_time(x):
    """DatetimeIndex'deki son zamanı döndürür
    """
    x = x.reset_index()
    return x.iloc[-1].date


def first_val(x):
    x_drop = x.dropna()
    if len(x_drop) != 0:
        return x_drop[0]
    else:
        return np.nan


def mark_data(data):
    """Dalgaları bulmak için verileri işaretler
    Parameters
    ----------
    data (pd.Series): Negatif,pozitif ve 0 içerebilen sayı dizisi
    Return
    ------
    signs (pd.Series): 1,1,1,2,2,3,3,3,4,5,6,6..vs gibi işaretlenmiş seri
    """
    # mask the zeros
    s = data.eq(0)
    # merge the zeros to the wave after them
    m = np.sign(data).mask(s).bfill()
    # result
    marked_data = m.diff().ne(0).cumsum()
    marked_data.name = 'sign'
    return marked_data


def generate_data(number: int, zero: int, nan: int) -> pd.Series:
    """ Random veri oluşturmak için kullanılır
    @number : oluşturulacak veri sayısı
    @zero : oluşturulacak verideki sıfır sayısı
    @nan : oluşturulacak verideki NaN değer sayısı
    """
    data = np.random.randint(-20, 20, number)
    data = pd.Series(data)
    data[np.random.choice(data.index, zero)] = 0
    data[np.random.choice(data.index, nan)] = np.nan
    return data


# deneme amaçlı 2 veri oluşturuluyor.
data1 = generate_data(25, 7, 4)  # pivot
data2 = generate_data(25, 9, 5)
pd.concat([data1, data2], axis=1)


fluctuation_bools = ~(np.sign(data1).eq(0) | data1.isna())


fluctuation_signs = fluctuation_bools.cumsum()


d1 = pd.concat([fluctuation_signs, data1, data2], axis=1)


d1.groupby(0).size()[d1.groupby(0).size() == 1].index+1


d1


def up_down(var_1: pd.Series, var_2: pd.Series) -> pd.DataFrame:
    """this function is for testing the result"""
    var_1[var_1 < 0] = -1
    var_1[var_1 == 0] = 0
    var_1[var_1 > 0] = 1

    var_2[var_2 < 0] = -1
    var_2[var_2 == 0] = 0
    var_2[var_2 > 0] = 1

    sign_1 = var_1.astype('str').apply(lambda x: x.split('.')[0])
    sign_2 = var_2.astype('str').apply(lambda x: x.split('.')[0])
    result = sign_1+sign_2
    result.name = 'result'
    return pd.concat([var_1, var_2, result], axis=1)


akbnk = data['AKBNK']


garan = data['GARAN']


# ### Change


# NaN'ları kaldır ve change'i hesapla
change_1 = akbnk.dropna().diff().dropna()
change_2 = garan.dropna().diff().dropna()
change_df = pd.concat([change_1, change_2], axis=1).dropna(how='all')
# index'n zaman aralığı ayarlanıyor
# bu,pivot'un başlangıç ve bitiş zamanıdır.
change_df = change_df[(change_df.index >= change_1.index.min()) & (
    change_df.index <= change_1.index.max())]


# # baştaki ve sondaki nan'ları kaldır
# change_df = change_df[change_df.first_valid_index():change_df.last_valid_index()]


# pivot'un negatif ve pozitif hareketleri işaretleniyor.
marks = mark_data(change_df.iloc[:, 0])


first = change_df.iloc[:, 0].groupby(marks).sum()


second = change_df.iloc[:, 1].groupby(marks).apply(first_val)


time_series = change_df.groupby(marks).apply(last_time)


time_series.name = 'date'


result = pd.concat([time_series, first, second], axis=1)


result = result.loc[np.trim_zeros(result.AKBNK).index]
result = result.fillna(0)


result = result.set_index('date')


result[result < 0] = -1
result[result == 0] = 0
result[result > 0] = 1


# ### Confusion Matrix


c_matrix = confusion_matrix(result.AKBNK, result.GARAN, labels=[1, 0, -1]).T


c_matrix = np.delete(c_matrix, 1, 1)


# ### Confusion Matrix Grafiği


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    x_class = np.array(classes)[[0, 2]]
    y_class = np.array(classes)

    x_tick_marks = np.arange(len(x_class))
    y_tick_marks = np.arange(len(y_class))

    plt.xticks(x_tick_marks, classes, rotation=45)
    plt.yticks(y_tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


np.set_printoptions(precision=2)


class_names = ['up', 'const', 'down']


plt.figure()
plot_confusion_matrix(c_matrix, classes=class_names,
                      title='Confusion matrix, without normalization')

plt.figure()
plot_confusion_matrix(c_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')


# ### Mutual Information Criteria


y_true = result.AKBNK
y_pred = result.GARAN


c_matrix


# cnf_matrix[[True,False,True],:]
# cnf_matrix2d = np.delete(cnf_matrix,[1,3,4,5,7]).reshape(2,2)
# cnf_matrix2d

#oddsratio, pvalue = stats.fisher_exact(c_matrix)
#print('Fischer exact test p-val: ',p_value)
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
