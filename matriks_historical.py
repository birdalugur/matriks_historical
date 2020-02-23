import requests
import base64
import json
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
# import datetime as dt
from collections import OrderedDict



class MatriksData(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__token = self.__login(self.__username, self.__password, False)
        self.__token_test = self.__login(self.__username, self.__password, True)
        self.__auth_header = {'Authorize': 'jwt ' + self.__token}
        print(self.__token)
        if self.__token:
            self.__disco = requests.get('https://api.matriksdata.com/disco.json')
        if self.__token_test:
            self.__disco_test = requests.get('https://apitest.matriksdata.com/disco.json')

    def __login(self, username, password, is_test):
        up = username + ':' + password
        up64 = base64.b64encode(up.encode())
        auth = 'Basic ' + str(up64)
        print(auth)
        extra_headers = {'Authorization': auth, 'X-Client-Type': 'D'}
        if is_test:
            r = requests.get("http://api.matriksdata.com/login", headers=extra_headers, auth=(username, password))
        else:
            r = requests.get("http://apitest.matriksdata.com/login", headers=extra_headers, auth=(username, password))
        response = json.loads(r.text)
        if not response['authenticated']:
            raise ValueError('Wrong username or password')
        return response['token']

    def __divide_dates(self, start, end):
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
        dates = [start]
        while (end - dates[-1]).days > 14:
            dates.append(dates[-1] + timedelta(days=13))
        dates.append(end + timedelta(days=1))
        return dates

    def __request_builder(self, url, **kwargs):
        query = str()
        first = True
        for key, value in kwargs.items():
            if first:
                query += '?' + key + '=' + str(value)
                first = False
            else:
                query += '&' + key + '=' + str(value)

        return url + query

    def requester(self, url, **kwargs):
        start_date = kwargs.pop('start_date')
        end_date = kwargs.pop('end_date')
        date_range = self.__divide_dates(start_date, end_date)
        appended_data = []
        for i in range(0, len(date_range)-1):
            counter = 0
            status_code = None
            start = date_range[i].date()
            end = date_range[i+1].date() - timedelta(days=1)
            request = self.__request_builder(url, start=start, end=end, **kwargs)
            print(request)
            response = None
            while status_code != 200:
                response = requests.get(request, headers=self.__auth_header)
                status_code = response.status_code
                counter += 1
                if counter > 10:
                    print(response.status_code, response.reason)
                    raise ConnectionError
            try:
                response_data = json.loads(response.text, object_pairs_hook=OrderedDict)
                data = pd.DataFrame.from_dict(response_data)
            except json.JSONDecodeError:
                file = StringIO(response.text)
                data = pd.read_csv(file, sep=',')

            appended_data.append(data)

        df = pd.concat(appended_data, axis=0)
        df = df.reset_index(drop=True)
        return df

    def bar(self, symbol, start_date, end_date, period):
        return self.requester('https://api.matriksdata.com/dumrul/v1/tick/bar', symbol=symbol, start_date=start_date,
                              end_date=end_date, period=period)

    def bar_local(self, symbol, start_date, end_date, period):
        return self.requester('http://192.168.105.110:6666', symbol=symbol, start_date=start_date,
                              end_date=end_date, period=period)

    def depth(self, symbol, start_date, end_date):
        return self.requester('https://api.matriksdata.com/dumrul/v1/tick/depth', symbol=symbol, start_date=start_date,
                              end_date=end_date)

    def trade(self, symbol, start_date, end_date):
        return self.requester('https://api.matriksdata.com/dumrul/v1/tick/trade', symbol=symbol, start_date=start_date,
                              end_date=end_date)
    
    def trade_bs(self, symbol, start_date, end_date):
        return self.requester('https://api.matriksdata.com/dumrul/v1/tick/trade_bs', symbol=symbol, start_date=start_date,
                              end_date=end_date)

    def bestbidoffer(self, symbol, start_date, end_date):
        return self.requester('https://api.matriksdata.com/dumrul/v1/tick/bestbidoffer', symbol=symbol,
                              start_date=start_date, end_date=end_date)

    # def news(self, username, password, headline='', symbol='', count=5000, comments=True):
    #     token = login(username, password)
    #     # print token
    #
    #     auth_token = 'jwt ' + token
    #     auth_header = {'Authorize': auth_token}
    #     # search_query = 'https://apitest.matriksdata.com/dumrul/v2/news/search?count=' + str(count) + '&query=headline:'\
    #     search_query = 'https://apitest.matriksdata.com/dumrul/v2/news/search?count=' + str(count) + '&query=symbol:'+ \
    #                    symbol +'&withComment=' + str(comments).lower()
    #     print(search_query)
    #     search_response = requests.get(search_query, headers=auth_header)
    #     search_id = json.loads(search_response.text)['id']
    #     print('Search id:', search_id)
    #
    #     appended_data = []
    #     for page_no in range(0, int(count/100)):
    #         counter = 0
    #         status_code = 0
    #         # print str(start)
    #         news_query = 'https://apitest.matriksdata.com/dumrul/v2/news/search/page?qid=' + search_id + '&page=' + \
    #                      str(page_no) + '&pageSize=100&content=' + str(comments).lower()
    #         while status_code != 200:
    #             response = requests.get(news_query, headers=auth_header)
    #             status_code = response.status_code
    #             counter += 1
    #             if counter > 10:
    #                 raise TimeoutError
    #                 # print(i, status_code)
    #
    #         response_json = json.loads(response.text, object_pairs_hook=OrderedDict)
    #         data = pd.DataFrame.from_dict(response_json)
    #         appended_data.append(data)
    #
    #         df = pd.concat(appended_data, axis=0)
    #         df = df.reset_index(drop=True)
    #     return df
