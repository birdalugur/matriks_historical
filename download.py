#!/usr/bin/env python
# coding: utf-8

# In[1]:


from time import sleep
import pandas as pd
import matriks_historical as mh
# news = mh.news(username, password, symbol='THYAO')
# print((news.iloc[1]['content']))
# print(news[['content', 'source']])
# print(news.shape)


# for i in range(0, len(bar_data['date'])-1):
#         if bar_data['date'][i] == bar_data['date'][i+1]:
#                 print(str(bar_data['date'][i]) + " : Tarihinden iki tane var!")
#                 pQQrint("Index : " + str(i))


# In[2]:


username = '12951' #your username or userid
password = 'VELI2951' #your password
mtx = mh.MatriksData(username, password)


# In[3]:


start_date = '2019-12-31'
end_date = '2010-12-31'
# bar_data = mtx.bar('GARAN', start_date, end_date, period='1day')
#ege_data = mtx.bestbidoffer('GARAN',start_date, end_date)


# In[4]:


# symbolCodes=['GOODY', 'ALKIM', 'KOZAL', 'TTKOM', 'VESTL', 'TRGYO', 'TCELL',
#        'PETKM', 'SISE', 'CEMTS', 'GOZDE', 'MGROS', 'ENKAI', 'ISMEN',
#        'TSKB', 'HALKB', 'AKSEN', 'YKBNK', 'TMSN', 'ECZYT', 'DOAS',
#        'ZOREN', 'BRISA', 'VAKBN', 'DOHOL', 'SKBNK', 'AKBNK', 'ANACM',
#        'ISGYO', 'KARSN', 'HURGZ', 'CLEBI', 'GARAN', 'SARKY', 'KERVT',
#        'AYGAZ', 'TTRAK', 'KOZAA', 'BIMAS', 'TKFEN', 'BRSAN', 'ANSGR',
#        'FROTO', 'KARTN', 'TOASO', 'TUPRS', 'KORDS', 'DEVA', 'ODAS',
#        'SODA', 'LOGO', 'GUBRF', 'KRDMD', 'ALBRK', 'GUSGR', 'ECILC',
#        'YGGYO', 'ANHYT', 'YATAS', 'ASELS', 'CIMSA', 'TRKCM', 'KCHOL',
#        'TATGD', 'AGHOL', 'AEFES', 'TAVHL', 'SASA', 'PGSUS', 'IPEKE',
#        'ULKER', 'EGEEN', 'CCOLA', 'AKGRT', 'OTKAR', 'EREGL', 'ARCLK',
#        'ISCTR', 'EKGYO', 'SAHOL', 'THYAO', 'ALARK', 'HEKTS', 'KRDMA',
#        'AKSA', 'HLGYO', 'NTHOL', 'ISFIN', 'ENJSA', 'MAVI', 'ISDMR',
#        'ODAS R', 'MPARK', 'SOKM', 'ODAS TR']



symbolCodes=['GOODY', 'ALKIM', 'KOZAL']
# In[5]:


not_received = []


# In[6]:


master_data = pd.DataFrame(columns=['symbol','date_time','timestamp_ns','bid_price','bid_size','ask_price','ask_size'])


# In[7]:


counter = 0
for symbol in symbolCodes:
    counter = counter + 1
    try:
        data = mtx.bestbidoffer(symbol,start_date, end_date)
        master_data = master_data.append(data,sort=False)
        sleep(1)
        print(counter, ' - ',symbol,'  veriler alındı!')
    except ConnectionError:
        not_received.append(symbol)
        print(counter, ' - ',symbol,' HATA !')
        sleep(1)


# In[8]:


master_data


# In[11]:


master_data.to_csv('matriksdata.csv',index=False)


# In[13]:


len(master_data.symbol.unique())


# In[ ]:




