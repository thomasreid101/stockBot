import time
import alpaca_trade_api as tradeapi
import pandas as pd
import config  # GET THIS BIT SORTED LATER

# TODO create function that runs as a websocket
# TODO create live dataframe that ranks each stocks based on their ratio
# TODO create function to order live dataframe (maybe not needed if you can sort efficiently)
# TODO create function to update dataframe
# TODO create function that will initially select the 10 highest stocks and invest the buy/short them
# TODO create function to remove entry from dataframe
# TODO function that can split your whole money up evenly between 10 stocks
# TODO whenever you sell a stock (for loss or profit) go through list and reinvest money in next most profitable
# TODO whenever market closes, historic data updates itself and new Moving averages are used
# TODO LONG TERM provide email list at end of day for daily updates
# TODO LONG TERM use different methods. M1 - always hold 10 stocks and when a new one enters the list, sell most profitable
# TODO LONG TERM use different methods. M2 - always hold 10 stocks and when a new one enters the list, sell least profitable
# TODO LONG TERM use different methods. M3 - always hold 10 stocks and when a new one enters the list, sell lowest loss
# TODO LONG TERM use different methods. M4 - always hold 10 stocks and when a new one enters the list, sell highest loss
# TODO LONG TERM use different methods. M5 - for each value above 95/105% buy/short all of them
# TODO LONG TERM use AI on methods 1 and 2 to figure out optimum way of
# TODO LONG TERM use AI to figure out, for method 5, if it is best to buy all stocks or X number of stocks
# TODO LONG TERM calculate stocks volatility and do more reserch onn how that effects stock price
# TODO LONG TERM as capital increase, find threshold that you can start increasing number of stocks held
# TODO LONG TERM research first signs of recession and then sell all stocks if it suspects recession coming
# TODO LONG TERM try estimate when peak recession and reinvest money when that happens

hi = "hi"

# THIS IS HOW IT WILL WORK - M1
#
# each time a bar comes in, if it is in the live data dictionary, replace it, if not just add it in
# save names of all stocks in an array
# if a name is in the ^ array & InitialbuyingBoolean (means data dictionary is already full) - Start initial buying process
# Initial buying process - buy X most ratio-ed stocks (if they were above 95%/105%) - add to orders array, InitialbuyingBoolean = False
# from then, every time a stock comes in re add it to the data dictionary, check if already owned
# if already owned, update the orders data-dictionarys profit column for that stock
# if not owned, first update the live data-dictionary, then check if it its in the top 10
# if in top 10 and above 95% - save ticker as temp_Ticker - then Start Selling process
# Selling process = go through orders array and sell the most profitable then delete it from the orders array
# after selling, reinvest money and figure out how much of the most recent stock you can buy
# When market closes - update moving averages and update the historical data

# THIS IS HOW IT WILL WORK - M2
#
# each time a bar comes in, if it is in the live data dictionary, replace it, if not just add it in
# save names of all stocks in an array
# if a name is in the ^ array & InitialbuyingBoolean (means data dictionary is already full) - Start initial buying process
# Initial buying process - buy X most ratio-ed stocks (if they were above 95%/105%) - add to orders array, InitialbuyingBoolean = False
# from then, every time a stock comes in re add it to the data dictionary, check if already owned
# if already owned, update the orders data-dictionarys profit column for that stock
# if not owned, first update the live data-dictionary, then check if it its in the top 10
# if in top 10 and above 95% - save ticker as temp_Ticker - then Start Selling process
# Selling process = go through orders array and sell the least profitable/least lost then delete it from the orders array
# after selling, reinvest money and figure out how much of the most recent stock you can buy
# When market closes - update moving averages and update the historical data

# THIS IS HOW IT WILL WORK - M3
#
# each time a bar comes in, if it is in the live data dictionary, replace it, if not just add it in
# save names of all stocks in an array
# if a name is in the ^ array & InitialbuyingBoolean (means data dictionary is already full) - Start initial buying process
# Initial buying process - buy X most ratio-ed stocks (if they were above 95%/105%) - add to orders array, InitialbuyingBoolean = False
# from then, every time a stock comes in re add it to the data dictionary, check if already owned
# if already owned, update the orders data-dictionarys profit column for that stock
# if not owned, first update the live data-dictionary, then check if it its in the top 10
# if in top 10 and above 95% - save ticker as temp_Ticker - then Start Selling process
# Selling process = go through orders array and sell the lowest loss then delete it from the orders array
# after selling, reinvest money and figure out how much of the most recent stock you can buy
# When market closes - update moving averages and update the historical data

# THIS IS HOW IT WILL WORK - M4
#
# each time a bar comes in, if it is in the live data dictionary, replace it, if not just add it in
# save names of all stocks in an array
# if a name is in the ^ array & InitialbuyingBoolean (means data dictionary is already full) - Start initial buying process
# Initial buying process - buy X most ratio-ed stocks (if they were above 95%/105%) - add to orders array, InitialbuyingBoolean = False
# from then, every time a stock comes in re add it to the data dictionary, check if already owned
# if already owned, update the orders data-dictionarys profit column for that stock
# if not owned, first update the live data-dictionary, then check if it its in the top 10
# if in top 10 and above 95% - save ticker as temp_Ticker - then Start Selling process
# Selling process = go through orders array and sell the most lost then delete it from the orders array
# after selling, reinvest money and figure out how much of the most recent stock you can buy
# When market closes - update moving averages and update the historical data

# THIS IS HOW IT WILL WORK - M5
#
# each time a bar comes in, if it is in the live data dictionary, replace it, if not just add it in
# save names of all stocks in an array
# if a name is in the ^ array & InitialbuyingBoolean (means data dictionary is already full) - Start initial buying process
# if stock comes in and its above 95% and it is not in orders array start buying process
# buying process = sell all current stocks go through orders array and add all stocks that are above 95/105% to an array then start buying process.
# get total money in the account and aplit it between number in buying array
# calculate amount of each stock you could buy then buy/short that amount and add it to the orders array
# each time a stock comes in thats above 95% restart buying process


sp500 = pd.read_csv("constituents_csv.csv")
sp500_ticker = sp500['Symbol']
API_KEY = "PKS9UKQZ63W99NPBOI10"
SECRET_KEY = "AtACwKWe0mcbJXY1j90f3pwZU2XYywJednt4OlNd"
base_url = 'https://paper-api.alpaca.markets'

deviation_columns = ["ticker", "price", "deviation"]  # deviation = (ratio-1)^2
deviation_rank = pd.DataFrame(columns=deviation_columns)
orders_columns = ["ticker", "type", "ma", "close price", "profit"]
orders = pd.DataFrame(columns=orders_columns)
data_dictionary_columns = ["ticker", "position", "ma", "close price", "ratio"]
data_dictionary = pd.DataFrame(columns=data_dictionary_columns)
data_dictionary_array = []
orders_array = []


def getData():
    api_ = tradeapi.REST(API_KEY, SECRET_KEY, base_url=base_url, api_version="v2")
    startTime = time.time()
    for i in sp500_ticker:
        bar_ = api_.get_latest_bar(i)
        print(bar_)
        print(bar_.c)
    time.sleep(60.0 - ((time.time() - startTime) % 60.0))


getData()

# THIS WORKS -------------------------------------------------------------

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=base_url, api_version="v2")
account = api.get_account()
# print(account)
aapl = api.get_barset('AAPL', 'day')
# print(aapl.df)

for i in range(10):
    starttime = time.time()
    bar = api.get_latest_bar("AAPL")
    print(bar)
    print(bar.c)
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

# ------------------------------------------------------------------------


for i in range(10):
    starttime = time.time()
    bar = api.get_latest_bar("AAPL")
    print(bar)
    print(bar.c)
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

# USING THIS API CLASS, IF YOU WRITE A PROGRAM THAT RUNS EVERY MINUTE AND GETS THE VALUE FROM THEN
# START NEW DATASTREAM FILE FROM HERE ---------------------------------------------------------------

import json
import numpy as np
import pandas as pd
import config
import Processes

# this will moniter the data coming in from alpaca every minute
# this will also compare every stock to see which are the most profitable and which should be invested in

# Email list of currently held positions at the end of the day
# make big list


sp500 = pd.read_csv("constituents_csv.csv")
sp500_ticker = sp500['Symbol']
# socket = "wss://data.alpaca.markets/stream"
socket = "wss://api.alpaca.markets/stream"
authorisation = {
    "action": "authenticate",
    "data": {
        "key_id": config.API_KEY,
        "secret_key": config.SECRET_KEY,
    }
}
listen_request = {
    "action": "listen",
    "data": {
        "streams": ["trade_updates"]
    }
}

deviation_columns = ["ticker", "price", "deviation"]  # deviation = (ratio-1)^2
deviation_rank = pd.DataFrame(columns=deviation_columns)
# on message update each message, update deviation list, check that the first ten values in the ticker column are the same

orders_columns = ["ticker", "type", "ma", "close price", "profit"]
orders = pd.DataFrame(columns=orders_columns)
data_dictionary_columns = ["ticker", "position", "ma", "close price", "ratio"]
data_dictionary = pd.DataFrame(columns=data_dictionary_columns)
data_dictionary_array = []
orders_array = []


def get_minute_tickers(sp500_tickers):
    minute_tickers = []
    minute_start = "AM."
    for i in range(len(sp500_tickers)):
        new_ticker = "{}{}".format(minute_start, sp500_tickers[i])
        minute_tickers.append(new_ticker)
    return minute_tickers


sp500_minute_tickers = get_minute_tickers(sp500_ticker)


def on_open(ws):
    print("opened")
    # dataFormatter.bootup()
    ws.send(json.dumps(authorisation))
    # listen_message = {"action": "listen", "data": {"streams": sp500_minute_tickers}}
    listen_message = {"action": "listen", "data": {"streams": "AAPL"}}
    ws.send(json.dumps(listen_message))


# WILL NEED TO CHANGE A LOT
def on_message(ws, message):
    # save to dataframe
    mess = json.loads(message)
    df = save_message(mess)
    # update the profit column
    update_orders(mess)
    check_to_make_transaction(mess)


# When connection is closed for the day, check market is closed using the clock method
# if it is not closed, you need to reconnect
# if it is run dataformatter.bootup


def on_close(ws, close_status_code, close_msg):
    print("closed connection")


def check(message):
    mess = json.loads(message)
    if mess["stream"] != "authorization" and mess["stream"] != "listening":
        ticker = mess["stream"]
        close_price = mess["data"]["c"]
        ticker_correct = ticker.replace('AM.', '')
        data = "historical_data/Historical_data_" + ticker_correct + ".csv"
        table = pd.read_csv(data)
        del table['Unnamed: 0']

        percentiles = [5, 95]
        p = np.percentile(table['ratio'].dropna(), percentiles)
        short = p[-1]
        long = p[0]
        last_row = table.iloc[-1]
        position = last_row['position']
        ma = last_row['ma']
        ratio = close_price / ma
        have = False

        print("{}: {}".format(ticker_correct, close_price))
        if is_in(ticker_correct, "short"):
            have = True
            if close_price < ma and close_price < get_bought_price(ticker_correct, "short"):
                # Processes.closeOrder(ticker_correct)
                Processes.CancelPosition(ticker_correct)
                message = "I just closed {} CONGRATULATIONS!!!".format(ticker_correct)
                bought_price = get_bought_price(ticker_correct, "short")
                profit = (100 * bought_price) - (100 * close_price)
                print(message)
                print("you just made {}".format(profit))
                temp_order = {"stock": ticker_correct, "type": "short", "price": bought_price}
                orders.remove(temp_order)
        if is_in(ticker_correct, "buy"):
            have = True
            if close_price > ma and close_price > get_bought_price(ticker_correct, "buy"):
                Processes.CancelPosition(ticker_correct)
                # headerFile2.closeOrder(ticker_correct)
                message = "I just closed {} CONGRATULATIONS!!!".format(ticker_correct)
                final_price = get_bought_price(ticker, "buy")
                profit = ((100 * close_price) - (100 * final_price))
                print(message)
                print("you just made {}".format(profit))
                order = {"stock": ticker_correct, "type": "buy", "price": final_price}
                orders.remove(order)
        if ratio > short:
            # while float(headerFile.moneyCheck()) < (100 * close_price) + close_price / 20:
            #   1+1
            # get all orders
            # sell off orders that is up the most
            if float(Processes.moneyCheck()) > (100 * close_price) + close_price / 20:
                Processes.CreateOrder(ticker_correct, 100, "sell", "market", "gtc")
                # headerFile2.createOrder(ticker_correct, 100, "sell", "market", "gtc")
                order = {"stock": ticker_correct, "type": "short", "price": close_price}
                orders.append(order)
                message = "I just shorted 100 stocks of {} at {}".format(ticker_correct, close_price)
                print(message)
                # email_client.sendmail(sender_email, reciever_email, message)
        elif ratio < long:
            if float(Processes.moneyCheck()) > (100 * close_price) + close_price / 20:
                Processes.CreateOrder(ticker_correct, 100, "buy", "market", "gtc")
                order = {"stock": ticker_correct, "type": "buy"}
                orders.append(order)
                message = "I just bought 100 stocks of {} at {}".format(ticker_correct, close_price)
                print(message)
                # email_client.sendmail(sender_email, reciever_email, message)
        if not have:
            if position == -1:
                if float(Processes.moneyCheck()) > (100 * close_price):
                    Processes.CreateOrder(ticker_correct, 100, "sell", "market", "gtc")
                    order = {"stock": ticker_correct, "type": "short", "price": close_price}
                    orders.append(order)
                    message = "I just shorted 100 stocks of {} at {}".format(ticker_correct, close_price)
                    print(message)
                    # email_client.sendmail(sender_email, reciever_email, message)
            if position == 1:
                if float(Processes.moneyCheck()) > (100 * close_price) + close_price / 20:
                    Processes.CreateOrder(ticker_correct, 100, "buy", "market", "gtc")
                    order = {"stock": ticker_correct, "type": "buy", "price": close_price}
                    orders.append(order)
                    message = "I just bought 100 stocks of {} at {}".format(ticker_correct, close_price)
                    print(message)
                    # email_client.sendmail(sender_email, reciever_email, message)


def is_in(ticker, sell_type):
    in_it = False
    if not orders:
        return in_it
    for i in range(len(orders)):
        temp = orders[i]
        temp_ticker = temp['stock']
        temp_type = temp['type']
        if temp_ticker == ticker and temp_type == sell_type:
            in_it = True
    return in_it


def get_bought_price(ticker, sell_type):
    price2 = 0

    for i in range(len(orders)):
        temp = orders[i]
        temp_ticker = temp['stock']
        temp_type = temp['type']
        temp_price = temp['price']
        if temp_ticker == ticker and temp_type == sell_type:
            price2 = temp_price
    return price2


def save_message(mess):
    if mess["stream"] != "authorization" and mess["stream"] != "listening":
        ticker = mess["stream"]
        ticker_correct = ticker.replace('AM.', '')
        close_price = mess["data"]["c"]
        data = "historical_data/Historical_data_" + ticker_correct + ".csv"
        table = pd.read_csv(data)
        del table['Unnamed: 0']
        last_row = table.iloc[-1]
        position = last_row['position']
        ma = last_row['ma']
        ratio = close_price / ma

        stock_data = {"ticker": ticker_correct, "position": position, "ma": ma, "close price": close_price,
                      "ratio": ratio}
        delete_message(mess)
        data_dictionary_array.append(stock_data)
        # print(data_dictionary_array)
        # try get to work with dataframe
    else:
        print(mess)

    # ticker = from message
    # correct_ticker = ticker without (AM.)
    # ticker_url = ticker + historical data
    # position = from historical_data
    # ma = from historical data
    # close price = from message
    # ratio = close_price/ma
    # adjusted ratio = ratio * ratio

    # stock_data = [correct_ticker, position, ma, close_price, ratio, adjusted ratio]
    # data_dictionary.add(stock_data)
    # no return
    return 0


def delete_message(message):
    index = -2
    ticker = message["stream"]
    ticker_correct = ticker.replace('AM.', '')
    if not data_dictionary_array:
        return True
    for i in range(len(data_dictionary_array)):
        if data_dictionary_array[i]["ticker"] == ticker_correct:
            index = i
    if index != -2:
        # data_dictionary.drop(index=index)
        del data_dictionary_array[index]
    return True


def update_orders(message):
    if message["stream"] != "authorization" and message["stream"] != "listening":
        ticker = message["stream"]
        ticker_correct = ticker.replace('AM.', '')
        for i in range(len(orders_array)):
            if orders_array[i]["ticker"] == ticker_correct:
                if orders_array[i]["type"] == "buy":
                    profit = float(message["data"]["c"]) - float(orders_array[i]["close price"])
                    orders_array[i]["profit"] = str(profit)
                    check_to_close_transaction(message, i)

                else:
                    profit = float(orders_array[i]["close price"]) - float(message["data"]["c"])
                    orders_array[i]["profit"] = str(profit)
                    check_to_close_transaction(message, i)

    # for each order in orders list
    # if message["stock"] = data_dictionary["stock"][i]
    # update closing value
    # check_to_make_transaction
    # check_to_close_transaction
    return 0


def check_to_make_transaction(mess):
    if mess["stream"] != "authorization" and mess["stream"] != "listening":
        ticker = mess["stream"]
        close_price = float(mess["data"]["c"])
        ticker_correct = ticker.replace('AM.', '')
        if not in_orders(ticker_correct):
            data = "historical_data/Historical_data_" + ticker_correct + ".csv"
            table = pd.read_csv(data)
            del table['Unnamed: 0']
            percentiles = [5, 95]
            p = np.percentile(table['ratio'].dropna(), percentiles)
            short = p[-1]
            long = p[0]
            last_row = table.iloc[-1]
            ma = float(last_row['ma'])
            ratio = close_price / ma
            # print("{}: {}: {}".format(ticker_correct, close_price, ratio))
            # print("======{} or {}".format(short, long))
            if ratio > short:
                if float(Processes.moneyCheck()) > (100 * close_price):
                    Processes.CreateOrder(ticker_correct, 100, "sell", "market", "gtc")
                    order = {"ticker": ticker_correct, "type": "sell", "ma": ma, "close price": close_price,
                             "profit": 0}
                    orders_array.append(order)
                    message = "I just shorted 100 stocks of {} at ${}".format(ticker_correct, close_price)
                    print(message)
                else:
                    liquidate(100 * close_price, ticker_correct, "sell", close_price, ma)
            elif ratio < long:
                if float(Processes.moneyCheck()) > (100 * close_price):
                    Processes.CreateOrder(ticker_correct, 100, "buy", "market", "gtc")
                    order = {"ticker": ticker_correct, "type": "buy", "ma": ma, "close price": close_price, "profit": 0}
                    orders_array.append(order)
                    message = "I just bought 100 stocks of {} at ${}".format(ticker_correct, close_price)
                    print(message)
                else:
                    liquidate(100 * close_price, ticker_correct, "buy", close_price, ma)
            # get percentiles from histoical data
            # short 95%
            # long 5%
            # get ratio from message
            # if ratio > short
            # if have_enough_money - short
            # else liqudate
            # if ratio < long
            # if have_enough_money - buy
            # else liquidate(money_needed)


def check_to_close_transaction(message, i):
    sale_type = orders_array[i]["type"]
    bought_price = orders_array[i]["close price"]
    pro = orders_array[i]["profit"]
    # check if the bought price is above MA -
    ticker = message["stream"]
    close_price = message["data"]["c"]
    ticker_correct = ticker.replace('AM.', '')

    data = "historical_data/Historical_data_" + ticker_correct + ".csv"
    table = pd.read_csv(data)
    del table['Unnamed: 0']
    last_row = table.iloc[-1]
    ma = last_row['ma']
    # print(message)
    # ma = 1000000000
    if sale_type == "buy":
        if close_price > ma and close_price > bought_price:
            Processes.CancelPosition(ticker_correct)
            print("CONGRATS, I just sold 100 stocks of {} at ${}".format(ticker_correct, close_price))
            # bought_price = get_bought_price(ticker, "buy")
            profit = 100 * float(pro)
            print("you just made ${}".format(profit))
            orders_array.pop(i)
        elif close_price < bought_price * 0.9:
            # get bought price
            Processes.CancelPosition(ticker_correct)
            print("I sold your shares of {} at ${} as it dipped below 90%".format(ticker_correct, close_price))
            profit = 100 * float(pro)
            print("unfortunately you lost ${}".format(abs(profit)))
            orders_array.pop(i)
    elif sale_type == "sell":
        if close_price < ma and close_price < bought_price:
            Processes.CancelPosition(ticker_correct)
            print("CONGRATS, I just sold 100 stocks of {} at ${}".format(ticker_correct, close_price))
            profit = 100 * float(pro)
            print("you just made ${}".format(profit))
            orders_array.pop(i)
        elif close_price > bought_price * 1.1:
            Processes.CancelPosition(ticker_correct)
            print("I sold your shares of {} at ${} as it was above 110%".format(ticker_correct, close_price))
            profit = 100 * float(pro)
            print("unfortunately you lost ${}".format(profit))
            orders_array.pop(i)

    # if ticker-message is in orderd
    # loop through orders
    # if bought
    # if stock above MA - sell
    # get price stock was bought for, *0.9
    # if close_price-message < 90% value - sell

    # if short
    # if stock below MA - buy
    # get price stock was short for, *1.1
    # if close_price-message > 110% - buy
    return 0


def liquidate(money_needed, ticker, buy_type, close_price, ma):
    have_enough = False
    while not have_enough:
        orders.sort_values(by=['profit'])
        top_stock = orders[1]
        Processes.CancelPosition(top_stock["ticker"])
        print("CONGRATS, I just sold 100 stocks of {} at {} for {} profit!!".format(top_stock["ticker"],
                                                                                    top_stock["close price"],
                                                                                    top_stock["profit"]))
        if float(Processes.moneyCheck()) > money_needed:
            Processes.CreateOrder(ticker, 100, buy_type, "market", "gtc")
            # could update this to get a reciept of the transaction but cbf atm
            order = [ticker, "sell", ma, close_price, 0]
            orders.append(order)
            message = "I just shorted 100 stocks of {} at {}".format(ticker, close_price)
            print(message)
            have_enough = True

    # while have_enough = false
    # sort orders by profit
    # close stock at top of list
    # delete top row from orders
    return 0


def in_orders(ticker):
    for i in range(len(orders_array)):
        if orders_array[i]["ticker"] == ticker:
            return True
    else:
        return False
