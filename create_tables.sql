-- create schema
CREATE SCHEMA IF NOT EXISTS spx;

-- create table info
CREATE TABLE spx.info
(
  symbol varchar(255),
  security varchar(255),
  gics_sector varchar(255),
  gics_sub_industry varchar(255),
  headquarters_location varchar(255),
  date_added date,
  cik integer,
  founded varchar(255)
);

-- create index for table info
CREATE INDEX IX_info ON spx.info (symbol);

-- create table prices
CREATE TABLE spx.prices 
(
  date date,
  ticker varchar(255),
  metric varchar(255),
  value float
);

-- create index for table prices
CREATE INDEX IX_prices ON spx.prices (ticker, metric, date);

-- create table financials
CREATE TABLE spx.financials 
(
  ticker varchar(255),
  date date,
  variable varchar(255),
  value float
);

-- create index for table financials
CREATE INDEX IX_financials ON spx.financials (ticker, date);

-- Create views with IDs for Django
-- Info view with ID
CREATE OR REPLACE VIEW spx.info_view AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY symbol) as id,
    symbol,
    security,
    gics_sector,
    gics_sub_industry,
    headquarters_location,
    date_added,
    cik,
    founded
FROM spx.info;

-- Prices view with ID
CREATE OR REPLACE VIEW spx.prices_view AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY date, ticker, metric) as id,
    date,
    ticker,
    metric,
    value
FROM spx.prices;

-- Financials view with ID
CREATE OR REPLACE VIEW spx.financials_view AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY ticker, date, variable) as id,
    ticker,
    date,
    variable,
    value
FROM spx.financials;
