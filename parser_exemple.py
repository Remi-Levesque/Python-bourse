import math
import requests
import json

url = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
apikey = '3™±PQRLNKE9VP5JH12'


symbol = 'goog'

params = {
    'function': function,
    'symbol': symbol,
    'apikey': apikey,
    'outputsize': 'compact',
    }

response = requests.get(url=url, params=params)
response = json.loads(response.text)

if __name__ == '__main__':

    for key in response.keys():
        print(key)
    print(response['Time Series (Daily)']['2018-09-24'])
