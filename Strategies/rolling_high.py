from client_functions.download_trades import download_trades
import pandas as pd
import time

async def strategy(coin):
  prevHours= 5
  end = time.time()*1000
  start = end - prevHours*60*60*1000
  trades = await download_trades(start,end,coin) #data frame of past trades

  # groups trades by hour and gets High of each hour
  trades['TIME'] = trades['TIME']/1000
  trades['TIME'] = pd.to_datetime(trades['TIME'], unit='s')
  trades['hour'] = pd.DatetimeIndex(trades['TIME']).hour
  trades= trades.groupby(['hour'])["RATE"].max()

  # target rate is the lowest High of past 3 hours
  rate = trades[-4:-1].min()
  
  # build duration of trade
  if rate > 0.0006:
      per = 30
  else:
      per = 2
  return(rate, per)
