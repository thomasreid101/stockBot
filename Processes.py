import json
import config
import requests

# 2:30pm - 9pm OPENING TIMES

BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
ASSETS_URL = "{}/v2/assets".format(BASE_URL)
STREAMING_URL = "{}/stream".format(BASE_URL)
CLOCK_URL = "{}/v2/clock".format(BASE_URL)
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADER = {'APCA-API-KEY-ID': config.API_KEY, 'APCA-API-SECRET-KEY': config.SECRET_KEY}


def GetAccount():
    r = requests.get(ACCOUNT_URL, headers=HEADER)
    return json.loads(r.content)


def GetOrders():
    r = requests.get(ORDERS_URL, headers=HEADER)
    return json.loads(r.content)


def CreateOrder(symbol, qty, side, stock_type, time_in_force): #Maybe fix here so you cant fuck up too much
    order_data ={
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": stock_type,
        "time_in_force": time_in_force,
    }
    r = requests.post(ORDERS_URL,json=order_data ,headers=HEADER)
    return json.loads(r.content)


def IsMarketOpen():
    r = requests.get(CLOCK_URL, headers=HEADER)
    market_clock = json.loads(r.content)
    return market_clock["is_open"]


def moneyCheck():
    account = GetAccount()
    return account['cash']


def GetAllPositions():
    r = requests.get(POSITIONS_URL,headers=HEADER)
    return json.loads(r.content)


def GetPosition(symbol):
    POSITION_URL = "{}{}".format(POSITIONS_URL, symbol)
    r = requests.get(POSITION_URL,headers=HEADER)


def CloseAllPositions():
    r = requests.delete(POSITIONS_URL, headers=HEADER)
    return json.loads(r.content)


def CancelPosition(symbol):
    CloseSpecificURL = "{}{}".format(POSITIONS_URL, symbol)
    r = requests.delete(CloseSpecificURL, headers=HEADER)
    return json.loads(r.content)






# def GetAccount():
#     api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, BASE_URL, api_version='v2')
#     account = api.get_account()
#     return account