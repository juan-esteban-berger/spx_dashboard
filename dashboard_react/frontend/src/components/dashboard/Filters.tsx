import { FilterOptions } from '@/types/interfaces';
import { MultiSelect } from '@/components/custom/multi-select';
import { useState, KeyboardEvent } from 'react';

interface FiltersProps {
  filterOptions: FilterOptions;
  selectedSymbols: string[];
  selectedSectors: string[];
  selectedSubIndustries: string[];
  selectedLocations: string[];        
  minYear: number | null;
  maxYear: number | null;
  setSelectedSymbols: (symbols: string[]) => void;
  setSelectedSectors: (sectors: string[]) => void;
  setSelectedSubIndustries: (subIndustries: string[]) => void;
  setSelectedLocations: (locations: string[]) => void;     
  setMinYear: (year: number | null) => void;
  setMaxYear: (year: number | null) => void;
}

export const Filters = ({
  filterOptions,
  selectedSymbols,
  selectedSectors,
  selectedSubIndustries,
  selectedLocations,
  minYear,
  maxYear,
  setSelectedSymbols,
  setSelectedSectors,
  setSelectedSubIndustries,
  setSelectedLocations,
  setMinYear,
  setMaxYear,
}: FiltersProps) => {
  const [minYearInput, setMinYearInput] = useState(minYear?.toString() || '');
  const [maxYearInput, setMaxYearInput] = useState(maxYear?.toString() || '');

  const handleYearKeyPress = (
    e: KeyboardEvent<HTMLInputElement>,
    setYear: (year: number | null) => void,
    value: string
  ) => {
    if (e.key === 'Enter') {
      const yearValue = parseInt(value);
      if (!isNaN(yearValue) && yearValue > 0) {
        setYear(yearValue);
      } else {
        setYear(null);
      }
    }
  };

  const handleYearBlur = (
    value: string,
    setYear: (year: number | null) => void
  ) => {
    const yearValue = parseInt(value);
    if (!isNaN(yearValue) && yearValue > 0) {
      setYear(yearValue);
    } else {
      setYear(null);
    }
  };

  return (
    <div className="grid grid-cols-6 gap-4 mb-6">
      {/* Symbol Filter */}
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

      {/* Location Filter */}
      <MultiSelect
        options={filterOptions.locations.map(location => ({
          label: location,
          value: location
        }))}
        selected={selectedLocations.map(location => ({
          label: location,
          value: location
        }))}
        onChange={values => setSelectedLocations(values.map(v => v.value))}
        placeholder="Select locations..."
        className="w-full"
      />

      {/* Min Year Text Input */}
      <input
        type="text"
        placeholder="Min Founded Year..."
        value={minYearInput}
        onChange={(e) => setMinYearInput(e.target.value)}
        onKeyDown={(e) => handleYearKeyPress(e, setMinYear, minYearInput)}
        onBlur={() => handleYearBlur(minYearInput, setMinYear)}
        className="rounded-md border border-input px-3 py-2 text-sm w-full"
      />

      {/* Max Year Text Input */}
      <input
        type="text"
        placeholder="Max Founded Year..."
        value={maxYearInput}
        onChange={(e) => setMaxYearInput(e.target.value)}
        onKeyDown={(e) => handleYearKeyPress(e, setMaxYear, maxYearInput)}
        onBlur={() => handleYearBlur(maxYearInput, setMaxYear)}
        className="rounded-md border border-input px-3 py-2 text-sm w-full"
      />
    </div>
  );
};