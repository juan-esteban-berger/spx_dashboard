import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import pymssql
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

########################################################################
# Page Configuration
# wide mode
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

########################################################################
# Database Credentials
server = os.getenv('server')
port = os.getenv('port')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')

def mssql(sql_query, server, user, password, database, port):
    # Connect to the database
    conn = pymssql.connect(server, user, password, database, port=port,
                           tds_version='7.0')
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch data for SELECT queries
    batch_size = 1000
    rows = cursor.fetchmany(batch_size)
    data = []

    while rows:
        data.extend(rows)
        rows = cursor.fetchmany(batch_size)

    # Load into a DataFrame
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])

   # Close the connection
    cursor.close()
    conn.close()

    # Return DataFrame
    return df

########################################################################
# Data Caching Functions

# Get SPX Info
@st.cache_data
def get_spx_info(server, user, password, database, port):
    with st.spinner('Loading SPX Info...'):
        query = "SELECT * FROM spx.info"
        df_info = mssql(query, server, user, password, database, port)
        # Rename Date_added to Date_Added
        df_info = df_info.rename(columns={'Date_added': 'Date_Added'})
        # Convert Date_Added to datetime
        df_info['Date_Added'] = pd.to_datetime(df_info['Date_Added'])
        return df_info

# Get SPX Prices
@st.cache_data
def get_spx_prices(symbol, server, user, password, database, port, metrics=['Close']):
    with st.spinner('Loading SPX Prices...'):
        query = f"SELECT * FROM spx.prices WHERE Ticker = '{symbol}' AND ("
        for metric in metrics:
            query += f"Metric = '{metric}' OR "
        query = query[:-4] + ")"

        df_prices = mssql(query, server, user, password, database, port)
        return df_prices

# Get SPX Financials
@st.cache_data
def get_spx_financials(server, user, password, database, port):
    with st.spinner('Loading SPX Financials...'):
        query = "SELECT * FROM spx.financials"
        df_financials = mssql(query, server, user, password, database, port)
        return df_financials

########################################################################
# Title
# H1 Centered HTML Title
st.markdown("<h1 style='text-align: center;'>S&P 500 Stocks Analysis</h1>", unsafe_allow_html=True)

########################################################################
# Source SPX Info
df_info = get_spx_info(server, user, password, database, port)

########################################################################
# Create Filters
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Symbol Filter
    symbols = st.multiselect('Select Symbols:', df_info['Symbol'].sort_values().unique())
    # Headquarters_Location Filter
    headquarters_locations = st.multiselect('Select Headquarters Locations:', df_info['Headquarters_Location'].sort_values().unique())

with col2:
    # Security Filter
    securities = st.multiselect('Select Securities:', df_info['Security'].sort_values().unique())
    # Date_Added Filter (Date Range)
    min_date_added = df_info['Date_Added'].min()
    min_date_added = datetime(min_date_added.year, min_date_added.month, min_date_added.day)
    max_date_added = df_info['Date_Added'].max()
    max_date_added = datetime(max_date_added.year, max_date_added.month, max_date_added.day)
    date_added_range = st.date_input('Select Date Added Range:', [min_date_added, max_date_added])

with col3:
    # GICS_Sector Filter
    gics_sectors = st.multiselect('Select GICS Sectors:', df_info['GICS_Sector'].sort_values().unique())
    # CIK Filter
    ciks = st.multiselect('Select CIKs:', df_info['CIK'].sort_values().unique())

with col4:
    # GICS_Sub_Industry Filter
    gics_sub_industries = st.multiselect('Select GICS Sub Industries:', df_info['GICS_Sub_Industry'].sort_values().unique())
    # Founded Filter (multiselect)
    founded_years = st.multiselect('Select Founded Years:', df_info['Founded'].sort_values().unique())

########################################################################
# Apply Filters
if symbols != []:
    df_info = df_info[df_info['Symbol'].isin(symbols)]
if securities != []:
    df_info = df_info[df_info['Security'].isin(securities)]
if gics_sectors != []:
    df_info = df_info[df_info['GICS_Sector'].isin(gics_sectors)]
if gics_sub_industries != []:
    df_info = df_info[df_info['GICS_Sub_Industry'].isin(gics_sub_industries)]
if headquarters_locations != []:
    df_info = df_info[df_info['Headquarters_Location'].isin(headquarters_locations)]
if date_added_range != [min_date_added, max_date_added]:
    first_date_added = date_added_range[0]
    first_date_added = datetime(first_date_added.year, first_date_added.month, first_date_added.day)
    last_date_added = date_added_range[1]
    last_date_added = datetime(last_date_added.year, last_date_added.month, last_date_added.day)
    df_info = df_info[(df_info['Date_Added'] >= first_date_added) & (df_info['Date_Added'] <= last_date_added)]
if ciks != []:
    df_info = df_info[df_info['CIK'].isin(ciks)]
if founded_years != []:
    df_info = df_info[df_info['Founded'].isin(founded_years)]

########################################################################
# Display SPX Info
st.dataframe(df_info, use_container_width=True)

########################################################################
# Source SPX Prices
# Get the First Symbol in the Filtered Dataframe
symbol = df_info['Symbol'].iloc[0]
# Multi Select Filter for Metrics: High, Low, Open, Close, Volume
metrics_list = ['High', 'Low', 'Open', 'Close', 'Volume']
metrics = st.multiselect('Select Metrics:', metrics_list, default=['Close'])
if metrics == []:
    metrics = ['Close']
df_prices = get_spx_prices(symbol, server, user, password, database, port, metrics)

########################################################################
# Line Chart (colored by Metric)
fig = px.line(df_prices, x='Date',
                         y='Value',
                         color='Metric',
                         title=f'{symbol} Metrics')
# Add Legend
fig.update_layout(legend_title_text='Metric')
st.plotly_chart(fig, use_container_width=True)

########################################################################
# Source SPX Financials
df_financials = get_spx_financials(server, user, password, database, port)
st.dataframe(df_financials, use_container_width=True)
