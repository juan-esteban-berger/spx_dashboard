import { Company, Price, FilterOptions, Financial } from '@/types/interfaces';

{/*****************************************************************************/}
{/* Filter Options API */}
/**
 * Fetches available filter options (symbols, sectors, sub-industries)
 * Endpoint: GET /api/info/filter_options/
 */
export const fetchFilterOptions = async (): Promise<FilterOptions> => {
  const response = await fetch('/api/info/filter_options/');
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
};

{/*****************************************************************************/}
{/* Company Data API */}
/**
 * Fetches company information based on selected filters
 * Endpoint: GET /api/info/?symbols[]=...&sectors[]=...&subIndustries[]=...
 */
export const fetchCompanyData = async (
  selectedSymbols: string[],
  selectedSectors: string[],
  selectedSubIndustries: string[]
): Promise<Company[]> => {
  // Build URL with query parameters
  let url = '/api/info/?';
  
  // Add selected symbols to URL if any
  if (selectedSymbols.length) {
    selectedSymbols.forEach(symbol => {
      url += `symbols[]=${encodeURIComponent(symbol)}&`;
    });
  }

  // Add selected sectors to URL if any
  if (selectedSectors.length) {
    selectedSectors.forEach(sector => {
      url += `sectors[]=${encodeURIComponent(sector)}&`;
    });
  }

  // Add selected sub-industries to URL if any
  if (selectedSubIndustries.length) {
    selectedSubIndustries.forEach(subIndustry => {
      url += `subIndustries[]=${encodeURIComponent(subIndustry)}&`;
    });
  }
  
  // Fetch and return company data
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
};

{/*****************************************************************************/}
{/* Price Data API */}
/**
 * Fetches price data for a specific symbol
 * Endpoint: GET /api/prices/?symbols[]=SYMBOL&metric=Close
 */
export const fetchPriceData = async (symbol: string): Promise<Price[]> => {
  // Return empty array if no symbol provided
  if (!symbol) return [];

  // Fetch price data for the symbol
  const response = await fetch(`/api/prices/?symbols[]=${symbol}&metric=Close`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
};

{/*****************************************************************************/}
{/* Financial Data API */}
/**
 * Fetches financial data for a specific symbol
 * Endpoint: GET /api/financials/?symbols[]=SYMBOL
 */
export const fetchFinancialsData = async (symbol: string): Promise<Financial[]> => {
  // Return empty array if no symbol provided
  if (!symbol) return [];

  // Fetch financial data for the symbol with custom error handling
  try {
    const response = await fetch(`/api/financials/?symbols[]=${symbol}`);
    if (!response.ok) {
      if (response.status === 500) {
        // If we get a 500 error, return an empty array instead of throwing
        console.warn(`Server error fetching financials for ${symbol}, returning empty array`);
        return [];
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    // Log the error but don't throw it
    console.error(`Error fetching financials for ${symbol}:`, error);
    // Return empty array instead of throwing
    return [];
  }
};
