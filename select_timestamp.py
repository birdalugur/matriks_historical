#!/usr/bin/env python
# coding: utf-8

# ## Aynı datetime'a sahip symbollerden, timestamp_ns değeri en büyük olanı seçin...

# In[21]:


import pandas as pd
import multiprocessing as mp
import numpy as np


# In[19]:


path = '../matriksdata.csv'


# In[2]:


data = pd.read_csv(path)


# In[3]:


# zaman sütunu datetime64 tipine dönüştürülüyor
data['date_time'] = pd.to_datetime(data.date_time)


# In[4]:


all_symbols : np.ndarray = data.symbol.unique()


# In[5]:


data : list = [data[data.symbol==all_symbols[i]] for i in range(len(all_symbols))]


# In[6]:


def last_time(q):
    return q.groupby('date_time').apply(lambda x : _last_timestamp(x))


# In[7]:


def _last_timestamp(x):
    return x.loc[x.timestamp_ns.idxmax()]


# In[27]:


if __name__ == '__main__':
    pool = mp.Pool(processes=4)
    results = pool.map(last_time, data)
    pool.close()
    result_df = pd.concat(results)
    result_df.reset_index(drop=True)
    result_df.to_csv('selected_'+path.split('/').pop())
    

