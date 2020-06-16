import requests
import ast
import pandas as pd
import time

async def download_trades(start,end,coin):
    coin = "f{}".format(coin)
    dt= pd.DataFrame()
    while len(dt) == 0:
        try:
            while end > start:
                url = 'https://api-pub.bitfinex.com/v2/trades/{}/hist?end={}&limit=10000'.format(coin,end) #funding
                response = requests.request("GET", url)
                trades= response.text
                trades = ast.literal_eval(trades)
                df = pd.DataFrame(trades,columns=['#','TIME','AMOUNT','RATE','PER'])
                end = df['TIME'].iloc[-1]
                dt = dt.append(df[1:])
        except Exception as e:
            print('Couldnt get trades: '+ str(e))
            time.sleep(5)
    return(dt)
