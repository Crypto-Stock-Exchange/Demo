from filldata import update_stock_data

tickers = [
    "AAPL", "NVDA", "MSFT", "GOOGL", "AMZN",
    "AMD", "TSLA", "INTC", "CRM", "ORCL"
]

for ticker in tickers:
    update_stock_data(ticker)
