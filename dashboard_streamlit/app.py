import warnings
warnings.filterwarnings('ignore')

import os
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

############################################################################
# Page Configurations
st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
        [data-testid="stDecoration"] {
                display: none;
        }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>""",
unsafe_allow_html=True)

############################################################################
# HTML Centered Title
st.markdown('<h1 style="text-align: center;">S&P 500 Dashboard</h1>', unsafe_allow_html=True)

############################################################################
# Database Credentials
host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PGPASSWORD')
database = os.getenv('DATABASE')

# Remove trailing whitespace
host = host.strip()
port = port.strip()
user = user.strip()
password = password.strip()
database = database.strip()

############################################################################
# PostgreSQL to Pandas DataFrame Function
def postgresql(sql_query, host, user, password, database, port):
    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=database
    )

    # Create a new cursor
    cur = conn.cursor()

    # Execute the query
    cur.execute(sql_query)

    # Get the column names
    colnames = [desc[0] for desc in cur.description]

    # Fetch the data
    data = cur.fetchall()

    # Close the cursor
    cur.close()

    # Close the connection
    conn.close()

    # Create a DataFrame
    df = pd.DataFrame(data, columns=colnames)

    # Return DataFrame
    return df

############################################################################
# Data Caching Functions
# Get SPX Info
@st.cache_data
def get_spx_info(host, user, password, database, port):
    with st.spinner('Loading SPX Info...'):
        query = "SELECT * FROM spx.info ORDER BY symbol"
        df_info = postgresql(query, host, user, password, database, port)
        # Convert founded to int
        df_info['founded'] = df_info['founded'].astype(int)
        # Convert cik to str
        df_info['cik'] = df_info['cik'].astype(str)
        return df_info

# Get SPX Prices                                                                     
@st.cache_data                                                                        
def get_spx_prices(symbols, host, user, password, database, port, metrics=['Close']):
    with st.spinner('Loading SPX Prices...'):                                         
        symbols_str = ", ".join(f"'{symbol}'" for symbol in symbols)
        query = f"SELECT * FROM spx.prices WHERE Ticker IN ({symbols_str}) AND ("           
        for metric in metrics:                                                        
            query += f"Metric = '{metric}' OR "                                       
        query = query[:-4] + ")"                                                      
        df_prices = postgresql(query, host, user, password, database, port)           
        df_prices['date'] = pd.to_datetime(df_prices['date'])                         
        return df_prices

# Get SPX Financials
@st.cache_data
def get_spx_financials(symbols, host, user, password, database, port):
    with st.spinner('Loading SPX Financials...'):
        symbols_str = ", ".join(f"'{symbol}'" for symbol in symbols)
        query = f"SELECT * FROM spx.financials WHERE ticker IN ({symbols_str})"
        df_financials = postgresql(query, host, user, password, database, port)
        df_financials['date'] = pd.to_datetime(df_financials['date'])
        return df_financials

############################################################################
# Load SPX Info
df_info = get_spx_info(host, user, password, database, port)

############################################################################
# Create Filters
col1, col2, col3, col4, = st.columns(4)

with col1:
    # Multi Select for gics_sector
    sector = st.multiselect('Sector', df_info['gics_sector'].unique(), [])
with col2:
    # Multi Select for gics_sub_industry
    sub_industry = st.multiselect('Sub Industry', df_info['gics_sub_industry'].unique(), [])
with col3:
    # Multi Select for headquarters_location
    location = st.multiselect('Location', df_info['headquarters_location'].unique(), [])
with col4:
    # Slider for Data Range
    min_value, max_value = df_info['founded'].min(), df_info['founded'].max()
    # Slider for Founded
    founded = st.slider('Founded', min_value, max_value, [min_value, max_value])

############################################################################
# Apply Filters
if sector != []:
    df_info = df_info[df_info['gics_sector'].isin(sector)]
if sub_industry != []:
    df_info = df_info[df_info['gics_sub_industry'].isin(sub_industry)]
if location != []:
    df_info = df_info[df_info['headquarters_location'].isin(location)]
if founded != [min_value, max_value]:
    df_info = df_info[(df_info['founded'] >= founded[0]) & (df_info['founded'] <= founded[1])]

df_filtered = df_info

############################################################################
# Display Filtered DataFrame
df_filtered['founded'] = df_filtered['founded'].astype(str)
st.dataframe(df_filtered, use_container_width=True)

# Get the first three tickers
try:
    ticker_list = df_filtered['symbol'].unique()[:3]
    symbols = st.multiselect('Symbol', df_filtered['symbol'].unique(), ticker_list)
except:
    symbols = st.multiselect('Symbol', df_filtered['symbol'].unique(), [])

if symbols != []:
    df_filtered = df_filtered[df_filtered['symbol'].isin(symbols)]
elif symbols == []:
    symbols = [df_filtered['symbol'].iloc[0]]

############################################################################
# Load SPX Prices
df_close = get_spx_prices(symbols, host, user, password, database, port, metrics=['Close'])
df_open = get_spx_prices(symbols, host, user, password, database, port, metrics=['Open'])
df_high = get_spx_prices(symbols, host, user, password, database, port, metrics=['High'])
df_low = get_spx_prices(symbols, host, user, password, database, port, metrics=['Low'])
df_volume = get_spx_prices(symbols, host, user, password, database, port, metrics=['Volume'])

############################################################################
# Load SPX Financials
df_financials = get_spx_financials(symbols, host, user, password, database, port)

############################################################################

############################################################################
col1, col2 = st.columns(2)
with col1:
    # Visualize SPX Metrics
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Close", "Open", "High", "Low", "Volume"])

    def visualize_metric(df, metric):
        fig = px.line(df, x='date', y='value', color='ticker')
        # Add Title
        fig.update_layout(title=f'{metric} Prices')
        st.plotly_chart(fig, use_container_width=True)

    with tab1:
        visualize_metric(df_close, 'Close')
    with tab2:
        visualize_metric(df_open, 'Open')
    with tab3:
        visualize_metric(df_high, 'High')
    with tab4:
        visualize_metric(df_low, 'Low')
    with tab5:
        visualize_metric(df_volume, 'Volume')

############################################################################
# Visualize SPX Financials
with col2:
    # Filter for SPX Financials
    sorted_unique = df_financials['variable'].sort_values().unique()
    # Get the index of "Total Revenue"
    index_num = [i for i, j in enumerate(sorted_unique) if j == 'Total Revenue'][0]
    variable = st.selectbox('Value', df_financials['variable'].sort_values().unique(), index=index_num)
    # Filter DataFrame
    df_financials = df_financials[df_financials['variable'] == variable]
    # Plot SPX Financials
    fig = px.bar(df_financials, x='date', y='value', color='ticker')
    st.plotly_chart(fig, use_container_width=True)
