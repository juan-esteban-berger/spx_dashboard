import { Company } from '@/types/interfaces';

export const filterCompanies = (
  companies: Company[],
  {
    selectedSymbols,
    selectedSectors,
    selectedSubIndustries,
    selectedLocations,
    minYear,
    maxYear,
  }: {
    selectedSymbols: string[];
    selectedSectors: string[];
    selectedSubIndustries: string[];
    selectedLocations: string[];
    minYear: number | null;
    maxYear: number | null;
  }
) => {
  return companies.filter(company => {
    // Symbol filter
    if (selectedSymbols.length > 0 && !selectedSymbols.includes(company.symbol)) {
      return false;
    }

    // Sector filter
    if (selectedSectors.length > 0 && !selectedSectors.includes(company.gics_sector)) {
      return false;
    }

    // Sub-industry filter
    if (selectedSubIndustries.length > 0 && !selectedSubIndustries.includes(company.gics_sub_industry)) {
      return false;
    }

    // Location filter
    if (selectedLocations.length > 0 && !selectedLocations.includes(company.headquarters_location)) {
      return false;
    }

    // Year range filter
    const foundedYear = parseInt(company.founded);
    if (!isNaN(foundedYear)) {
      if (minYear !== null && foundedYear < minYear) {
        return false;
      }
      if (maxYear !== null && foundedYear > maxYear) {
        return false;
      }
    }

    return true;
  });
};
