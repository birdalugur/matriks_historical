# %%
import matriks_historical as mh

username = '12951'  # your username or userid
password = 'VELI2951'  # your password
mtx = mh.MatriksData(username, password)

start_date = '2019-04-01'
end_date = '2019-04-04'
# bar_data = mtx.bar('GARAN', start_date, end_date, period='1day')
ege_data = mtx.bestbidoffer('GARAN', start_date, end_date)
print(ege_data)

# news = mh.news(username, password, symbol='THYAO')
# print((news.iloc[1]['content']))
# print(news[['content', 'source']])
# print(news.shape)


# for i in range(0, len(bar_data['date'])-1):
#         if bar_data['date'][i] == bar_data['date'][i+1]:
#                 print(str(bar_data['date'][i]) + " : Tarihinden iki tane var!")
#                 pQQrint("Index : " + str(i))
