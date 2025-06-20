import matplotlib.pyplot as plt
import pandas as pd

def backtest_prices(prices):
    # strategy_return_prices & compute pnl
    prices["Pnl"] = prices["signal"] * prices["monthly_future_return"]
    strategy_return_prices = prices["Pnl"].sum() / prices["signal"].sum()
    print("\nstrategy_return_prices: ", strategy_return_prices, "\n")
    return prices

def backtest_sp500(sp500):
     # strategy_return_sp500 & compute pnl
    signal_serie = pd.Series(index=sp500.index, data=20)
    sp500["Pnl"] = signal_serie * sp500["monthly returns"]
    strategy_return_sp500 = sp500["Pnl"].sum() / signal_serie.sum()
    print("\nstrategy_return_sp500: ", strategy_return_sp500, "\n")
    return sp500

def plot_two_strategies(prices, sp500):
    # compare 2 differents strategies
    reset_index_prices = prices.reset_index()
    reset_index_prices = reset_index_prices.groupby("Date").agg("sum")
    reset_index_prices

    plt.plot(reset_index_prices.index, reset_index_prices["Pnl"].cumsum(), label="prices strategies")
    plt.plot(sp500.index, sp500["Pnl"].cumsum(), label="sp500 strategies")

    plt.title("Cumulative Pnl on two differents Backtest strategies")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Cumulative Pnl")
    plt.show()



def backtest(prices, sp500):
    prices = backtest_prices(prices)
    sp500 = backtest_sp500(sp500)
    plot_two_strategies(prices, sp500)
