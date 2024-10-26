import { useState, useEffect } from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Company, Price, Financial, FilterOptions } from '@/types/interfaces';
import { fetchFilterOptions, fetchCompanyData, fetchPriceData, fetchFinancialsData } from '@/services/api';
import { StatsCards } from '@/components/dashboard/StatsCards';
import { Filters } from '@/components/dashboard/Filters';
import { CompanyGrid } from '@/components/dashboard/CompanyGrid';
import { DebugPriceData } from '@/components/dashboard/DebugPriceData';
import { DebugFinancialsData } from '@/components/dashboard/DebugFinancialsData';

{/*****************************************************************************/}
{/*****************************************************************************/}
{/*****************************************************************************/}
{/* Main Dashboard Component */}
function App() {
  {/* State Management */}
  // Main data states for companies and their stock prices
  const [infoData, setInfoData] = useState<Company[]>([]);
  const [pricesData, setPricesData] = useState<Price[]>([]);
  const [financialsData, setFinancialsData] = useState<Financial[]>([]);
  
  // Filter options available for selection
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    symbols: [],
    sectors: [],
    subIndustries: []
  });
  
  // Currently selected filter values
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>([]);
  const [selectedSectors, setSelectedSectors] = useState<string[]>([]);
  const [selectedSubIndustries, setSelectedSubIndustries] = useState<string[]>([]);
  const [selectedTicker, setSelectedTicker] = useState<string>('');
  
  // UI state management
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  // Fetches company data whenever filters change
  useEffect(() => {
    const loadCompanyData = async () => {
      setLoading(true);
      try {
        const data = await fetchCompanyData(selectedSymbols, selectedSectors, selectedSubIndustries);
        setInfoData(data);
      } catch (error) {
        console.error('Error loading company data:', error);
        setError(`Failed to load company data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };
    loadCompanyData();
  }, [selectedSymbols, selectedSectors, selectedSubIndustries]);

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
    <div className="p-4">
      {/* Dashboard Header */}
      <h1 className="text-3xl font-bold mb-6 text-center">S&P 500 Dashboard</h1>
      
      {/* Statistics Overview Cards */}
      <StatsCards companies={infoData} />
      
      {/* Filter Selection Section */}
      <Filters
        filterOptions={filterOptions}
        selectedSymbols={selectedSymbols}
        selectedSectors={selectedSectors}
        selectedSubIndustries={selectedSubIndustries}
        setSelectedSymbols={setSelectedSymbols}
        setSelectedSectors={setSelectedSectors}
        setSelectedSubIndustries={setSelectedSubIndustries}
      />

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
      <CompanyGrid companies={infoData} />

      {/* Debug Section for Price Data */}
      <DebugPriceData
        filterOptions={filterOptions}
        selectedTicker={selectedTicker}
        setSelectedTicker={setSelectedTicker}
        pricesData={pricesData}
        loading={loading}
      />

      {/* Debug Section for Financials Data */}
      <DebugFinancialsData
        filterOptions={filterOptions}
        selectedTicker={selectedTicker}
        setSelectedTicker={setSelectedTicker}
        financialsData={financialsData}
        loading={loading}
      />
    </div>
  );
}

export default App;
