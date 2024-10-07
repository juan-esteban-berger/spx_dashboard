import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from tqdm import tqdm

def fetch_stock_prices(symbols, start_date=None, end_date=None):
    """
    Fetch stock prices for given symbols from Yahoo Finance.

    Args:
        symbols (list): List of stock symbols to fetch data for.
        start_date (datetime, optional): Start date for data fetching. Defaults to 10 years ago.
        end_date (datetime, optional): End date for data fetching. Defaults to yesterday.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched stock price data.

    The returned DataFrame has the following columns:
    - Date: The date of the price data
    - Ticker: The stock symbol
    - Metric: The type of price data (Open, High, Low, Close, Volume)
    - Value: The value of the metric

    Example:
        ```python
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        df = fetch_stock_prices(symbols)
        print(df.head())
        ```

    Note:
        This function uses the yfinance library to fetch data from Yahoo Finance.
        It handles errors for individual stocks and continues with the next one.
    """
    if end_date is None:
        end_date = datetime.now() - timedelta(days=1)
    if start_date is None:
        start_date = end_date - timedelta(days=10*365)

    df_prices = pd.DataFrame()

    for ticker in tqdm(symbols, desc="Fetching stock data"):
        try:
            df_temp = yf.download(ticker,
                                  start=start_date.strftime('%Y-%m-%d'),
                                  end=end_date.strftime('%Y-%m-%d'),
                                  auto_adjust=True)
            df_temp['Ticker'] = ticker
            df_melt = pd.melt(df_temp.reset_index(),
                              id_vars=['Date', 'Ticker'],
                              var_name='Metric',
                              value_name='Value')
            df_prices = pd.concat([df_prices, df_melt], ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    df_prices['Date'] = pd.to_datetime(df_prices['Date']).dt.date

    return df_prices
