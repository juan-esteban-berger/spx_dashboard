import pandas as pd
import warnings

def fetch_sp500_companies_gdrive():
    """
    Fetch S&P 500 companies data from Wikipedia for Google Drive storage.

    Returns:
        pandas.DataFrame: A DataFrame containing the following columns:
        - symbol (str): The stock symbol of the company
        - security (str): The name of the company
        - gics_sector (str): The GICS sector of the company
        - gics_sub_industry (str): The GICS sub-industry of the company
        - headquarters_location (str): The headquarters location of the company
        - date_added (str): The date when the company was added to the S&P 500 (YYYY-MM-DD format)
        - cik (str): The Central Index Key (CIK) of the company
        - founded (str): The year the company was founded

    Raises:
        Exception: If there's an error in fetching or processing the data
    """
    try:
        warnings.filterwarnings('ignore')
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        df_info = pd.read_html(url)[0]
        
        df_info['Date added'] = pd.to_datetime(df_info['Date added'])
        df_info['Date added'] = df_info['Date added'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else x)
        
        df_info.columns = ['symbol', 'security', 'gics_sector', 'gics_sub_industry', 
                           'headquarters_location', 'date_added', 'cik', 'founded']
        
        df_info['founded'] = df_info['founded'].str.extract(r'(\d+)')
        df_info['cik'] = df_info['cik'].astype(str)
        
        return df_info
    except Exception as e:
        raise Exception(f"Error fetching S&P 500 companies data: {str(e)}")
