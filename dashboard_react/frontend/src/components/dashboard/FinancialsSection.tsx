import { Financial, FilterOptions } from '@/types/interfaces';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { dateFormatter, currencyFormatter } from '@/utils/formatters';
import { MultiSelect } from "@/components/custom/multi-select";

{/*****************************************************************************/}
{/* Interface Definitions */}

interface FinancialsSectionProps {
  filterOptions: FilterOptions;                  // Available filter options
  selectedTicker: string;                        // Currently selected stock ticker
  setSelectedTicker: (ticker: string) => void;   // Function to update selected ticker
  financialsData: Financial[];                  // Financial data for selected ticker
  loading?: boolean;                            // Loading state indicator
}

{/*****************************************************************************/}
{/* FinancialsSection Component */}
export const FinancialsSection = ({
  filterOptions,
  selectedTicker,
  setSelectedTicker,
  financialsData,
  loading = false
}: FinancialsSectionProps) => {
  // Convert selected ticker to option format
  const selectedOption = selectedTicker 
    ? [{ label: selectedTicker, value: selectedTicker }] 
    : [];

  // Convert available symbols to options format
  const symbolOptions = filterOptions.symbols.map(symbol => ({
    label: symbol,
    value: symbol
  }));

  // Handle selection changes
  const handleSelectionChange = (selected: { label: string; value: string }[]) => {
    // Take the last selected value for single-select behavior
    const lastSelected = selected[selected.length - 1];
    setSelectedTicker(lastSelected ? lastSelected.value : '');
  };

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Debug: Financials Data
          {loading && (
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Ticker Selection with MultiSelect */}
        <div className="w-[300px] mb-4">
          <MultiSelect
            options={symbolOptions}
            selected={selectedOption}
            onChange={handleSelectionChange}
            placeholder="Select a symbol..."
          />
        </div>

        {/* Financials Data Display */}
        <div className="space-y-4 relative">
          {/* Loading Overlay */}
          {loading && (
            <div className="absolute inset-0 bg-background/50 flex items-center justify-center z-50">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          )}

          {/* First Record Preview */}
          <div>
            <h3 className="font-semibold mb-2">First Financial Record:</h3>
            {financialsData.length > 0 ? (
              <pre className="bg-gray-100 p-4 rounded-lg overflow-auto">
                {JSON.stringify(financialsData[0], null, 2)}
              </pre>
            ) : (
              <p className="text-gray-500">No financial data available</p>
            )}
          </div>
          
          {/* Financials Data Table */}
          <div>
            <h3 className="font-semibold mb-2">Financial Data Table (First 5 Records):</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-200">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 border">Date</th>
                    <th className="px-4 py-2 border">Ticker</th>
                    <th className="px-4 py-2 border">Variable</th>
                    <th className="px-4 py-2 border">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {financialsData.slice(0, 5).map((record, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border">{dateFormatter({ value: record.date })}</td>
                      <td className="px-4 py-2 border">{record.ticker}</td>
                      <td className="px-4 py-2 border">{record.variable}</td>
                      <td className="px-4 py-2 border">{currencyFormatter(record.value)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Summary Information */}
          <div>
            <h3 className="font-semibold mb-2">Total Records: {financialsData.length}</h3>
          </div>

          {/* Unique Variables */}
          <div>
            <h3 className="font-semibold mb-2">Available Financial Variables:</h3>
            <div className="flex flex-wrap gap-2">
              {Array.from(new Set(financialsData.map(d => d.variable))).map((variable, index) => (
                <span 
                  key={index} 
                  className="px-2 py-1 bg-gray-100 rounded text-sm"
                >
                  {variable}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-2">Current Selected Ticker: {selectedTicker || 'None'}</h3>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
