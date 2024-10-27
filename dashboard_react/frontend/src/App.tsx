import { useState, useEffect, useMemo } from 'react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Company, Price, Financial, FilterOptions } from '@/types/interfaces';
import { fetchFilterOptions, fetchCompanyData, fetchPriceData, fetchFinancialsData } from '@/services/api';
import { StatsCards } from '@/components/dashboard/StatsCards';
import { Filters } from '@/components/dashboard/Filters';
import { CompanyGrid } from '@/components/dashboard/CompanyGrid';
import { CombinedDataSection } from '@/components/dashboard/CombinedDataSection';
import { filterCompanies } from '@/utils/filteringUtils';
import { AlertDialog, AlertDialogContent } from "@/components/ui/alert-dialog";
import { Loader2 } from "lucide-react";

{/*****************************************************************************/}
{/* Main Dashboard Component */}
const App = () => {
  {/*****************************************************************************/}
  {/* State Management */}
  // Initialization state
  const [initializing, setInitializing] = useState(true);

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
  const [selectedTicker, setSelectedTicker] = useState<string>('AAPL');
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
  {/* Data Fetching Effects */}

  // Initial data load with loading dialog
  useEffect(() => {
    const initializeData = async () => {
      setInitializing(true);
      try {
        // Fetch initial data in parallel
        const [options, data] = await Promise.all([
          fetchFilterOptions(),
          fetchCompanyData([], [], [])
        ]);

        setFilterOptions(options);
        setInfoData(data);

        // Fetch initial prices and financials for AAPL
        const [prices, financials] = await Promise.all([
          fetchPriceData('AAPL'),
          fetchFinancialsData('AAPL')
        ]);

        setPricesData(prices);
        setFinancialsData(financials);
      } catch (error) {
        console.error('Error initializing data:', error);
        setError(`Failed to initialize data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      } finally {
        setInitializing(false);
      }
    };
    initializeData();
  }, []);

  // Fetches price data when a specific ticker is selected
  useEffect(() => {
    const loadPriceData = async () => {
      if (!selectedTicker || initializing) return;
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
  }, [selectedTicker, initializing]);

  // Fetches financials data when a specific ticker is selected
  useEffect(() => {
    const loadFinancialsData = async () => {
      if (!selectedTicker || initializing) return;
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
  }, [selectedTicker, initializing]);

  {/*****************************************************************************/}
  {/* Component Render */}
  return (
    <>
      {/* Loading Dialog */}
      <AlertDialog open={initializing}>
        <AlertDialogContent className="flex flex-col items-center justify-center gap-4 sm:max-w-[425px]">
          <div className="flex items-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <h2 className="text-xl font-semibold">Loading Historical S&P 500 Data...</h2>
          </div>
        </AlertDialogContent>
      </AlertDialog>

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

        {/* Combined Data Section */}
        <CombinedDataSection
          filterOptions={filterOptions}
          selectedTicker={selectedTicker}
          setSelectedTicker={setSelectedTicker}
          pricesData={pricesData}
          financialsData={financialsData}
          loading={loading}
        />
      </div>
    </>
  );
};

export default App;
