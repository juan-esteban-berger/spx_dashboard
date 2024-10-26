export interface Company {
  symbol: string;
  security: string;
  gics_sector: string;
  gics_sub_industry: string;
  headquarters_location: string;
  date_added: string;
  cik: number;
  founded: string;
}

export interface Price {
  date: string;
  ticker: string;
  metric: string;
  value: number;
}

export interface Financial {
  date: string;
  ticker: string;
  variable: string;
  value: number;
}

export interface FilterOptions {
  symbols: string[];
  sectors: string[];
  subIndustries: string[];
}
