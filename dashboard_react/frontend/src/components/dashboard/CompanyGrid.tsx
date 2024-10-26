import { useCallback, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { GridReadyEvent } from 'ag-grid-community';
import { Company } from '@/types/interfaces';
import { infoColumns } from './CompanyGridColumns';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CompanyGridProps {
  companies: Company[];
  selectedSymbols: string[];
  selectedSectors: string[];
  selectedSubIndustries: string[];
  selectedLocations: string[];
  minYear: number | null;
  maxYear: number | null;
}

export const CompanyGrid = ({
  companies,
  selectedSymbols,
  selectedSectors,
  selectedSubIndustries,
  selectedLocations,
  minYear,
  maxYear
}: CompanyGridProps) => {
  const gridRef = useRef<AgGridReact>(null);

  const onGridReady = useCallback((params: GridReadyEvent) => {
    const gridApi = params.api;
    gridApi.sizeColumnsToFit();
    
    const resizeObserver = new ResizeObserver(() => {
      if (!gridApi.isDestroyed()) {
        gridApi.sizeColumnsToFit();
      }
    });
    
    const gridElement = document.querySelector('#ag-grid-container');
    if (gridElement) {
      resizeObserver.observe(gridElement);
    }

    return () => {
      resizeObserver.disconnect();
    };
  }, []);

  // Filter the data based on selected filters
  const getFilteredData = useCallback(() => {
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
  }, [companies, selectedSymbols, selectedSectors, selectedSubIndustries, selectedLocations, minYear, maxYear]);

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>S&P 500 Companies</CardTitle>
      </CardHeader>
      <CardContent>
        <div id="ag-grid-container" className="h-[600px] w-full ag-theme-alpine">
          <AgGridReact
            ref={gridRef}
            columnDefs={infoColumns}
            rowData={getFilteredData()}
            defaultColDef={{
              flex: 1,
              minWidth: 100,
              resizable: true,
              sortable: true,
              filter: false
            }}
            pagination={true}
            paginationPageSize={100}
            enableCellTextSelection={true}
            ensureDomOrder={true}
            onGridReady={onGridReady}
            animateRows={true}
            rowSelection={{
              type: 'multiple',
              enableClickSelection: true
            }}
            suppressMovableColumns={true}
          />
        </div>
      </CardContent>
    </Card>
  );
};
