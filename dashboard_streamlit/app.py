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

# Get the first ticker in a list
symbols = [df_info['symbol'].iloc[0]]
# Load SPX Prices to get the dates
df_close = get_spx_prices(symbols, host, user, password, database, port, metrics=['Close'])
earliest_date = df_close['date'].min()
# Format as MM-DD-YY (Only two digits for year)
earliest_date = earliest_date.strftime('%m-%d-%y')
latest_date = df_close['date'].max()
latest_date = latest_date.strftime('%m-%d-%y')

############################################################################
col1, col2, col3, col4 = st.columns(4)
with col1:
    # Metric for Number of Unique Tickers
    st.metric(label='Unique Tickers', value=df_info['symbol'].nunique())
with col2:
    # Metric for Number of Unique Sectors
    st.metric(label='Unique Sectors', value=df_info['gics_sector'].nunique())
with col3:
    # Metric for Earliest Date
    st.metric(label='Earliest Date', value=earliest_date)
with col4:
    # Metric for Latest Date
    st.metric(label='Latest Date', value=latest_date)

############################################################################
# Get the first three tickers
try:
    ticker_list = df_info['symbol'].unique()[:3]
    symbols = st.multiselect('Select Tickers to Visualize', df_info['symbol'].unique(), ticker_list)
except:
    symbols = st.multiselect('Select Tickers to Visualize', df_info['symbol'].unique(), [])

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
# Create Filters
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
    variable = st.selectbox('Select Financial Record', df_financials['variable'].sort_values().unique(), index=index_num)
    # Filter DataFrame
    df_financials = df_financials[df_financials['variable'] == variable]
    # Plot SPX Financials
    fig = px.bar(df_financials, x='date', y='value', color='ticker')
    st.plotly_chart(fig, use_container_width=True)

############################################################################
# H2 Title
st.markdown('<h3 style="text-align: center;">S&P 500 Dataset Information</h3>', unsafe_allow_html=True)
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

# Display Filtered DataFrame
df_info['founded'] = df_info['founded'].astype(str)
st.dataframe(df_info, use_container_width=True)

############################################################################
tab1, tab2, tab3 = st.tabs(["GICS Sector", "GICS Sub Industry", "Headquarters Location"])
with tab1:
    # Bar Chart for GICS Sector
    df_pivot = df_info['gics_sector'].value_counts().reset_index()
    df_pivot.columns = ['gics_sector', 'count']
    # Color by Gics Sector
    fig = px.bar(df_pivot, x='gics_sector', y='count', title='GICS Sector Counts',
                    color='gics_sector')
    # Sort x axis
    fig.update_xaxes(categoryorder='total descending')
    # Add Data Labels
    fig.update_traces(texttemplate='%{value}', textposition='outside')
    # Increae Height
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    # Bar Chart for Top 20 GICS Sub Industry
    df_pivot = df_info.groupby(['gics_sector', 'gics_sub_industry']).size().reset_index()
    df_pivot.columns = ['gics_sector', 'gics_sub_industry', 'count']
    df_pivot = df_pivot.sort_values('count', ascending=False).head(20)

    # Color by Gics Sector
    fig = px.bar(df_pivot, x='gics_sub_industry', y='count', title='Top 20 GICS Sub Industry Counts',
                    color='gics_sector')
    # Sort x axis
    fig.update_xaxes(categoryorder='total descending')
    # Add Data Labels
    fig.update_traces(texttemplate='%{value}', textposition='outside')
    # Increase Height
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
with tab3:
    # Bar Chart for Top 10 Headquarters Location
    df_pivot = df_info['headquarters_location'].value_counts().reset_index()
    df_pivot.columns = ['headquarters_location', 'count']
    df_pivot = df_pivot.sort_values('count', ascending=False).head(10)
    # Color by Headquarters Location
    fig = px.bar(df_pivot, x='headquarters_location', y='count', title='Top 10 Headquarters Location Counts',
                    color='headquarters_location')
    # Sort x axis
    fig.update_xaxes(categoryorder='total descending')
    # Add Data Labels
    fig.update_traces(texttemplate='%{value}', textposition='outside')
    # Increase Height
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

############################################################################
col1, col2 = st.columns(2)
with col1:
    # Histogram of founded
    fig = px.histogram(df_info, x='founded', title='Distribution of Founding Dates')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Histogram of date_added
    fig = px.histogram(df_info, x='date_added', title='Distribution of Date Added')
    st.plotly_chart(fig, use_container_width=True)
