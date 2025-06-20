def create_signal(prices):
    # compute rolling average on the last year
    prices = prices.reset_index()
    prices["average_return_1y"] = (
        prices.groupby("Ticker")["monthly_past_return"]
        .rolling(12).mean()
        .reset_index(level=0, drop=True)
    )
    prices.set_index(["Date", "Ticker"], inplace=True)

    # make signal on the 20 highest company in the month
    prices = prices.sort_values(by=["Date", "average_return_1y"], ascending=[True, False])
    prices["signal"] = False
    top20_indices = prices.groupby("Date").head(20).index
    prices.loc[top20_indices, "signal"] = True
    return prices



