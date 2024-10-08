import pandas as pd
import yfinance as yf
from tqdm import tqdm

def fetch_quarterly_financials_gdrive(symbols_list):
    """
    Fetch quarterly financial data for given symbols from Yahoo Finance.

    Args:
        symbols_list (list): List of stock symbols to fetch data for.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched quarterly financial data.
        The DataFrame has the following columns:
        - ticker: The stock symbol
        - Date: The date of the financial data
        - Metric: The financial metric
        - Value: The value of the financial metric

    Raises:
        Exception: If there's an error in fetching or processing the data
    """
    df_fundamentals = pd.DataFrame()
    for ticker in tqdm(symbols_list, desc="Fetching financial data"):
        try:
            stock = yf.Ticker(ticker)
            df_temp = stock.quarterly_financials.transpose().reset_index()
            df_temp['ticker'] = ticker
            df_melt = pd.melt(df_temp, id_vars=['ticker', 'index'], var_name='Metric', value_name='Value')
            df_fundamentals = pd.concat([df_fundamentals, df_melt], ignore_index=True)
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
    
    df_fundamentals = df_fundamentals.rename(columns={'index': 'Date'})
    df_fundamentals['Date'] = pd.to_datetime(df_fundamentals['Date']).dt.strftime('%Y-%m-%d')
    
    return df_fundamentals
