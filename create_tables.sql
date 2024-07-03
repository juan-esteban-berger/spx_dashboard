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
