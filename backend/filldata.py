import yfinance as yf
import psycopg2
import json
from config import read_secret
import math

def fill_nan_chain(data):
    if not data:
        return data

    filled = []
    last_valid = None
    for val in data:
        if val is not None and not (isinstance(val, float) and math.isnan(val)):
            filled.append(val)
            last_valid = val
        else:
            filled.append(last_valid)

    last_valid = None
    for i in range(len(filled) - 1, -1, -1):
        if filled[i] is not None:
            last_valid = filled[i]
        elif last_valid is not None:
            filled[i] = last_valid

    return filled


def populate_data(ticker_symbol):
    DB_NAME = read_secret("POSTGRES_DB")
    DB_USER = read_secret("POSTGRES_USER")
    DB_PASS = read_secret("POSTGRES_PASSWORD")

    DB_HOST = "postgres"  
    DB_PORT = "5432"

    tsla = yf.Ticker(ticker_symbol)
    info = tsla.info

    current_price = info.get("regularMarketPrice")
    week_52_range = f"{info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}"
    volume = info.get("volume")
    market_cap = info.get("marketCap")

    pricehistory24h = json.dumps(fill_nan_chain(tsla.history(period="1d", interval="1h")["Close"].tolist()))
    pricehistory5d = json.dumps(fill_nan_chain(tsla.history(period="5d")["Close"].tolist()))
    pricehistory1m = json.dumps(fill_nan_chain(tsla.history(period="1mo")["Close"].tolist()))
    pricehistory6m = json.dumps(fill_nan_chain(tsla.history(period="6mo")["Close"].tolist()))
    pricehistory1y = json.dumps(fill_nan_chain(tsla.history(period="1y")["Close"].tolist()))
    pricehistory5y = json.dumps(fill_nan_chain(tsla.history(period="5y")["Close"].tolist()))
    pricehistoryall = json.dumps(fill_nan_chain(tsla.history(period="max")["Close"].tolist()))

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO stocks (
    name, price, week_52_range, volume, market_cap,
    pricehistory24h, pricehistory5d, pricehistory1m,
    pricehistory6m, pricehistory1y, pricehistory5y,
    pricehistoryall, avgintervalum, avgtime, avgvolume,
 total_bet_amount, link, network
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

    data = (
        info.get("longName") or ticker_symbol, current_price, week_52_range, volume, market_cap,
        pricehistory24h, pricehistory5d, pricehistory1m, pricehistory6m,
        pricehistory1y, pricehistory5y, pricehistoryall,
        0, 0, 0, 0, 
        ticker_symbol , "Sepolia Testnet"
    )

    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()

def update_stock_data(ticker_symbol):
    DB_NAME = read_secret("POSTGRES_DB")
    DB_USER = read_secret("POSTGRES_USER")
    DB_PASS = read_secret("POSTGRES_PASSWORD")
    DB_HOST = "postgres"
    DB_PORT = "5432"

    tsla = yf.Ticker(ticker_symbol)
    info = tsla.info

    week_52_range = f"{info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')}"
    volume = info.get("volume")
    market_cap = info.get("marketCap")

    pricehistory24h = json.dumps(fill_nan_chain(tsla.history(period="1d", interval="1h")["Close"].tolist()))
    pricehistory5d = json.dumps(fill_nan_chain(tsla.history(period="5d")["Close"].tolist()))
    pricehistory1m = json.dumps(fill_nan_chain(tsla.history(period="1mo")["Close"].tolist()))
    pricehistory6m = json.dumps(fill_nan_chain(tsla.history(period="6mo")["Close"].tolist()))
    pricehistory1y = json.dumps(fill_nan_chain(tsla.history(period="1y")["Close"].tolist()))
    pricehistory5y = json.dumps(fill_nan_chain(tsla.history(period="5y")["Close"].tolist()))
    pricehistoryall = json.dumps(fill_nan_chain(tsla.history(period="max")["Close"].tolist()))

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    update_query = """
    UPDATE stocks SET
        name = %s,
        week_52_range = %s,
        volume = %s,
        market_cap = %s,
        pricehistory24h = %s,
        pricehistory5d = %s,
        pricehistory1m = %s,
        pricehistory6m = %s,
        pricehistory1y = %s,
        pricehistory5y = %s,
        pricehistoryall = %s,
        network = %s
    WHERE link = %s
    """

    data = (
        info.get("longName") or ticker_symbol,
        week_52_range,
        volume,
        market_cap,
        pricehistory24h,
        pricehistory5d,
        pricehistory1m,
        pricehistory6m,
        pricehistory1y,
        pricehistory5y,
        pricehistoryall,
        "Sepolia Testnet",
        ticker_symbol
    )

    cursor.execute(update_query, data)
    conn.commit()
    cursor.close()
    conn.close()
