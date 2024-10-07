import pandas as pd
import yfinance as yf
from tqdm import tqdm
import warnings

def fetch_quarterly_financials(symbols):
    """
    Fetch quarterly financial data for given symbols from Yahoo Finance.

    Args:
        symbols (list): List of stock symbols to fetch data for.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched quarterly financial data.

    The returned DataFrame has the following columns:
    - Ticker: The stock symbol
    - Date: The date of the financial data
    - variable: The financial metric
    - value: The value of the financial metric

    Example:
        ```python
        symbols = ['AAPL', 'GOOGL', 'MSFT']
        df = fetch_quarterly_financials(symbols)
        print(df.head())
        ```

    Note:
        This function uses the yfinance library to fetch data from Yahoo Finance.
        It handles errors for individual stocks and continues with the next one.
        Warnings are suppressed to avoid cluttering the output.
    """
    warnings.filterwarnings('ignore')
    df_fundamentals = pd.DataFrame()

    for ticker in tqdm(symbols, desc="Fetching financial data"):
        try:
            stock = yf.Ticker(ticker)
            df_temp = stock.quarterly_financials.transpose().reset_index()
            df_temp['Ticker'] = ticker
            df_melt = pd.melt(df_temp, id_vars=['Ticker', 'index'])
            df_fundamentals = pd.concat([df_fundamentals, df_melt], ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    df_fundamentals = df_fundamentals.rename(columns={'index': 'Date'})
    df_fundamentals['Date'] = pd.to_datetime(df_fundamentals['Date']).dt.date

    return df_fundamentals
