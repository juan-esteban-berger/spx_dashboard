import { useState, useEffect, useMemo } from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Company, Price, Financial, FilterOptions } from '@/types/interfaces';
import { fetchFilterOptions, fetchCompanyData, fetchPriceData, fetchFinancialsData } from '@/services/api';
import { StatsCards } from '@/components/dashboard/StatsCards';
import { Filters } from '@/components/dashboard/Filters';
import { CompanyGrid } from '@/components/dashboard/CompanyGrid';
import { PriceSection } from '@/components/dashboard/PriceSection';
import { FinancialsSection } from '@/components/dashboard/FinancialsSection';
import { filterCompanies } from '@/utils/filteringUtils';

{/*****************************************************************************/}
{/*****************************************************************************/}
{/*****************************************************************************/}
{/* Main Dashboard Component */}
const App = () => {
  {/* State Management */}
  // Main data states for companies and their stock prices
  const [infoData, setInfoData] = useState<Company[]>([]);
  const [pricesData, setPricesData] = useState<Price[]>([]);
  const [financialsData, setFinancialsData] = useState<Financial[]>([]);
  
  // Filter options available for selection
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    symbols: [],
    sectors: [],
    subIndustries: [],
    locations: [],
    foundedRange: {
      min: 0,
      max: 0
    }
  });
  
  // Currently selected filter values
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>([]);
  const [selectedSectors, setSelectedSectors] = useState<string[]>([]);
  const [selectedSubIndustries, setSelectedSubIndustries] = useState<string[]>([]);
  const [selectedTicker, setSelectedTicker] = useState<string>('');
  const [selectedLocations, setSelectedLocations] = useState<string[]>([]);
  const [minYear, setMinYear] = useState<number | null>(null);
  const [maxYear, setMaxYear] = useState<number | null>(null);
  
  // UI state management
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  {/*****************************************************************************/}
  {/* Memoized Filtered Data */}
  const filteredCompanies = useMemo(() => {
    return filterCompanies(infoData, {
      selectedSymbols,
      selectedSectors,
      selectedSubIndustries,
      selectedLocations,
      minYear,
      maxYear,
    });
  }, [infoData, selectedSymbols, selectedSectors, selectedSubIndustries, selectedLocations, minYear, maxYear]);

  {/*****************************************************************************/}
  {/*****************************************************************************/}
  {/*****************************************************************************/}
  {/* Data Fetching Effects */}

  // Initial data load - fetches filter options and company data on component mount
  useEffect(() => {
    const initializeData = async () => {
      try {
        const options = await fetchFilterOptions();
        setFilterOptions(options);
        const data = await fetchCompanyData([], [], []);
        setInfoData(data);
      } catch (error) {
        console.error('Error initializing data:', error);
        setError(`Failed to initialize data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    };
    initializeData();
  }, []);

  // Fetches price data when a specific ticker is selected
  useEffect(() => {
    const loadPriceData = async () => {
      if (!selectedTicker) return;
      setLoading(true);
      try {
        const data = await fetchPriceData(selectedTicker);
        setPricesData(data);
      } catch (error) {
        console.error('Error loading price data:', error);
        setError(`Failed to load price data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };
    loadPriceData();
  }, [selectedTicker]);

  // Fetches financials data when a specific ticker is selected
  useEffect(() => {
    const loadFinancialsData = async () => {
      if (!selectedTicker) return;
      setLoading(true);
      try {
        const data = await fetchFinancialsData(selectedTicker);
        setFinancialsData(data);
      } catch (error) {
        console.error('Error loading financials data:', error);
        setError(`Failed to load financials data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };
    loadFinancialsData();
  }, [selectedTicker]);

  {/*****************************************************************************/}
  {/*****************************************************************************/}
  {/*****************************************************************************/}
  {/* Component Render */}
  return (
    <div className="p-4 pt-20">
      {/* Dashboard Header */}
      <h1 className="text-5xl font-bold mb-6 text-center">S&P 500 Dashboard</h1>
      
      {/* Filter Selection Section */}
      <Filters
        filterOptions={filterOptions}
        selectedSymbols={selectedSymbols}
        selectedSectors={selectedSectors}
        selectedSubIndustries={selectedSubIndustries}
        selectedLocations={selectedLocations}
        minYear={minYear}
        maxYear={maxYear}
        setSelectedSymbols={setSelectedSymbols}
        setSelectedSectors={setSelectedSectors}
        setSelectedSubIndustries={setSelectedSubIndustries}
        setSelectedLocations={setSelectedLocations}
        setMinYear={setMinYear}
        setMaxYear={setMaxYear}
      />

      {/* Statistics Overview Cards */}
      <StatsCards companies={filteredCompanies} />

      {/* Loading and Error States */}
      {loading && (
        <div className="text-gray-600 mb-4">Loading data...</div>
      )}
      
      {error && (
        <div className="text-red-600 mb-4 p-2 border border-red-300 rounded">
          {error}
        </div>
      )}

      {/* Main Company Data Grid */}
      <CompanyGrid 
        companies={filteredCompanies}
        selectedSymbols={selectedSymbols}
        selectedSectors={selectedSectors}
        selectedSubIndustries={selectedSubIndustries}
        selectedLocations={selectedLocations}
        minYear={minYear}
        maxYear={maxYear}
      />

      {/* Debug Section for Price Data */}
      <PriceSection
        filterOptions={filterOptions}
        selectedTicker={selectedTicker}
        setSelectedTicker={setSelectedTicker}
        pricesData={pricesData}
        loading={loading}
      />

      {/* Debug Section for Financials Data */}
      <FinancialsSection
        filterOptions={filterOptions}
        selectedTicker={selectedTicker}
        setSelectedTicker={setSelectedTicker}
        financialsData={financialsData}
        loading={loading}
      />
    </div>
  );
};

export default App;
