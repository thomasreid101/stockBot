# every day after market close this file will go through and update the historical data
# may need to format the historical data if files get to big - when adding in new row, delete last

import pandas as pd
import requests
import datetime
import numpy as np
import json
import config


HEADER = {'APCA-API-KEY-ID': config.API_KEY, 'APCA-API-SECRET-KEY': config.SECRET_KEY}
base_url = "https://data.alpaca.markets/v2"
dow_jones_tickers = ["AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW", "GS", "HD", "IBM", "INTC",
                     "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA",
                     "WMT"]
ticker_df = {}
percentiles = [5, 10, 50, 90, 95]
sp500 = pd.read_csv("constituents_csv.csv")
sp500_ticker = sp500['Symbol']


def miniboot(ticker):
    start_date = get_year_ago()
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    minute_bars = "{}/stocks/{}/bars?timeframe=1Day&start={}&end={}".format(base_url, ticker, start_date, end_date)
    r = requests.get(minute_bars, headers=HEADER)
    j = json.loads(r.content)
    k = j["bars"]
    df = pd.DataFrame()
    for bar in k:
        df = df.append(bar, ignore_index=True)
    del df['o']
    del df['h']
    del df['l']
    del df['v']
    del df['n']
    del df['vw']
    ticker_df[ticker] = df
    ticker_df[ticker]["symbol"] = ticker
    csv_name = "historical_data/Historical_data_" + ticker + ".csv"
    df.to_csv(csv_name, sep=',')


def get_three_years_ago():
    today = datetime.date.today()
    years_ago = today - datetime.timedelta(days=(3 * 365))
    return years_ago


def get_year_ago():
    today = datetime.date.today()
    years_ago = today - datetime.timedelta(days= 365)
    return years_ago


def get_five_days_ago():
    today = datetime.date.today()
    days_ago = today - datetime.timedelta(days=5)
    return days_ago


def ma_calculation(ticker):
    filename = "historical_data/Historical_data_" + ticker + ".csv"
    table = pd.read_csv(filename)
    del table['Unnamed: 0']
    ma = 21
    table['returns'] = np.log(table["c"]).diff()
    table['ma'] = table['c'].rolling(ma).mean()
    table['ratio'] = table['c'] / table['ma']
    table['ratio'].describe()
    p = np.percentile(table['ratio'].dropna(), percentiles)
    short = p[-1]
    long = p[0]
    table['position'] = np.where(table.ratio > short, -1, np.nan)
    table['position'] = np.where(table.ratio < long, 1, table['position'])
    table['position'] = table['position'].ffill()
    table.to_csv(filename, sep=',')
    #print(filename + ": updated successfully")


def bootup():
    for name in sp500_ticker:
        ticker_df[name] = pd.DataFrame()

    for stock in sp500_ticker:
         print("downloading {} data".format(stock))
         miniboot(stock)
         ma_calculation(stock)

bootup()