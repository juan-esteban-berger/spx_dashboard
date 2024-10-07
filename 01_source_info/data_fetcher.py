import pandas as pd

def fetch_sp500_companies():
    """
    Fetch S&P 500 companies data from Wikipedia.

    This function scrapes the Wikipedia page for the list of S&P 500 companies
    and returns a cleaned DataFrame with relevant information.

    Returns:
        pandas.DataFrame: A DataFrame containing the following columns:
            - symbol (str): The stock symbol of the company
            - security (str): The name of the company
            - gics_sector (str): The GICS sector of the company
            - gics_sub_industry (str): The GICS sub-industry of the company
            - headquarters_location (str): The headquarters location of the company
            - date_added (datetime.date): The date when the company was added to the S&P 500
            - cik (str): The Central Index Key (CIK) of the company
            - founded (str): The year the company was founded

    Raises:
        Exception: If there's an error in fetching or processing the data

    Example:
        ```python
        df = fetch_sp500_companies()
        print(df.head())
        ```

    Note:
        This function relies on the structure of the Wikipedia page remaining consistent.
        If the page structure changes, this function may need to be updated.
    """
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        df_info = pd.read_html(url)[0]
        df_info['Date added'] = pd.to_datetime(df_info['Date added']).dt.date
        df_info.columns = ['symbol', 'security', 'gics_sector', 'gics_sub_industry', 
                           'headquarters_location', 'date_added', 'cik', 'founded']
        df_info['founded'] = df_info['founded'].str.extract(r'(\d+)')
        df_info['cik'] = df_info['cik'].astype(str)
        return df_info
    except Exception as e:
        raise Exception(f"Error fetching S&P 500 companies data: {str(e)}")
