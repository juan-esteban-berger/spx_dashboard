import { FilterOptions } from '@/types/interfaces';
import { MultiSelect } from '@/components/custom/multi-select';

{/*****************************************************************************/}
{/* Interface Definitions */}

interface FiltersProps {
  filterOptions: FilterOptions;      // Available options for all filters
  selectedSymbols: string[];         // Currently selected stock symbols
  selectedSectors: string[];         // Currently selected sectors
  selectedSubIndustries: string[];   // Currently selected sub-industries
  setSelectedSymbols: (symbols: string[]) => void;           // Update symbol selections
  setSelectedSectors: (sectors: string[]) => void;           // Update sector selections
  setSelectedSubIndustries: (subIndustries: string[]) => void; // Update sub-industry selections
}

{/*****************************************************************************/}
{/* Filters Component */}
// Provides a filter interface for S&P 500 companies using three multi-select dropdowns
export const Filters = ({
  filterOptions,
  selectedSymbols,
  selectedSectors,
  selectedSubIndustries,
  setSelectedSymbols,
  setSelectedSectors,
  setSelectedSubIndustries
}: FiltersProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Stock Symbol Filter */}
      <MultiSelect
        options={filterOptions.symbols.map(symbol => ({
          label: symbol,
          value: symbol
        }))}
        selected={selectedSymbols.map(symbol => ({
          label: symbol,
          value: symbol
        }))}
        onChange={values => setSelectedSymbols(values.map(v => v.value))}
        placeholder="Select symbols..."
        className="w-full"
      />
      
      {/* Sector Filter */}
      <MultiSelect
        options={filterOptions.sectors.map(sector => ({
          label: sector,
          value: sector
        }))}
        selected={selectedSectors.map(sector => ({
          label: sector,
          value: sector
        }))}
        onChange={values => setSelectedSectors(values.map(v => v.value))}
        placeholder="Select sectors..."
        className="w-full"
      />
      
      {/* Sub-Industry Filter */}
      <MultiSelect
        options={filterOptions.subIndustries.map(subIndustry => ({
          label: subIndustry,
          value: subIndustry
        }))}
        selected={selectedSubIndustries.map(subIndustry => ({
          label: subIndustry,
          value: subIndustry
        }))}
        onChange={values => setSelectedSubIndustries(values.map(v => v.value))}
        placeholder="Select sub-industries..."
        className="w-full"
      />
    </div>
  );
};
