#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


data = pd.read_csv('../matriksdata.csv')


# In[ ]:


data['date_time'] = pd.to_datetime(data.date_time)


# In[ ]:


# Aynı datetime içeren symbol'lerin ortalaması alındı (1'er sn'lik gösterim).
data = data.groupby(['symbol','date_time']).mean()


# In[ ]:


data.reset_index(inplace=True)


# In[ ]:


data['mid_price'] = (data['bid_price']+data['ask_price'])/2


# In[ ]:


data['hour_slice'] = data.date_time.dt.hour


# In[ ]:


start_time = data.date_time.min()
end_time = data.date_time.max()


# In[ ]:


time_series = pd.date_range(start=start_time, end=end_time,freq='S')


# In[ ]:


data = data.pivot(index='date_time',columns='symbol',values='mid_price')


# In[ ]:


pivot_data = data.reindex(time_series)


# In[ ]:


# Zaman seriler resample metodu kullanılarak, belirlenen koşula göre parçalara ayrılabilir.
# Burada 'd' parametresi kullanılarak veriler günlük olarak bölündü.
# Daha fazla bilgi için -> https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#resampling
rd = pivot_data.resample('d')


# In[ ]:


# Günlük olarak bölünen veriler .csv formatında dışa aktarılıyor.
for group in list(rd.groups):
    current_data = rd.get_group(group)
    current_data.to_csv(str(group.date())+'.csv')    

