import pandas as pd
from memory_reducer import memory_reducer
from preprocessing import preprocessing
from create_signal import create_signal
from backtester import backtest

# import data
prices = pd.read_csv("../data/stock_prices.csv", index_col="Date", parse_dates=True, na_values=["?", ""])
sp500 = pd.read_csv("../data/sp500.csv", index_col="Date", parse_dates=True, na_values=["?", ""])

# memory reducer
prices = memory_reducer(prices)
sp500 = memory_reducer(sp500)

print(prices.info())
print("\033[31m-------------------------------------------------------------------------\033[0m")
print(sp500.info())

# preprocessing
prices, sp500 = preprocessing(prices, sp500)
print("\n\033[31mMissing values:\033[0m")
print("Prices\n", prices.isna().sum(), "\n\nsp500\n", sp500.isna().sum())

# create signal
prices = create_signal(prices)
print("\033[31m-------------------------------------------------------------------------\033[0m")

# #backtest
backtest(prices, sp500)