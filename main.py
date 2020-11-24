import mydata
import mytime

data = mydata.read('data/all_data/')

data['mid_price'] = (data['bid_price'] + data['ask_price']) / 2

mid_price = data.pivot_table(index='time', columns='symbol', values='mid_price', aggfunc='mean')

mid_price = mid_price.resample('5Min').mean()

mid_price = mydata.sample()
