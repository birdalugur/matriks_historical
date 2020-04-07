#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from multiprocessing import Pool


# In[ ]:


file_path = 'matriksdata.csv'


# In[ ]:


data = pd.read_csv(file_path)


# In[ ]:


date = pd.to_datetime(data.date_time)
nano = pd.to_datetime(data.timestamp_ns,unit='ns')


# In[ ]:


date_size = len(date)


# In[ ]:


x=list(range(date_size))


# In[ ]:


def set_date(i):
    return pd.Timestamp(month=date[i].month,year=date[i].year,day=date[i].day,hour=nano[i].hour,minute=nano[i].minute,second=nano[i].second,microsecond=nano[i].microsecond,nanosecond=nano[i].nanosecond)


# In[ ]:


if __name__ == '__main__':
    
    pool = Pool(processes=8)
    
    results = pool.map(set_date, x)
    
    data['date'] = results

    data.drop(['date_time','timestamp_ns'],axis=1,inplace=True)

    data.to_csv('matriksdata_1.csv',index=False)

