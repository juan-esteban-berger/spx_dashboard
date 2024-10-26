import { AgGridReact } from 'ag-grid-react';
import { Company } from '@/types/interfaces';
import { infoColumns } from './CompanyGridColumns';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

{/*****************************************************************************/}
{/* Interface Definitions */}

interface CompanyGridProps {
  companies: Company[]  // Array of companies to display in the grid
}

{/*****************************************************************************/}
{/* CompanyGrid Component */}
// Displays company data in a sortable, filterable grid using AG-Grid
export const CompanyGrid = ({ companies }: CompanyGridProps) => {
  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>S&P 500 Companies</CardTitle>
      </CardHeader>
      <CardContent>
        {/* AG-Grid Container */}
        <div className="h-[600px] w-full ag-theme-alpine">
          <AgGridReact
            // Data configuration
            columnDefs={infoColumns}
            rowData={companies}
            
            // Column configuration
            defaultColDef={{
              flex: 1,
              minWidth: 100,
              resizable: true,
            }}
            
            // Grid features
            pagination={true}
            paginationPageSize={100}
            enableCellTextSelection={true}
            ensureDomOrder={true}
            
            // Grid initialization
            onGridReady={(params) => {
              params.api.sizeColumnsToFit();
            }}
          />
        </div>
      </CardContent>
    </Card>
  );
};
