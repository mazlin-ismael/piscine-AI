import pandas as pd
import numpy as np

def proprocessing_prices(prices):
    # Resample data on month and keep the last value
    prices = prices.resample("BME").agg("last")
    prices = prices.stack()
    prices = prices.to_frame(name="Price")
    prices.index.set_names(["Date", "Ticker"], inplace=True)


    # Filter prices outliers: Remove prices outside the range 0.1$, 10k$
    prices = prices[(prices["Price"] >= 0.1) & (prices["Price"] <= 10000)].copy()

    # Compute monthly returns
    prices["monthly_past_return"] = prices.groupby("Ticker")["Price"].pct_change()
    #prices["monthly_future_return"] = prices.groupby("Ticker")["Price"].pct_change(periods=-1)
    next_month = prices.groupby("Ticker")["Price"].shift(-1)
    current_month = prices.groupby("Ticker")["Price"].shift(0)
    prices["monthly_future_return"] = (next_month - current_month) / current_month

    # Replace returns outliers by the last value available regarding the company
    years = prices.index.get_level_values("Date").year
    excluded_years_mask = (years == 2008) | (years == 2009)

    outliers_past = (prices["monthly_past_return"] < -0.5) | (prices["monthly_past_return"] > 1)
    outliers_future = (prices["monthly_future_return"] < -0.5) | (prices["monthly_future_return"] > 1)

    mask_past = outliers_past & ~(excluded_years_mask)
    mask_future = outliers_future & ~(excluded_years_mask)

    prices.loc[mask_past, "monthly_past_return"] = np.nan
    prices.loc[mask_future, "monthly_future_return"] = np.nan

    # handle missing values
    prices["monthly_past_return"] = prices.groupby("Ticker")["monthly_past_return"].bfill()
    prices["monthly_future_return"] = prices.groupby("Ticker")["monthly_future_return"].ffill()
    prices = prices.dropna()
    return prices

def preprocessing_sp500(sp500):
    sp500 = sp500.resample("BME").agg("last")
    sp500["monthly returns"] = sp500["Adjusted Close"].pct_change()
    return sp500

def preprocessing(prices, sp500):
    return proprocessing_prices(prices), preprocessing_sp500(sp500)